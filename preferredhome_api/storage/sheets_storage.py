# =============================================================
# sheets_storage.py — PreferredHome API Build 3.2.03 HOTFIX
# Google Sheets read/write layer.
# Fix: load_listings_df() now casts all columns to object dtype
# after load. This prevents gspread from inferring int64 for any
# column (e.g. Zip Code stored as a number in the sheet), which
# caused HTTP 400 "Invalid value for dtype int64" on Edit saves.
# =============================================================

import math
import gspread
import pandas as pd
from google.oauth2 import service_account
from functools import lru_cache
from typing import Optional, Dict, Any

from preferredhome_api.core.settings import get_settings, load_service_account_dict
from preferredhome_api.core import config_constants as cfg
from preferredhome_api.utils.helpers import generate_id

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@lru_cache(maxsize=1)
def get_google_client():
    settings = get_settings()
    creds_dict = load_service_account_dict(settings)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=SCOPE
    )
    return gspread.authorize(creds)


@lru_cache(maxsize=1)
def get_spreadsheet():
    settings = get_settings()
    client = get_google_client()
    if settings.spreadsheet_url:
        return client.open_by_url(settings.spreadsheet_url)
    name = settings.spreadsheet_name or getattr(cfg, "SPREADSHEET_NAME", "")
    if not name:
        raise ValueError("Missing SPREADSHEET_NAME or SPREADSHEET_URL.")
    return client.open(name)


def get_worksheet(tab_name: str):
    ss = get_spreadsheet()
    try:
        return ss.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = ss.add_worksheet(title=tab_name, rows=1000, cols=50)
        if tab_name == cfg.TAB_LISTINGS:
            ws.append_row(cfg.LISTINGS_COLUMNS)
        elif tab_name == cfg.TAB_CATEGORIES:
            ws.append_row(["Category", "Label", "Weight", "Notes"])
        elif tab_name == cfg.TAB_BASELINE:
            ws.append_row(["Field", "Value"])
        return ws


def sheet_to_df(tab_name: str) -> pd.DataFrame:
    ws = get_worksheet(tab_name)
    rows = ws.get_all_records()
    return pd.DataFrame(rows)


def _bool_to_sheet_str(v) -> str:
    """
    Converts any value to a string safe for writing to Google Sheets.
    Python booleans and string 'True'/'False' are written as 'TRUE'/'FALSE'
    (all caps) to match Google Sheets boolean convention.
    """
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    s = str(v).strip()
    if s == "True":
        return "TRUE"
    if s == "False":
        return "FALSE"
    return s


def df_to_sheet(tab_name: str, df: pd.DataFrame):
    """
    Writes a DataFrame to a Google Sheet tab.

    Safe backup/restore pattern:
    - A snapshot of the current sheet is taken before any changes.
    - If the write fails at any point, the snapshot is restored.
    - This prevents data loss from a crash mid-write.

    Boolean values are written as 'TRUE' / 'FALSE' (all caps).
    """
    ws = get_worksheet(tab_name)

    # --- Step 1: Take a backup snapshot of the current sheet ---
    try:
        backup = ws.get_all_values()  # List of rows including header
    except Exception:
        backup = []

    # --- Step 2: Build the rows to write ---
    header = list(df.columns)
    # Apply boolean casing and convert all values to strings
    data_rows = [
        [_bool_to_sheet_str(cell) for cell in row]
        for row in df.values.tolist()
    ]
    all_rows = [header] + data_rows

    # --- Step 3: Write with restore on failure ---
    try:
        ws.clear()
        if all_rows:
            ws.append_rows(all_rows)
    except Exception as write_error:
        # Restore from backup to prevent data loss
        if backup:
            try:
                ws.clear()
                ws.append_rows(backup)
            except Exception:
                pass  # Best-effort restore — original error is re-raised below
        raise write_error


# -------------------------------------------------------------------
# NaN sanitization — applied to every row before JSON response
# -------------------------------------------------------------------

def _sanitize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Replace float NaN and None with empty string for safe JSON serialization."""
    out = {}
    for k, v in row.items():
        if v is None:
            out[k] = ""
        elif isinstance(v, float) and math.isnan(v):
            out[k] = ""
        else:
            out[k] = v
    return out


# -------------------------------------------------------------------
# LISTINGS
# -------------------------------------------------------------------

def load_listings_df() -> pd.DataFrame:
    df = sheet_to_df(cfg.TAB_LISTINGS)
    for col in cfg.LISTINGS_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[cfg.LISTINGS_COLUMNS]
    # Cast all columns to object dtype.
    # gspread infers Python types from sheet values — any column containing
    # only integers (e.g. Zip Code stored as a number) gets dtype int64.
    # df.at[idx, col] = <string> then raises a dtype error on Edit saves.
    # Casting to object prevents this. Type conversion is handled downstream
    # by helpers.py clean_row() / parse_row() — not by the DataFrame.
    df = df.astype(object)
    return df


def add_listing(data: Dict[str, Any]) -> Dict[str, Any]:
    df = load_listings_df()
    listing_id = data.get("id") or data.get("ID") or generate_id()
    row = {col: data.get(col, "") for col in cfg.LISTINGS_COLUMNS}
    row["id"] = listing_id
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df_to_sheet(cfg.TAB_LISTINGS, df)
    return _sanitize_row(row)


def update_listing(listing_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    df = load_listings_df()
    if "id" not in df.columns:
        raise KeyError("Listings sheet missing id column.")
    mask = df["id"].astype(str) == str(listing_id)
    if not mask.any():
        raise KeyError(f"Listing ID not found: {listing_id}")
    idx = df[mask].index[0]
    for k, v in data.items():
        if k in df.columns and k.lower() != "id":
            df.at[idx, k] = v
    df_to_sheet(cfg.TAB_LISTINGS, df)
    return _sanitize_row(df.loc[idx].to_dict())


def delete_listing(listing_id: str) -> None:
    df = load_listings_df()
    mask = df["id"].astype(str) == str(listing_id)
    if not mask.any():
        raise KeyError(f"Listing ID not found: {listing_id}")
    df = df.loc[~mask].reset_index(drop=True)
    df_to_sheet(cfg.TAB_LISTINGS, df)


# -------------------------------------------------------------------
# BASELINE
# -------------------------------------------------------------------

def load_baseline() -> Dict[str, Any]:
    ws = get_worksheet(cfg.TAB_BASELINE)
    records = ws.get_all_records()
    if not records:
        defaults = getattr(cfg, "BASELINE_DEFAULTS", {})
        ws.clear()
        ws.append_row(["Field", "Value"])
        rows = [[k, str(v)] for k, v in defaults.items()]
        if rows:
            ws.append_rows(rows)
        return defaults
    out = {}
    for r in records:
        k = r.get("Field") or r.get("field")
        v = r.get("Value") or r.get("value")
        if k:
            out[k] = v
    return out


def save_baseline(data: Dict[str, Any]) -> Dict[str, Any]:
    ws = get_worksheet(cfg.TAB_BASELINE)
    ws.clear()
    ws.append_row(["Field", "Value"])
    rows = [[k, str(v)] for k, v in data.items()]
    if rows:
        ws.append_rows(rows)
    return data


# -------------------------------------------------------------------
# CATEGORIES
# -------------------------------------------------------------------

def load_categories_df() -> pd.DataFrame:
    df = sheet_to_df(cfg.TAB_CATEGORIES)
    if df.empty:
        items = []
        defs = getattr(cfg, "CATEGORY_DEFINITIONS", {})
        for cat, labels in defs.items():
            for label in labels:
                items.append({"Category": cat, "Label": label, "Weight": "", "Notes": ""})
        if items:
            df = pd.DataFrame(items)
            df_to_sheet(cfg.TAB_CATEGORIES, df)
    return df


def add_category_item(category: str, label: str,
                       weight: Optional[float] = None, notes: str = ""):
    df = load_categories_df()
    row = {
        "Category": category,
        "Label":    label,
        "Weight":   weight if weight is not None else "",
        "Notes":    notes,
    }
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df_to_sheet(cfg.TAB_CATEGORIES, df)
    return row


def delete_category_item(category: str, label: str):
    df = load_categories_df()
    mask = (
        (df["Category"].astype(str) == str(category)) &
        (df["Label"].astype(str) == str(label))
    )
    if not mask.any():
        raise KeyError("Category item not found")
    df = df.loc[~mask].reset_index(drop=True)
    df_to_sheet(cfg.TAB_CATEGORIES, df)


# -------------------------------------------------------------------
# TOGGLES (stored in baseline tab)
# -------------------------------------------------------------------

def load_toggles() -> Dict[str, Any]:
    base = load_baseline()
    return {k: v for k, v in base.items() if str(k).startswith("toggle_")}


def save_toggles(data: Dict[str, Any]) -> Dict[str, Any]:
    base = load_baseline()
    base = {k: v for k, v in base.items() if not str(k).startswith("toggle_")}
    base.update({f"toggle_{k}": v for k, v in data.items()})
    save_baseline(base)
    return data
