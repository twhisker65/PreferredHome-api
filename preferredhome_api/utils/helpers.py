# =============================================================
# utils/helpers.py — Apartment Tracker Build 3
# Shared helper functions used across multiple pages.
# =============================================================

import uuid
import re
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
    """
    Generates a unique ID for each new listing.
    Example: "a3f9c1b2"
    """
    return str(uuid.uuid4())[:8]


# -------------------------------------------------------------------
# LISTING SITE AUTO-DETECTION
# -------------------------------------------------------------------

def detect_listing_site(url: str) -> str:
    """
    Detects the listing site name from a URL.
    Returns the site name if found, otherwise returns "Other".
    """
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

# A small lookup table for common US zip code prefixes.
# This gives a reasonable City/State without any external API.
ZIP_STATE_MAP = {
    "100": ("New York", "NY"), "101": ("New York", "NY"),
    "102": ("New York", "NY"), "103": ("Staten Island", "NY"),
    "104": ("Bronx", "NY"),    "105": ("Westchester", "NY"),
    "106": ("White Plains", "NY"), "107": ("Yonkers", "NY"),
    "110": ("Queens", "NY"),   "111": ("Queens", "NY"),
    "112": ("Brooklyn", "NY"), "113": ("Queens", "NY"),
    "114": ("Queens", "NY"),   "115": ("Queens", "NY"),
    "116": ("Queens", "NY"),   "117": ("Long Island", "NY"),
    "118": ("Long Island", "NY"), "119": ("Long Island", "NY"),
    "200": ("Washington", "DC"), "201": ("Washington", "DC"),
    "202": ("Washington", "DC"), "203": ("Washington", "DC"),
    "204": ("Washington", "DC"), "205": ("Washington", "DC"),
    "300": ("Atlanta", "GA"),  "301": ("Atlanta", "GA"),
    "302": ("Atlanta", "GA"),
    "330": ("Miami", "FL"),    "331": ("Miami", "FL"),
    "332": ("Miami", "FL"),    "333": ("Fort Lauderdale", "FL"),
    "600": ("Chicago", "IL"),  "601": ("Chicago", "IL"),
    "602": ("Chicago", "IL"),
    "900": ("Los Angeles", "CA"), "901": ("Los Angeles", "CA"),
    "902": ("Beverly Hills", "CA"), "903": ("Los Angeles", "CA"),
    "940": ("San Francisco", "CA"), "941": ("San Francisco", "CA"),
    "942": ("Sacramento", "CA"),
    "980": ("Seattle", "WA"),  "981": ("Seattle", "WA"),
    "770": ("Houston", "TX"),  "771": ("Houston", "TX"),
    "750": ("Dallas", "TX"),   "751": ("Dallas", "TX"),
    "850": ("Phoenix", "AZ"),  "852": ("Phoenix", "AZ"),
    "800": ("Denver", "CO"),   "801": ("Denver", "CO"),
    "021": ("Boston", "MA"),   "022": ("Boston", "MA"),
    "191": ("Philadelphia", "PA"), "190": ("Philadelphia", "PA"),
    "481": ("Detroit", "MI"),  "482": ("Detroit", "MI"),
    "430": ("Columbus", "OH"), "441": ("Cleveland", "OH"),
    "971": ("Portland", "OR"), "972": ("Portland", "OR"),
    "891": ("Las Vegas", "NV"), "890": ("Las Vegas", "NV"),
    "671": ("Nashville", "TN"), "372": ("Nashville", "TN"),
    "282": ("Charlotte", "NC"), "277": ("Raleigh", "NC"),
    "302": ("Atlanta", "GA"),  "303": ("Atlanta", "GA"),
    "700": ("New Orleans", "LA"), "701": ("New Orleans", "LA"),
    "531": ("Milwaukee", "WI"), "530": ("Milwaukee", "WI"),
    "550": ("Minneapolis", "MN"), "551": ("Minneapolis", "MN"),
    "680": ("Omaha", "NE"),    "681": ("Omaha", "NE"),
    "501": ("Little Rock", "AR"), "720": ("Oklahoma City", "OK"),
    "871": ("Albuquerque", "NM"), "870": ("Albuquerque", "NM"),
    "841": ("Salt Lake City", "UT"), "840": ("Salt Lake City", "UT"),
    "967": ("Honolulu", "HI"), "968": ("Honolulu", "HI"),
    "995": ("Anchorage", "AK"), "994": ("Anchorage", "AK"),
}

def lookup_city_state(zip_code: str) -> tuple:
    """
    Returns (city, state) for a given zip code using a prefix lookup.
    Returns ("", "") if not found.
    """
    if not zip_code or len(str(zip_code)) < 3:
        return ("", "")
    prefix = str(zip_code)[:3]
    return ZIP_STATE_MAP.get(prefix, ("", ""))


# -------------------------------------------------------------------
# FEE CALCULATION
# -------------------------------------------------------------------

def calculate_total_monthly(row: dict) -> float:
    """
    Calculates Total Monthly cost from all fee fields.
    Returns 0.0 if all fields are empty or zero.
    """
    fee_fields = [
        "Monthly Rent",
        "Parking Fee",
        "Amenity Fee",
        "Admin Fee",
        "Utility Fee",
        "Other Fee",
    ]
    total = 0.0
    for field in fee_fields:
        try:
            total += float(row.get(field) or 0)
        except (ValueError, TypeError):
            pass
    return total


# -------------------------------------------------------------------
# DATA CLEANING
# -------------------------------------------------------------------

def clean_row(row: dict) -> dict:
    """
    Cleans a listing row before saving to Google Sheets.
    - Converts boolean fields to "True" / "False" strings
    - Converts numeric fields to strings (blank if empty)
    - Strips whitespace from text fields
    - Joins list values in category fields with commas
    """
    cleaned = {}
    for key, value in row.items():

        if key in BOOLEAN_FIELDS:
            cleaned[key] = "True" if value else "False"

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
    Parses a raw row from Google Sheets into proper Python types.
    - Boolean fields become True/False
    - Numeric fields become float (or None if empty)
    - Category fields become lists
    - All other fields remain strings
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
# BASELINE COMPARISON LOGIC
# -------------------------------------------------------------------

def get_comparison_color(field: str, value, baseline: dict) -> str:
    """
    Returns "green", "yellow", "red", or "gray" for a field value
    compared against the baseline settings.
    """
    if value is None or value == "" or value == []:
        return "gray"

    # --- Monthly Rent: lower is better, max budget ---
    if field == "Monthly Rent":
        try:
            max_rent = float(baseline.get("Max Monthly Rent", 0))
            return "green" if float(value) <= max_rent else "red"
        except (ValueError, TypeError):
            return "gray"

    # --- Square Footage: higher is better, minimum ---
    if field == "Square Footage":
        try:
            min_sqft = float(baseline.get("Min Square Footage", 0))
            return "green" if float(value) >= min_sqft else "red"
        except (ValueError, TypeError):
            return "gray"

    # --- Commute Time: lower is better, max limit ---
    if field == "Commute Time":
        try:
            max_commute = float(baseline.get("Max Commute Time", 0))
            return "green" if float(value) <= max_commute else "red"
        except (ValueError, TypeError):
            return "gray"

    # --- Walk Score: higher is better, minimum ---
    if field == "Walk Score":
        try:
            min_walk = float(baseline.get("Min Walk Score", 0))
            return "green" if float(value) >= min_walk else "red"
        except (ValueError, TypeError):
            return "gray"

    # --- AC Type: user-defined ranking ---
    if field == "AC Type":
        ranking_str = baseline.get("AC Type Ranking", ",".join(AC_TYPE_OPTIONS))
        return _ranked_color(str(value), ranking_str)

    # --- Laundry: user-defined ranking ---
    if field == "Laundry":
        ranking_str = baseline.get("Laundry Ranking", ",".join(LAUNDRY_OPTIONS))
        return _ranked_color(str(value), ranking_str)

    # --- Parking Type: user-defined ranking ---
    if field == "Parking Type":
        ranking_str = baseline.get("Parking Ranking", ",".join(PARKING_OPTIONS))
        return _ranked_color(str(value), ranking_str)

    # --- Board Approval: binary match ---
    if field == "Board Approval":
        required = str(baseline.get("Board Approval Required", "False")).strip().lower() == "true"
        listing_val = str(value).strip().lower() == "true"
        # Green if: user wants it and it has it, OR user doesn't want it and it doesn't have it
        return "green" if required == listing_val else "red"

    # --- Broker Fee: binary match ---
    if field == "Broker Fee":
        acceptable = str(baseline.get("Broker Fee Acceptable", "False")).strip().lower() == "true"
        listing_val = str(value).strip().lower() == "true"
        return "green" if acceptable == listing_val else "red"

    return "gray"


def _ranked_color(value: str, ranking_str: str) -> str:
    """
    Helper for user-defined ranking fields.
    Rank 1 = green, ranks 2+ = yellow, "None" = red, not found = gray.
    """
    if not ranking_str:
        return "gray"
    ranking = [r.strip() for r in ranking_str.split(",") if r.strip()]
    if not ranking:
        return "gray"
    try:
        index = ranking.index(value)
        if index == 0:
            return "green"
        elif value.lower() == "none":
            return "red"
        else:
            return "yellow"
    except ValueError:
        if value.lower() == "none":
            return "red"
        return "gray"


# -------------------------------------------------------------------
# FORMATTING HELPERS
# -------------------------------------------------------------------

def format_currency(value) -> str:
    """Formats a number as a dollar amount. Returns blank if empty."""
    try:
        return f"${float(value):,.0f}" if value not in (None, "", 0) else ""
    except (ValueError, TypeError):
        return ""


def format_number(value, decimals: int = 0) -> str:
    """Formats a number with optional decimal places. Returns blank if empty."""
    try:
        if value in (None, ""):
            return ""
        return f"{float(value):,.{decimals}f}"
    except (ValueError, TypeError):
        return ""


def format_score(value) -> str:
    """Formats a 0-100 score. Returns blank if empty."""
    try:
        return str(int(float(value))) if value not in (None, "") else ""
    except (ValueError, TypeError):
        return ""


def safe_float(value, default: float = 0.0) -> float:
    """Safely converts a value to float, returning default on failure."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value, default: int = 0) -> int:
    """Safely converts a value to int, returning default on failure."""
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default
