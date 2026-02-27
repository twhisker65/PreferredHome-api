from __future__ import annotations

import re

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
    # Special-case common symbols
    h = h.replace("#", " Number ")
    h = h.replace("/", " ")
    h = h.replace("&", " ")
    # Collapse to tokens
    h = _non_alnum.sub(" ", h).strip()
    return [w for w in h.split() if w]


def sheet_key_to_camel(h: str) -> str:
    # Preserve "ID" exactly as "id"
    if h.strip().upper() == "ID":
        return "id"
    words = _words_from_sheet_header(h)
    if not words:
        return "field"
    first = words[0].lower()
    rest = [w[:1].upper() + w[1:].lower() if w else "" for w in words[1:]]
    return first + "".join(rest)


def _norm_api_key(k: str) -> str:
    # normalize API keys for matching
    return _non_alnum.sub("", k).lower()


def build_listings_keymaps() -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Builds:
      api_to_sheet:  apiKey(camelCase) -> sheet column name (exact)
      sheet_to_api:  sheet column name -> apiKey(camelCase)
    Based on the current sheet headers.
    """
    df = load_listings_df()
    cols = [str(c) for c in df.columns.tolist()]

    sheet_to_api: Dict[str, str] = {}
    api_to_sheet: Dict[str, str] = {}

    # Create a stable mapping from existing columns
    for col in cols:
        api_key = sheet_key_to_camel(col)
        sheet_to_api[col] = api_key
        api_to_sheet[_norm_api_key(api_key)] = col

    # Hard overrides / aliases for nicer keys (optional)
    # If your sheet header is "Unit #", the derived key becomes "unitNumber".
    # If you prefer "unitNo" or "unit", add alias here.
    aliases = {
        "unit": "unitNumber",
        "zipcode": "zipCode",
        "listingurl": "listingUrl",
        "photourl": "photoUrl",
    }
    # Apply aliases only if the target exists in the sheet
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
        # Also accept raw sheet keys (with spaces) if user sends them
        if nk in api_to_sheet:
            out[api_to_sheet[nk]] = v
        else:
            # last resort: keep original key (may already match sheet)
            out[str(k)] = v
    return out


def sheet_row_to_api(row: Dict[str, Any], sheet_to_api: Dict[str, str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in (row or {}).items():
        api_key = sheet_to_api.get(str(k), sheet_key_to_camel(str(k)))
        out[api_key] = "" if v is None else v
    return out


@app.get("/health")
def health():
    return {"ok": True}


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

        # Ensure ID exists in sheet payload
        if "ID" not in sheet_payload and "id" not in sheet_payload:
            sheet_payload["ID"] = generate_id()
        elif "id" in sheet_payload and "ID" not in sheet_payload:
            sheet_payload["ID"] = sheet_payload.pop("id")

        row = add_listing(sheet_payload)
        return sheet_row_to_api(row, sheet_to_api)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/listings/{listing_id}")
def listings_put(listing_id: str, payload: Dict[str, Any]):
    try:
        api_to_sheet, sheet_to_api = build_listings_keymaps()
        sheet_payload = api_payload_to_sheet(payload, api_to_sheet)

        # force ID consistency
        sheet_payload["ID"] = listing_id

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
    # Keep common as-is
    if k.strip().upper() == "ID":
        return "id"
    return sheet_key_to_camel(k)


def build_baseline_keymaps(existing: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str]]:
    # existing keys are whatever the sheet uses
    sheet_keys = [str(k) for k in (existing or {}).keys()]
    sheet_to_api = {k: baseline_key_to_camel(k) for k in sheet_keys}
    api_to_sheet = {_norm_api_key(v): k for k, v in sheet_to_api.items()}
    return api_to_sheet, sheet_to_api


@app.get("/baseline")
def baseline_get():
    try:
        base = load_baseline()  # dict with sheet-style keys
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
        # save_baseline might return dict or something else; normalize if dict
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

    # Normalize to camelCase for the app
    # Expected sheet columns: Category, Label, Weight, Notes (but we derive safely)
    sheet_to_api = {k: sheet_key_to_camel(str(k)) for k in (df.columns.tolist() if not df.empty else [])}
    return [sheet_row_to_api(r, sheet_to_api) for r in rows]


@app.post("/categories")
def categories_post(payload: Dict[str, Any]):
    try:
        # Accept clean API keys
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