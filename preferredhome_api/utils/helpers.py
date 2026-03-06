# =============================================================
# helpers.py — PreferredHome API Build 3.2.1
# Shared helper functions.
# All field references use camelCase to match LISTINGS_COLUMNS.
# =============================================================

import uuid
from preferredhome_api.core.config_constants import (
    LISTING_SITE_URL_KEYWORDS,
    BOOLEAN_FIELDS,
    NUMERIC_FIELDS,
    CATEGORY_FIELDS,
    BASELINE_DEFAULTS,
    AC_TYPE_OPTIONS,
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
    for key, value in row.items():
        if key in BOOLEAN_FIELDS:
            # All-caps TRUE/FALSE required by Google Sheets and the API contract
            cleaned[key] = "TRUE" if value else "FALSE"
        elif key in NUMERIC_FIELDS:
            if value is None or value == "":
                cleaned[key] = ""
            else:
                try:
                    cleaned[key] = str(float(value))
                except (ValueError, TypeError):
                    cleaned[key] = ""
        elif key in CATEGORY_FIELDS:
            if isinstance(value, list):
                cleaned[key] = ", ".join(str(v) for v in value if v)
            else:
                cleaned[key] = str(value) if value else ""
        else:
            cleaned[key] = str(value).strip() if value is not None else ""
    return cleaned


def parse_row(row: dict) -> dict:
    """
    Parses a raw row from Google Sheets into Python types.
    Uses camelCase keys matching LISTINGS_COLUMNS.
    Accepts both 'TRUE'/'FALSE' (all caps) and 'True'/'False' (mixed case)
    for backwards compatibility with older sheet data.
    """
    parsed = {}
    for key, value in row.items():
        if key in BOOLEAN_FIELDS:
            parsed[key] = str(value).strip().lower() == "true"
        elif key in NUMERIC_FIELDS:
            try:
                parsed[key] = float(value) if value != "" else None
            except (ValueError, TypeError):
                parsed[key] = None
        elif key in CATEGORY_FIELDS:
            if isinstance(value, list):
                parsed[key] = value
            elif value:
                parsed[key] = [v.strip() for v in str(value).split(",") if v.strip()]
            else:
                parsed[key] = []
        else:
            parsed[key] = str(value).strip() if value is not None else ""
    return parsed


# -------------------------------------------------------------------
# BASELINE COMPARISON (camelCase field names)
# -------------------------------------------------------------------

def _ranked_color(value: str, ranking_str: str) -> str:
    """
    Returns 'green', 'yellow', or 'red' based on rank position.
    First item in ranking = most preferred (green).
    """
    ranking = [r.strip() for r in ranking_str.split(",") if r.strip()]
    if not ranking or not value:
        return "gray"
    try:
        pos = ranking.index(value)
    except ValueError:
        return "gray"
    third = max(1, len(ranking) // 3)
    if pos < third:
        return "green"
    elif pos < third * 2:
        return "yellow"
    else:
        return "red"


def get_comparison_color(field: str, value, baseline: dict) -> str:
    """
    Returns 'green', 'yellow', 'red', or 'gray' for a field value
    compared against baseline settings.
    Uses camelCase field names matching LISTINGS_COLUMNS.
    """
    if value is None or value == "" or value == []:
        return "gray"

    if field == "baseRent":
        try:
            max_rent = float(baseline.get("Max Monthly Rent", 0))
            return "green" if float(value) <= max_rent else "red"
        except (ValueError, TypeError):
            return "gray"

    if field == "squareFootage":
        try:
            min_sqft = float(baseline.get("Min Square Footage", 0))
            return "green" if float(value) >= min_sqft else "red"
        except (ValueError, TypeError):
            return "gray"

    if field == "commuteTime":
        try:
            max_commute = float(baseline.get("Max Commute Time", 0))
            return "green" if float(value) <= max_commute else "red"
        except (ValueError, TypeError):
            return "gray"

    if field == "walkScore":
        try:
            min_walk = float(baseline.get("Min Walk Score", 0))
            return "green" if float(value) >= min_walk else "red"
        except (ValueError, TypeError):
            return "gray"

    if field == "acType":
        ranking_str = baseline.get("AC Type Ranking", ",".join(AC_TYPE_OPTIONS))
        return _ranked_color(str(value), ranking_str)

    if field == "laundry":
        ranking_str = baseline.get("Laundry Ranking", ",".join(LAUNDRY_OPTIONS))
        return _ranked_color(str(value), ranking_str)

    if field == "parkingType":
        ranking_str = baseline.get("Parking Ranking", ",".join(PARKING_OPTIONS))
        return _ranked_color(str(value), ranking_str)

    if field == "noBoardApproval":
        required = str(baseline.get("Board Approval Required", "False")).strip().lower() == "true"
        listing_val = str(value).strip().lower() == "true"
        return "green" if required == listing_val else "red"

    if field == "noBrokerFee":
        acceptable = str(baseline.get("Broker Fee Acceptable", "False")).strip().lower() == "true"
        listing_val = str(value).strip().lower() == "true"
        return "green" if acceptable == listing_val else "red"

    return "gray"
