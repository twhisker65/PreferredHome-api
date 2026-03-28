# =============================================================
# helpers.py — PreferredHome API Build 3.2.14
# Reverted from 3.2.15 — commute functions removed.
# =============================================================

import uuid

from preferredhome_api.core.config_constants import (
    LISTING_SITE_URL_KEYWORDS,
    BOOLEAN_FIELDS,
    NUMERIC_FIELDS,
    CATEGORY_FIELDS,
    BASELINE_DEFAULTS,
    COOLING_TYPE_OPTIONS,
    LAUNDRY_OPTIONS,
    PARKING_OPTIONS,
)


# -------------------------------------------------------------------
# ID GENERATION
# -------------------------------------------------------------------

def generate_id() -> str:
    return str(uuid.uuid4())[:8]


# -------------------------------------------------------------------
# LISTING SITE AUTO-DETECTION
# -------------------------------------------------------------------

def detect_listing_site(url: str) -> str:
    if not url:
        return "Other"
    url_lower = url.lower()
    for keyword, site_name in LISTING_SITE_URL_KEYWORDS.items():
        if keyword in url_lower:
            return site_name
    return "Other"


# -------------------------------------------------------------------
# ZIP CODE LOOKUP
# -------------------------------------------------------------------

ZIP_STATE_MAP = {
    "100": ("New York", "NY"),    "101": ("New York", "NY"),
    "102": ("New York", "NY"),    "103": ("Staten Island", "NY"),
    "104": ("Bronx", "NY"),       "105": ("Westchester", "NY"),
    "106": ("White Plains", "NY"),"107": ("Yonkers", "NY"),
    "110": ("Queens", "NY"),
}

def lookup_zip(zip_code: str):
    """Returns (city, state) tuple for a known ZIP prefix, or (None, None)."""
    if not zip_code:
        return None, None
    prefix = zip_code[:3]
    return ZIP_STATE_MAP.get(prefix, (None, None))


# -------------------------------------------------------------------
# TOTAL MONTHLY COST
# -------------------------------------------------------------------

def calculate_total_monthly(row: dict) -> float:
    """
    Sums all monthly fee fields.
    Uses camelCase keys matching LISTINGS_COLUMNS.
    """
    fee_fields = [
        "baseRent",
        "parkingFee",
        "amenityFee",
        "adminFee",
        "utilityFee",
        "otherFee",
    ]
    total = 0.0
    for field in fee_fields:
        try:
            total += float(row.get(field) or 0)
        except (ValueError, TypeError):
            pass
    return total


# -------------------------------------------------------------------
# DATA CLEANING (camelCase field names)
# -------------------------------------------------------------------

def clean_row(row: dict) -> dict:
    """
    Cleans a listing row before saving to Google Sheets.
    Uses camelCase keys matching LISTINGS_COLUMNS.
    Boolean fields are written as 'TRUE' / 'FALSE' (all caps)
    to match Google Sheets boolean convention.
    """
    cleaned = {}
    for k, v in row.items():
        if k in BOOLEAN_FIELDS:
            if isinstance(v, bool):
                cleaned[k] = "TRUE" if v else "FALSE"
            elif isinstance(v, str) and v.strip().upper() in ("TRUE", "1", "YES"):
                cleaned[k] = "TRUE"
            else:
                cleaned[k] = "FALSE"
        elif k in NUMERIC_FIELDS:
            if v in (None, "", "null"):
                cleaned[k] = ""
            else:
                try:
                    f = float(str(v))
                    import math
                    if math.isnan(f) or math.isinf(f):
                        cleaned[k] = ""
                    else:
                        cleaned[k] = int(f) if f == int(f) else f
                except (ValueError, TypeError):
                    cleaned[k] = ""
        elif k in CATEGORY_FIELDS:
            if isinstance(v, list):
                cleaned[k] = ", ".join(str(x) for x in v if x)
            elif isinstance(v, str):
                cleaned[k] = v
            else:
                cleaned[k] = ""
        else:
            cleaned[k] = "" if v is None else str(v)
    return cleaned
