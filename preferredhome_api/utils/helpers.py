# =============================================================
# helpers.py — PreferredHome API Build 3.2.15
# Added: calculate_commute() via Google Maps Distance Matrix API
# =============================================================

import os
import uuid
import requests
from datetime import datetime, timedelta

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
# COMMUTE CALCULATION — Google Maps Distance Matrix API
# -------------------------------------------------------------------

_COMMUTE_MODE_MAP = {
    "Drive":   "driving",
    "Transit": "transit",
    "Walk":    "walking",
    "Bike":    "bicycling",
}


def _next_monday_timestamp(departure_time: str) -> int:
    """
    Returns a Unix timestamp for the next Monday at departure_time.
    departure_time format: "8:00 AM", "9:30 AM", etc.
    Defaults to 8:00 AM if blank or unparseable.
    Always uses Monday — not today — so traffic reflects a real commute.
    """
    now = datetime.now()
    # Days until next Monday (weekday 0). If today is Monday, use next Monday.
    days_until = (7 - now.weekday()) % 7
    if days_until == 0:
        days_until = 7
    next_monday = now + timedelta(days=days_until)

    hour, minute = 8, 0
    if departure_time:
        try:
            t = datetime.strptime(departure_time.strip(), "%I:%M %p")
            hour, minute = t.hour, t.minute
        except ValueError:
            pass

    target = next_monday.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return int(target.timestamp())


def calculate_commute(
    listing_address: str,
    work_address: str,
    commute_method: str,
    departure_time: str,
) -> int | None:
    """
    Calls Google Maps Distance Matrix API.
    Returns commute time in integer minutes, or None on any failure.
    Silently skips if GOOGLE_MAPS_API_KEY is not set.
    Origin = work_address, Destination = listing_address.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()
    if not api_key:
        return None

    if not listing_address or not work_address:
        return None

    mode = _COMMUTE_MODE_MAP.get(commute_method, "transit")

    params: dict = {
        "origins":      work_address,
        "destinations": listing_address,
        "mode":         mode,
        "key":          api_key,
    }

    # Driving and transit benefit from departure_time for traffic accuracy.
    # Walk and bike ignore departure_time.
    if mode in ("driving", "transit"):
        params["departure_time"] = _next_monday_timestamp(departure_time)

    try:
        resp = requests.get(
            "https://maps.googleapis.com/maps/api/distancematrix/json",
            params=params,
            timeout=10,
        )
        data = resp.json()
        element = data["rows"][0]["elements"][0]
        if element.get("status") != "OK":
            return None
        # Prefer duration_in_traffic for driving (real traffic estimate).
        if "duration_in_traffic" in element:
            seconds = element["duration_in_traffic"]["value"]
        else:
            seconds = element["duration"]["value"]
        return max(1, round(seconds / 60))
    except Exception:
        return None


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
            if isinstance(value, bool):
                cleaned[key] = "TRUE" if value else "FALSE"
            elif str(value).strip().upper() in ("TRUE", "1", "YES"):
                cleaned[key] = "TRUE"
            else:
                cleaned[key] = "FALSE"
        elif key in NUMERIC_FIELDS:
            if value in (None, "", "null", "nan"):
                cleaned[key] = ""
            else:
                try:
                    cleaned[key] = float(str(value))
                except (ValueError, TypeError):
                    cleaned[key] = ""
        elif key in CATEGORY_FIELDS:
            if isinstance(value, list):
                cleaned[key] = ", ".join(str(v) for v in value)
            else:
                cleaned[key] = str(value) if value is not None else ""
        else:
            cleaned[key] = str(value) if value is not None else ""
    return cleaned


def parse_row(row: dict) -> dict:
    """
    Parses a row from Google Sheets into Python types.
    Uses camelCase keys matching LISTINGS_COLUMNS.
    """
    parsed = {}
    for key, value in row.items():
        if key in BOOLEAN_FIELDS:
            parsed[key] = str(value).strip().upper() in ("TRUE", "1", "YES")
        elif key in NUMERIC_FIELDS:
            if value in (None, ""):
                parsed[key] = None
            else:
                try:
                    parsed[key] = float(str(value))
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
            parsed[key] = str(value) if value is not None else ""
    return parsed
