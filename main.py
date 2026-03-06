from __future__ import annotations

import re
import math

from typing import Any, Dict, List, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from preferredhome_api.core.settings import get_settings
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
)
from preferredhome_api.utils.helpers import generate_id

app = FastAPI(title="PreferredHome API", version="0.2.0")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Key mapping: Sheet <-> API
# ----------------------------

_non_alnum = re.compile(r"[^A-Za-z0-9]+")


def _words_from_sheet_header(h: str) -> List[str]:
    h = h.replace("#", " Number ")
    h = h.replace("/", " ")
    h = h.replace("&", " ")
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
    rest = [w[:1].upper() + w[1:].lower() if w else "" for w in words[1:]]
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

    aliases = {
        "unit": "unitNumber",
        "zipcode": "zipCode",
        "listingurl": "listingUrl",
        "photourl": "photoUrl",
    }
    for alias_key, canonical in aliases.items():
        canonical_norm = _norm_api_key(canonical)
        if canonical_norm in api_to_sheet:
            api_to_sheet[alias_key] = api_to_sheet[canonical_norm]

    return api_to_sheet, sheet_to_api


def api_payload_to_sheet(payload: Dict[str, Any], api_to_sheet: Dict[str, str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in (payload or {}).items():
        if k is None:
            continue
        nk = _norm_api_key(str(k))
        if nk in api_to_sheet:
            out[api_to_sheet[nk]] = v
        else:
            out[str(k)] = v
    return out


def sheet_row_to_api(row: Dict[str, Any], sheet_to_api: Dict[str, str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in (row or {}).items():
        api_key = sheet_to_api.get(str(k), sheet_key_to_camel(str(k)))
        out[api_key] = "" if v is None else v
    return out


# ----------------------------
# FIX Build 3.1.15.4
# Sanitize incoming payload — replace None, NaN, and blank numeric
# values with "" before they reach pandas, preventing JSON NaN errors.
# ----------------------------

# These match cfg.NUMERIC_FIELDS exactly
_NUMERIC_FIELDS = {
    "Floor", "Bedrooms", "Bathrooms", "Square Footage",
    "Monthly Rent", "Parking Fee", "Amenity Fee", "Admin Fee",
    "Utility Fee", "Other Fee", "Total Monthly",
    "Security Deposit", "Application Fee",
    "Commute Time", "Walk Score", "Transit Score", "Bike Score",
    "Elementary School Rating", "Elementary School Distance",
    "Middle School Rating", "Middle School Distance",
    "High School Rating", "High School Distance",
}

def _sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Replace any None, float NaN, or non-numeric string in a numeric field
    with empty string "" before the payload reaches pandas.
    This prevents 'Out of range float values are not JSON compliant: nan'.
    """
    out = {}
    for k, v in payload.items():
        if k in _NUMERIC_FIELDS:
            if v is None:
                out[k] = ""
            elif isinstance(v, float) and math.isnan(v):
                out[k] = ""
            elif v == "" or v == "nan" or v == "NaN":
                out[k] = ""
            else:
                out[k] = v
        else:
            out[k] = v
    return out


@app.get("/health")
def health():
    return {"ok": "LOCAL DEV"}


# ----------------------------
# Listings
# ----------------------------

@app.get("/listings")
def listings_get():
    api_to_sheet, sheet_to_api = build_listings_keymaps()
    df = load_listings_df()
    rows = df.fillna("").to_dict(orient="records")
    return [sheet_row_to_api(r, sheet_to_api) for r in rows]


@app.post("/listings")
def listings_post(payload: Dict[str, Any]):
    try:
        api_to_sheet, sheet_to_api = build_listings_keymaps()
        sheet_payload = api_payload_to_sheet(payload, api_to_sheet)

        # FIX Bug 3: always pass lowercase "id"
        if "id" not in sheet_payload and "ID" not in sheet_payload:
            sheet_payload["id"] = generate_id()
        elif "ID" in sheet_payload and "id" not in sheet_payload:
            sheet_payload["id"] = sheet_payload.pop("ID")

        # FIX Build 3.1.15.4: sanitize numeric fields before pandas sees them
        sheet_payload = _sanitize_payload(sheet_payload)

        row = add_listing(sheet_payload)
        return sheet_row_to_api(row, sheet_to_api)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/listings/{listing_id}")
def listings_put(listing_id: str, payload: Dict[str, Any]):
    try:
        api_to_sheet, sheet_to_api = build_listings_keymaps()
        sheet_payload = api_payload_to_sheet(payload, api_to_sheet)

        # FIX Bug 2: pass lowercase "id"
        sheet_payload.pop("ID", None)
        sheet_payload["id"] = listing_id

        # FIX Build 3.1.15.4: sanitize numeric fields before pandas sees them
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


# ----------------------------
# Baseline
# ----------------------------

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
        raise HTTPException(status_code=400, detail=str(e))


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


# ----------------------------
# Categories
# ----------------------------

@app.get("/categories")
def categories_get():
    df = load_categories_df()
    rows = df.fillna("").to_dict(orient="records")
    sheet_to_api = {k: sheet_key_to_camel(str(k)) for k in (df.columns.tolist() if not df.empty else [])}
    return [sheet_row_to_api(r, sheet_to_api) for r in rows]


@app.post("/categories")
def categories_post(payload: Dict[str, Any]):
    try:
        category = payload.get("category") or payload.get("Category")
        label = payload.get("label") or payload.get("Label")
        weight = payload.get("weight") or payload.get("Weight")
        notes = payload.get("notes") or payload.get("Notes") or ""
        if not category or not label:
            raise ValueError("category and label are required.")
        return add_category_item(category, label, weight=weight if weight != "" else None, notes=notes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/categories")
def categories_delete(category: str, label: str):
    try:
        delete_category_item(category, label)
        return {"ok": True}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
