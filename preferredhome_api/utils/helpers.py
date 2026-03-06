# =============================================================
# helpers.py — PreferredHome API Build 3.1.15.5
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
    "110": ("Queens", "NY"),      "111": ("Queens", "NY"),
    "112": ("Brooklyn", "NY"),    "113": ("Queens", "NY"),
    "114": ("Queens", "NY"),      "115": ("Queens", "NY"),
    "116": ("Queens", "NY"),      "117": ("Long Island", "NY"),
    "118": ("Long Island", "NY"), "119": ("Long Island", "NY"),
    "200": ("Washington", "DC"),  "201": ("Washington", "DC"),
    "202": ("Washington", "DC"),  "203": ("Washington", "DC"),
    "204": ("Washington", "DC"),  "205": ("Washington", "DC"),
    "300": ("Atlanta", "GA"),     "301": ("Atlanta", "GA"),
    "302": ("Atlanta", "GA"),     "303": ("Atlanta", "GA"),
    "330": ("Miami", "FL"),       "331": ("Miami", "FL"),
    "332": ("Miami", "FL"),       "333": ("Fort Lauderdale", "FL"),
    "600": ("Chicago", "IL"),     "601": ("Chicago", "IL"),
    "602": ("Chicago", "IL"),
    "900": ("Los Angeles", "CA"), "901": ("Los Angeles", "CA"),
    "902": ("Beverly Hills", "CA"),"903": ("Los Angeles", "CA"),
    "940": ("San Francisco", "CA"),"941": ("San Francisco", "CA"),
    "942": ("Sacramento", "CA"),
    "980": ("Seattle", "WA"),     "981": ("Seattle", "WA"),
    "770": ("Houston", "TX"),     "771": ("Houston", "TX"),
    "750": ("Dallas", "TX"),      "751": ("Dallas", "TX"),
    "850": ("Phoenix", "AZ"),     "852": ("Phoenix", "AZ"),
    "800": ("Denver", "CO"),      "801": ("Denver", "CO"),
    "021": ("Boston", "MA"),      "022": ("Boston", "MA"),
    "191": ("Philadelphia", "PA"),"190": ("Philadelphia", "PA"),
    "481": ("Detroit", "MI"),     "482": ("Detroit", "MI"),
    "430": ("Columbus", "OH"),    "441": ("Cleveland", "OH"),
    "971": ("Portland", "OR"),    "972": ("Portland", "OR"),
    "891": ("Las Vegas", "NV"),   "890": ("Las Vegas", "NV"),
    "372": ("Nashville", "TN"),
    "282": ("Charlotte", "NC"),   "277": ("Raleigh", "NC"),
    "700": ("New Orleans", "LA"), "701": ("New Orleans", "LA"),
    "531": ("Milwaukee", "WI"),   "530": ("Milwaukee", "WI"),
    "550": ("Minneapolis", "MN"), "551": ("Minneapolis", "MN"),
    "680": ("Omaha", "NE"),       "681": ("Omaha", "NE"),
    "720": ("Oklahoma City", "OK"),
    "871": ("Albuquerque", "NM"), "870": ("Albuquerque", "NM"),
    "841": ("Salt Lake City", "UT"),"840": ("Salt Lake City", "UT"),
    "967": ("Honolulu", "HI"),    "968": ("Honolulu", "HI"),
    "995": ("Anchorage", "AK"),   "994": ("Anchorage", "AK"),
}

def lookup_city_state(zip_code: str) -> tuple:
    if not zip_code or len(str(zip_code)) < 3:
        return ("", "")
    prefix = str(zip_code)[:3]
    return ZIP_STATE_MAP.get(prefix, ("", ""))


# -------------------------------------------------------------------
# FEE CALCULATION (camelCase field names)
# -------------------------------------------------------------------

def calculate_total_monthly(row: dict) -> float:
    """
    Calculates total monthly cost from all fee fields.
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
    Parses a raw row from Google Sheets into Python types.
    Uses camelCase keys matching LISTINGS_COLUMNS.
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

def get_comparison_color(field: str, value, baseline: dict) -> str:
    """
    Returns "green", "yellow", "red", or "gray" for a field value
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


def _ranked_color(value: str, ranking_str: str) -> str:
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
    try:
        return f"${float(value):,.0f}" if value not in (None, "", 0) else ""
    except (ValueError, TypeError):
        return ""

def format_number(value, decimals: int = 0) -> str:
    try:
        if value in (None, ""):
            return ""
        return f"{float(value):,.{decimals}f}"
    except (ValueError, TypeError):
        return ""

def format_score(value) -> str:
    try:
        return str(int(float(value))) if value not in (None, "") else ""
    except (ValueError, TypeError):
        return ""

def safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default: int = 0) -> int:
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default
