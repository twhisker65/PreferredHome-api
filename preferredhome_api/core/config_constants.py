# =============================================================
# config.py — Apartment Tracker Build 3
# All constants, field definitions, and dropdown options.
# This file is imported by every other file in the app.
# =============================================================

# -------------------------------------------------------------------
# GOOGLE SHEETS SETTINGS
# -------------------------------------------------------------------
SPREADSHEET_NAME = "Apartment Listings"

# Tab names inside Google Sheets
TAB_LISTINGS  = "listings"
TAB_BASELINE  = "baseline"
TAB_CATEGORIES = "categories"

# -------------------------------------------------------------------
# STATUS OPTIONS
# -------------------------------------------------------------------
STATUS_OPTIONS = [
    "Available",
    "Inquired",
    "Visited",
    "Applied",
    "Rejected",
    "No Longer Available",
    "Not Interested",
    "Signed",
]

# Color for each status — used by the pill badge component
STATUS_COLORS = {
    "Available":           "#28a745",   # Green
    "Inquired":            "#007bff",   # Blue
    "Visited":             "#003d99",   # Dark Blue
    "Applied":             "#fd7e14",   # Orange
    "Rejected":            "#dc3545",   # Red
    "Not Interested":      "#6c757d",   # Gray
    "No Longer Available": "#343a40",   # Dark Gray
    "Signed":              "#6f42c1",   # Purple
}

STATUS_TEXT_COLORS = {
    "Available":           "#ffffff",
    "Inquired":            "#ffffff",
    "Visited":             "#ffffff",
    "Applied":             "#ffffff",
    "Rejected":            "#ffffff",
    "Not Interested":      "#ffffff",
    "No Longer Available": "#ffffff",
    "Signed":              "#ffffff",
}

# -------------------------------------------------------------------
# DROPDOWN OPTIONS
# -------------------------------------------------------------------
UNIT_TYPE_OPTIONS  = ["Rental", "Condo", "Co-Op"]
AC_TYPE_OPTIONS    = ["Central", "Wall", "Window", "None"]
LAUNDRY_OPTIONS    = ["In-Unit", "On Floor", "In Building", "None"]
PARKING_OPTIONS    = ["Covered", "Uncovered", "None"]

# Listing sites — auto-detected from URL, or selected manually
LISTING_SITE_OPTIONS = [
    "Zillow",
    "StreetEasy",
    "Apartments.com",
    "Realtor.com",
    "Trulia",
    "Compass",
    "Other",
]

# URL keywords used for auto-detection of listing site
LISTING_SITE_URL_KEYWORDS = {
    "zillow.com":       "Zillow",
    "streeteasy.com":   "StreetEasy",
    "apartments.com":   "Apartments.com",
    "realtor.com":      "Realtor.com",
    "trulia.com":       "Trulia",
    "compass.com":      "Compass",
}

# -------------------------------------------------------------------
# PROFILE TOGGLES
# When a toggle is Off, the associated fields are hidden everywhere.
# -------------------------------------------------------------------
PROFILE_TOGGLES = {
    "children": {
        "label":   "Children",
        "default": False,
        "description": "Show school ratings and information",
    },
    "pets": {
        "label":   "Pets",
        "default": False,
        "description": "Show pet amenities category",
    },
    "car": {
        "label":   "Car",
        "default": False,
        "description": "Show parking type and parking fee",
    },
}

# -------------------------------------------------------------------
# BASELINE SETTINGS
# These are the settings stored in the "baseline" tab.
# Each key matches the "Setting" column value in Google Sheets.
# -------------------------------------------------------------------
BASELINE_SETTINGS = [
    "Max Monthly Rent",
    "Min Square Footage",
    "Max Commute Time",
    "Min Walk Score",
    "AC Type Ranking",
    "Laundry Ranking",
    "Parking Ranking",
    "Board Approval Required",
    "Broker Fee Acceptable",
]

BASELINE_DEFAULTS = {
    "Max Monthly Rent":       "2500",
    "Min Square Footage":     "700",
    "Max Commute Time":       "30",
    "Min Walk Score":         "70",
    "AC Type Ranking":        "Central,Wall,Window,None",
    "Laundry Ranking":        "In-Unit,On Floor,In Building,None",
    "Parking Ranking":        "Covered,Uncovered,None",
    "Board Approval Required":"False",
    "Broker Fee Acceptable":  "False",
}

# -------------------------------------------------------------------
# MULTI-SELECT CATEGORY DEFINITIONS
# Pre-built options for each category.
# Users can also add their own custom items via the Profile page.
# -------------------------------------------------------------------
CATEGORY_DEFINITIONS = {
    "Utilities Included": [
        "Gas", "Electric", "Internet", "Water", "Sewage", "Trash", "Parking"
    ],
    "Unit Features": [
        "Hardwood Floors", "Air Conditioning", "Dishwasher",
        "Microwave", "Balcony/Terrace"
    ],
    "Building Amenities": [
        "Extra Storage", "Rooftop Space", "Common Lounge",
        "Barbecue Area", "Firepits", "Gym", "Pool"
    ],
    "Pet Amenities": [
        "Pet Washing", "Dog Park"
    ],
    "Close By": [
        "Subway", "Bus Stop", "Grocery Store", "Park",
        "Restaurants", "Pharmacy", "Coffee Shop", "Gym", "School"
    ],
}

# Which categories are gated by a profile toggle
CATEGORY_TOGGLE_GATE = {
    "Pet Amenities": "pets",
}

# -------------------------------------------------------------------
# LISTINGS TAB — COLUMN ORDER
# This must exactly match the column headers in Google Sheets.
# -------------------------------------------------------------------
LISTINGS_COLUMNS = [
    # Status & ID
    "ID",
    "Status",
    "Preferred",
    "Listing Site",
    "Listing URL",
    "Photo URL",
    # Location
    "Building Name",
    "Street Address",
    "Zip Code",
    "City",
    "State",
    "Neighborhood",
    "Unit #",
    "Floor",
    "Top Floor",
    "Corner Unit",
    # Unit Details
    "Unit Type",
    "Bedrooms",
    "Bathrooms",
    "Square Footage",
    "Furnished",
    "Lease Length",
    "Date Available",
    "AC Type",
    "Laundry",
    "Parking Type",
    # Contact
    "Contact Name",
    "Contact Phone",
    "Contact Email",
    "Board Approval",
    "Broker Fee",
    # Timeline
    "Contacted Date",
    "Viewing Appointment",
    "Applied Date",
    # Costs
    "Monthly Rent",
    "Parking Fee",
    "Amenity Fee",
    "Admin Fee",
    "Utility Fee",
    "Other Fee",
    "Total Monthly",
    "Security Deposit",
    "Application Fee",
    # Transportation
    "Commute Time",
    "Walk Score",
    "Transit Score",
    "Bike Score",
    # Categories (stored as comma-separated text)
    "Utilities Included",
    "Unit Features",
    "Building Amenities",
    "Pet Amenities",
    "Close By",
    # Schools
    "Elementary School Name",
    "Elementary School Rating",
    "Elementary School Grades",
    "Elementary School Distance",
    "Middle School Name",
    "Middle School Rating",
    "Middle School Grades",
    "Middle School Distance",
    "High School Name",
    "High School Rating",
    "High School Grades",
    "High School Distance",
    # Notes
    "Pros",
    "Cons",
]

# -------------------------------------------------------------------
# FIELD TYPE CLASSIFICATIONS
# -------------------------------------------------------------------

# Fields that store True/False values
BOOLEAN_FIELDS = [
    "Preferred",
    "Top Floor",
    "Corner Unit",
    "Furnished",
    "Board Approval",
    "Broker Fee",
]

# Fields that store numbers
NUMERIC_FIELDS = [
    "Floor",
    "Bedrooms",
    "Bathrooms",
    "Square Footage",
    "Monthly Rent",
    "Parking Fee",
    "Amenity Fee",
    "Admin Fee",
    "Utility Fee",
    "Other Fee",
    "Total Monthly",
    "Security Deposit",
    "Application Fee",
    "Commute Time",
    "Walk Score",
    "Transit Score",
    "Bike Score",
    "Elementary School Rating",
    "Elementary School Distance",
    "Middle School Rating",
    "Middle School Distance",
    "High School Rating",
    "High School Distance",
]

# Fields that are dropdown selections
DROPDOWN_FIELDS = [
    "Status",
    "Unit Type",
    "AC Type",
    "Laundry",
    "Parking Type",
    "Listing Site",
]

# Fields that store comma-separated category lists
CATEGORY_FIELDS = [
    "Utilities Included",
    "Unit Features",
    "Building Amenities",
    "Pet Amenities",
    "Close By",
]

# Fields that are profile-gated (hidden when toggle is Off)
CHILDREN_GATED_FIELDS = [
    "Elementary School Name",
    "Elementary School Rating",
    "Elementary School Grades",
    "Elementary School Distance",
    "Middle School Name",
    "Middle School Rating",
    "Middle School Grades",
    "Middle School Distance",
    "High School Name",
    "High School Rating",
    "High School Grades",
    "High School Distance",
]

CAR_GATED_FIELDS = [
    "Parking Type",
    "Parking Fee",
]

PETS_GATED_FIELDS = [
    "Pet Amenities",
]

# Fields used in baseline comparison (color-coded on Compare page)
BASELINE_COMPARED_FIELDS = [
    "Monthly Rent",
    "Square Footage",
    "Commute Time",
    "Walk Score",
    "AC Type",
    "Laundry",
    "Parking Type",
    "Board Approval",
    "Broker Fee",
]

# Fields that display on listing cards
CARD_FIELDS = [
    "Building Name",
    "Street Address",
    "Neighborhood",
    "Monthly Rent",
    "Total Monthly",
    "Bedrooms",
    "Bathrooms",
    "Square Footage",
    "Unit Type",
    "Floor",
    "Corner Unit",
    "Top Floor",
    "Listing Site",
    "Status",
    "Preferred",
    "Photo URL",
    "Listing URL",
    "Parking Fee",
    "Amenity Fee",
    "Admin Fee",
    "Utility Fee",
    "Other Fee",
]

# -------------------------------------------------------------------
# COMPARISON COLOR THRESHOLDS
# Used on the Compare page to color-code field values.
# -------------------------------------------------------------------
COMPARISON_COLORS = {
    "green":  "#28a745",
    "yellow": "#ffc107",
    "red":    "#dc3545",
    "gray":   "#6c757d",    # for fields with no baseline
}

# -------------------------------------------------------------------
# APP DISPLAY SETTINGS
# -------------------------------------------------------------------
APP_TITLE   = "Apartment Tracker"
APP_ICON    = "🏠"
NAV_PAGES   = ["Home", "Listings", "Add", "Compare", "Profile"]
NAV_ICONS   = ["🏠", "🏢", "➕", "⚖️", "👤"]
