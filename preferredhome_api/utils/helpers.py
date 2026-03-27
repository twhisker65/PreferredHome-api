# =============================================================
# helpers.py — PreferredHome API Build 3.2.15
# Changes from 3.2.11:
# - Added os, requests, datetime imports for commute calculation.
# - Added _get_next_monday_timestamp() — converts a time string to
#   next Monday Unix timestamp for Google Maps departure_time param.
# - Added calculate_commute_time() — calls Google Maps Distance
#   Matrix API and returns commute duration in minutes or None.
# All existing functions unchanged.
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


# -------------------------------------------------------------------
# COMMUTE CALCULATION — Build 3.2.15
# -------------------------------------------------------------------

def _get_next_monday_timestamp(time_str: str) -> int:
    """
    Returns a Unix timestamp for the next upcoming Monday at the given time.
    time_str format: "8:30 AM" or "11:00 PM" (matches TIME_OPTIONS in mobile).
    Defaults to Monday 8:00 AM if blank or unparseable.
    Always returns a future timestamp — never today even if today is Monday.
    """
    now = datetime.now()
    # days_ahead: positive number of days until next Monday
    days_ahead = (7 - now.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7  # if today is Monday, use next Monday
    next_monday = now + timedelta(days=days_ahead)

    hour, minute = 8, 0  # default
    if time_str and time_str.strip():
        for fmt in ("%I:%M %p", "%I:%M%p"):
            try:
                t = datetime.strptime(time_str.strip().upper(), fmt.upper())
                hour, minute = t.hour, t.minute
                break
            except ValueError:
                continue

    next_monday = next_monday.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return int(next_monday.timestamp())


def calculate_commute_time(
    work_address: str,
    listing_address: str,
    commute_method: str,
    departure_time: str,
) -> int | None:
    """
    Calls Google Maps Distance Matrix API to calculate commute duration.
    Returns integer minutes, or None if the call fails or address is invalid.

    commute_method: "Walk" | "Drive" | "Transit" | "Bike"
    departure_time: time string like "8:30 AM", or "" to use default Monday 8 AM
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    if not api_key:
        return None

    mode_map = {
        "Drive":   "driving",
        "Walk":    "walking",
        "Transit": "transit",
        "Bike":    "bicycling",
    }
    google_mode = mode_map.get(commute_method, "transit")

    params: dict = {
        "origins":      work_address,
        "destinations": listing_address,
        "mode":         google_mode,
        "key":          api_key,
    }

    # Departure time applies to driving (traffic) and transit (schedule).
    # Walk and Bike ignore it per Google Maps API behaviour.
    if google_mode in ("driving", "transit"):
        params["departure_time"] = _get_next_monday_timestamp(departure_time)

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
        # Use duration_in_traffic when available (driving with traffic model)
        dur = element.get("duration_in_traffic") or element.get("duration")
        if not dur:
            return None
        return round(dur["value"] / 60)  # seconds → minutes
    except Exception:
        return None
