# =============================================================
# main.py — PreferredHome API Build 3.2.15
# Added: commute calculation in POST/PUT handlers.
# Added: POST /commute/recalculate-all (load once, write once).
# =============================================================

from __future__ import annotations

import re
import math
from typing import Any, Dict, List, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from preferredhome_api.core.settings import get_settings
from preferredhome_api.core import config_constants as cfg
from preferredhome_api.storage.sheets_storage import (
    load_listings_df,
    add_listing,
    update_listing,
    delete_listing,
    load_baseline,
    save_baseline,
    load_categories_df,
    add_category_item,
    delete_category_item,
    df_to_sheet,
)
from preferredhome_api.utils.helpers import generate_id, calculate_commute

app = FastAPI(title="PreferredHome API", version="3.2.15")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------
# KEY MAPPING — Sheet column names <-> API camelCase keys
# -------------------------------------------------------------------

_non_alnum = re.compile(r"[^A-Za-z0-9]+")


def _words_from_sheet_header(h: str) -> List[str]:
    h = h.replace("#", " Number ").replace("/", " ").replace("&", " ")
    h = _non_alnum.sub(" ", h).strip()
    return [w for w in h.split() if w]


def _is_camel_case(h: str) -> bool:
    return bool(re.match(r"^[a-z][A-Za-z0-9]*$", h))


def sheet_key_to_camel(h: str) -> str:
    if h.strip().upper() == "ID":
        return "id"
    if _is_camel_case(h.strip()):
        return h.strip()
    words = _words_from_sheet_header(h)
    if not words:
        return "field"
    first = words[0].lower()
    rest = [w[:1].upper() + w[1:].lower() for w in words[1:] if w]
    return first + "".join(rest)


def _norm_api_key(k: str) -> str:
    return _non_alnum.sub("", k).lower()


def build_listings_keymaps() -> Tuple[Dict[str, str], Dict[str, str]]:
    df = load_listings_df()
    cols = [str(c) for c in df.columns.tolist()]
    sheet_to_api: Dict[str, str] = {}
    api_to_sheet: Dict[str, str] = {}
    for col in cols:
        api_key = sheet_key_to_camel(col)
        sheet_to_api[col] = api_key
        api_to_sheet[_norm_api_key(api_key)] = col
    for alias, canonical in [("preferred", "preferred"), ("id", "id")]:
        api_to_sheet.setdefault(_norm_api_key(alias), api_to_sheet.get(_norm_api_key(canonical), alias))
    return api_to_sheet, sheet_to_api


def api_payload_to_sheet(payload: Dict[str, Any], api_to_sheet: Dict[str, str]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for k, v in payload.items():
        sheet_key = api_to_sheet.get(_norm_api_key(k), k)
        result[sheet_key] = v
    return result


def sheet_row_to_api(row: Dict[str, Any], sheet_to_api: Dict[str, str]) -> Dict[str, Any]:
    return {sheet_to_api.get(k, sheet_key_to_camel(k)): v for k, v in row.items()}


# -------------------------------------------------------------------
# PAYLOAD SANITIZATION
# -------------------------------------------------------------------

_NUMERIC_SET = set(cfg.NUMERIC_FIELDS)


def _sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    cleaned: Dict[str, Any] = {}
    for k, v in payload.items():
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            cleaned[k] = ""
        elif k in _NUMERIC_SET:
            if v in (None, "", "null", "nan", "inf", "-inf"):
                cleaned[k] = ""
            else:
                try:
                    f = float(str(v))
                    if math.isnan(f) or math.isinf(f):
                        cleaned[k] = ""
                    else:
                        cleaned[k] = f
                except (ValueError, TypeError):
                    cleaned[k] = ""
        else:
            cleaned[k] = v
    return cleaned


# -------------------------------------------------------------------
# CALCULATED TOTALS
# -------------------------------------------------------------------

def _inject_calculated_totals(payload: Dict[str, Any]) -> Dict[str, Any]:
    def _n(key: str) -> float:
        try:
            return float(payload.get(key) or 0)
        except (ValueError, TypeError):
            return 0.0

    total_monthly = (
        _n("baseRent") + _n("parkingFee") + _n("amenityFee") +
        _n("adminFee") + _n("utilityFee") + _n("otherFee")
    )
    total_upfront = (
        _n("securityDeposit") + _n("applicationFee") +
        _n("brokerFee") + _n("moveInFee")
    )
    payload = dict(payload)
    payload["totalMonthly"] = total_monthly
    payload["totalUpfront"] = total_upfront
    return payload


# -------------------------------------------------------------------
# COMMUTE HELPER — extract commute profile fields from payload
# -------------------------------------------------------------------

def _extract_commute_fields(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], str, str, str]:
    """
    Pops workAddress, commuteMethod, departureTime from payload (if present).
    These are profile fields — not listing columns — so they must be removed
    before the payload is passed to the sheet layer.
    Returns (cleaned_payload, work_address, commute_method, departure_time).
    """
    payload = dict(payload)
    work_address    = str(payload.pop("workAddress",    "") or "").strip()
    commute_method  = str(payload.pop("commuteMethod",  "") or "Transit").strip()
    departure_time  = str(payload.pop("departureTime",  "") or "").strip()
    return payload, work_address, commute_method, departure_time


# -------------------------------------------------------------------
# HEALTH
# -------------------------------------------------------------------

@app.get("/health")
def health():
    return {"ok": "PreferredHome API 3.2.15"}


# -------------------------------------------------------------------
# LISTINGS
# -------------------------------------------------------------------

@app.get("/listings")
def listings_get():
    try:
        df = load_listings_df()
        import numpy as np
        df = df.replace([np.inf, -np.inf], "").fillna("")
        api_to_sheet, sheet_to_api = build_listings_keymaps()
        rows = df.to_dict(orient="records")
        return [sheet_row_to_api(r, sheet_to_api) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/listings")
def listings_post(payload: Dict[str, Any]):
    try:
        api_to_sheet, sheet_to_api = build_listings_keymaps()
        payload = _sanitize_payload(payload)
        payload = _inject_calculated_totals(payload)

        # Extract commute profile fields — these are not listing columns.
        payload, work_address, commute_method, departure_time = _extract_commute_fields(payload)

        # Calculate commute before saving so it goes into the row in one write.
        if work_address:
            street = str(payload.get("streetAddress", "") or "").strip()
            city   = str(payload.get("city",          "") or "").strip()
            state  = str(payload.get("state",         "") or "").strip()
            listing_address = ", ".join(p for p in [street, city, state] if p)
            if listing_address:
                mins = calculate_commute(listing_address, work_address, commute_method, departure_time)
                if mins is not None:
                    payload["commuteTime"] = mins

        sheet_payload = api_payload_to_sheet(payload, api_to_sheet)
        if "id" not in sheet_payload and "ID" not in sheet_payload:
            sheet_payload["id"] = generate_id()
        elif "ID" in sheet_payload and "id" not in sheet_payload:
            sheet_payload["id"] = sheet_payload.pop("ID")
        sheet_payload = _sanitize_payload(sheet_payload)
        row = add_listing(sheet_payload)
        return sheet_row_to_api(row, sheet_to_api)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/listings/{listing_id}")
def listings_put(listing_id: str, payload: Dict[str, Any]):
    try:
        api_to_sheet, sheet_to_api = build_listings_keymaps()
        payload = _sanitize_payload(payload)
        payload = _inject_calculated_totals(payload)

        # Extract commute profile fields — these are not listing columns.
        payload, work_address, commute_method, departure_time = _extract_commute_fields(payload)

        # Calculate commute before saving so it goes into the row in one write.
        if work_address:
            street = str(payload.get("streetAddress", "") or "").strip()
            city   = str(payload.get("city",          "") or "").strip()
            state  = str(payload.get("state",         "") or "").strip()
            listing_address = ", ".join(p for p in [street, city, state] if p)
            if listing_address:
                mins = calculate_commute(listing_address, work_address, commute_method, departure_time)
                if mins is not None:
                    payload["commuteTime"] = mins

        sheet_payload = api_payload_to_sheet(payload, api_to_sheet)
        sheet_payload.pop("ID", None)
        sheet_payload["id"] = listing_id
        sheet_payload = _sanitize_payload(sheet_payload)
        row = update_listing(listing_id, sheet_payload)
        return sheet_row_to_api(row, sheet_to_api)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/listings/{listing_id}")
def listings_delete(listing_id: str):
    try:
        delete_listing(listing_id)
        return {"ok": True}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------------------------------------------------------------------
# COMMUTE — RECALCULATE ALL
# Load sheet ONCE. Mutate commuteTime in memory. Write ONCE.
# Never calls update_listing() in a loop.
# -------------------------------------------------------------------

@app.post("/commute/recalculate-all")
def commute_recalculate_all(payload: Dict[str, Any]):
    work_address   = str(payload.get("workAddress",   "") or "").strip()
    commute_method = str(payload.get("commuteMethod", "") or "Transit").strip()
    departure_time = str(payload.get("departureTime", "") or "").strip()

    if not work_address:
        return {"updated": 0, "skipped": 0, "reason": "no work address"}

    # Load the full sheet exactly once.
    df = load_listings_df()

    updated = 0
    skipped = 0

    # Iterate rows — calculate commute in memory, no writes inside this loop.
    for idx in df.index:
        street = str(df.at[idx, "Street Address"] if "Street Address" in df.columns else "").strip()
        city   = str(df.at[idx, "City"]           if "City"           in df.columns else "").strip()
        state  = str(df.at[idx, "State"]          if "State"          in df.columns else "").strip()

        if not street:
            skipped += 1
            continue

        listing_address = ", ".join(p for p in [street, city, state] if p)
        mins = calculate_commute(listing_address, work_address, commute_method, departure_time)

        if mins is not None:
            if "Commute Time" in df.columns:
                df.at[idx, "Commute Time"] = mins
            updated += 1
        else:
            skipped += 1

    # Write the entire DataFrame exactly once.
    df_to_sheet(cfg.TAB_LISTINGS, df)

    return {"updated": updated, "skipped": skipped}


# -------------------------------------------------------------------
# BASELINE
# -------------------------------------------------------------------

def baseline_key_to_camel(k: str) -> str:
    if k.strip().upper() == "ID":
        return "id"
    return sheet_key_to_camel(k)


def build_baseline_keymaps(existing: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str]]:
    sheet_keys = [str(k) for k in (existing or {}).keys()]
    sheet_to_api = {k: baseline_key_to_camel(k) for k in sheet_keys}
    api_to_sheet = {_norm_api_key(v): k for k, v in sheet_to_api.items()}
    return api_to_sheet, sheet_to_api


@app.get("/baseline")
def baseline_get():
    try:
        base = load_baseline()
        api_to_sheet, sheet_to_api = build_baseline_keymaps(base)
        return sheet_row_to_api(base, sheet_to_api)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/baseline")
def baseline_put(payload: Dict[str, Any]):
    try:
        current = load_baseline()
        api_to_sheet, sheet_to_api = build_baseline_keymaps(current)
        sheet_payload = api_payload_to_sheet(payload, api_to_sheet)
        saved = save_baseline(sheet_payload)
        if isinstance(saved, dict):
            return sheet_row_to_api(saved, sheet_to_api)
        return saved
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------------------------------------------------------
# CATEGORIES
# -------------------------------------------------------------------

@app.get("/categories")
def categories_get():
    df = load_categories_df()
    rows = df.fillna("").to_dict(orient="records")
    sheet_to_api = {
        k: sheet_key_to_camel(str(k))
        for k in (df.columns.tolist() if not df.empty else [])
    }
    return [sheet_row_to_api(r, sheet_to_api) for r in rows]


@app.post("/categories")
def categories_post(payload: Dict[str, Any]):
    try:
        category = payload.get("category") or payload.get("Category")
        label    = payload.get("label")    or payload.get("Label")
        weight   = payload.get("weight")   or payload.get("Weight")
        notes    = payload.get("notes")    or payload.get("Notes") or ""
        if not category or not label:
            raise ValueError("category and label are required.")
        return add_category_item(
            category, label,
            weight=weight if weight != "" else None,
            notes=notes,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/categories")
def categories_delete(category: str, label: str):
    try:
        delete_category_item(category, label)
        return {"ok": True}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
