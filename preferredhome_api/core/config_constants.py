# =============================================================
# config_constants.py — PreferredHome API Build 3.1.15.5
# Single source of truth for all constants, field definitions,
# dropdown options, and column names.
# =============================================================

# -------------------------------------------------------------------
# GOOGLE SHEETS SETTINGS
# -------------------------------------------------------------------
SPREADSHEET_NAME = "Apartment Listings"

TAB_LISTINGS   = "listings"
TAB_BASELINE   = "baseline"
TAB_CATEGORIES = "categories"

# -------------------------------------------------------------------
# STATUS OPTIONS — 10-status pipeline (matches mobile exactly)
# -------------------------------------------------------------------
STATUS_OPTIONS = [
    "New",
    "Contacted",
    "Scheduled",
    "Viewed",
    "Shortlisted",
    "Applied",
    "Approved",
    "Signed",
    "Rejected",
    "Archived",
]

# Background color for each status pill (matches mobile colors.ts)
STATUS_COLORS = {
    "New":        "#2563EB",   # blue
    "Contacted":  "#2563EB",   # blue
    "Scheduled":  "#2563EB",   # blue
    "Viewed":     "#2563EB",   # blue
    "Shortlisted":"#D97706",   # amber
    "Applied":    "#2563EB",   # blue
    "Approved":   "#10B981",   # green
    "Signed":     "#0D9488",   # teal
    "Rejected":   "#EF4444",   # red
    "Archived":   "#475569",   # grey
    "Unknown":    "#475569",   # grey
}

STATUS_TEXT_COLORS = {
    "New":        "#ffffff",
    "Contacted":  "#ffffff",
    "Scheduled":  "#ffffff",
    "Viewed":     "#ffffff",
    "Shortlisted":"#ffffff",
    "Applied":    "#ffffff",
    "Approved":   "#ffffff",
    "Signed":     "#ffffff",
    "Rejected":   "#ffffff",
    "Archived":   "#ffffff",
    "Unknown":    "#ffffff",
}

# -------------------------------------------------------------------
# DROPDOWN OPTIONS
# -------------------------------------------------------------------
UNIT_TYPE_OPTIONS = ["Rental", "Condo", "Co-Op"]
AC_TYPE_OPTIONS   = ["Central", "Wall", "Window", "None"]
LAUNDRY_OPTIONS   = ["In-Unit", "On Floor", "In Building", "None"]
PARKING_OPTIONS   = ["Covered", "Uncovered", "None"]

LISTING_SITE_OPTIONS = [
    "Zillow",
    "StreetEasy",
    "Apartments.com",
    "Realtor.com",
    "Trulia",
    "Compass",
    "Other",
]

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
# -------------------------------------------------------------------
PROFILE_TOGGLES = {
    "children": {
        "label":       "Children",
        "default":     False,
        "description": "Show school ratings and information",
    },
    "pets": {
        "label":       "Pets",
        "default":     False,
        "description": "Show pet amenities category",
    },
    "car": {
        "label":       "Car",
        "default":     False,
        "description": "Show parking type and parking fee",
    },
}

# -------------------------------------------------------------------
# BASELINE SETTINGS
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
    "Max Monthly Rent":        "2500",
    "Min Square Footage":      "700",
    "Max Commute Time":        "30",
    "Min Walk Score":          "70",
    "AC Type Ranking":         "Central,Wall,Window,None",
    "Laundry Ranking":         "In-Unit,On Floor,In Building,None",
    "Parking Ranking":         "Covered,Uncovered,None",
    "Board Approval Required": "False",
    "Broker Fee Acceptable":   "False",
}

# -------------------------------------------------------------------
# MULTI-SELECT CATEGORY DEFINITIONS
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

CATEGORY_TOGGLE_GATE = {
    "Pet Amenities": "pets",
}

# -------------------------------------------------------------------
# LISTINGS TAB — COLUMN ORDER (camelCase — matches Google Sheet headers)
# -------------------------------------------------------------------
LISTINGS_COLUMNS = [
    # Identity
    "id",
    "status",
    "preferred",
    "listingSite",
    "listingUrl",
    "photoUrl",
    # Location
    "buildingName",
    "streetAddress",
    "zipCode",
    "city",
    "state",
    "neighborhood",
    "unitNumber",
    "floorNumber",
    "topFloor",
    "cornerUnit",
    # Unit Details
    "unitType",
    "bedrooms",
    "bathrooms",
    "squareFootage",
    "furnished",
    "leaseLength",
    "dateAvailable",
    "acType",
    "laundry",
    "parkingType",
    # Contact
    "contactName",
    "contactPhone",
    "contactEmail",
    "noBoardApproval",
    "noBrokerFee",
    # Timeline
    "contactedDate",
    "viewingAppointment",
    "appliedDate",
    # Costs
    "baseRent",
    "parkingFee",
    "amenityFee",
    "adminFee",
    "utilityFee",
    "otherFee",
    "totalMonthly",
    "securityDeposit",
    "applicationFee",
    # Transportation
    "commuteTime",
    "walkScore",
    "transitScore",
    "bikeScore",
    # Categories (comma-separated)
    "utilitiesIncluded",
    "unitFeatures",
    "buildingAmenities",
    "petAmenities",
    "closeBy",
    # Schools
    "elementarySchoolName",
    "elementaryRating",
    "elementaryGrades",
    "elementaryDistance",
    "middleSchoolName",
    "middleRating",
    "middleGrades",
    "middleDistance",
    "highSchoolName",
    "highRating",
    "highGrades",
    "highDistance",
    # Notes
    "pros",
    "cons",
]

# -------------------------------------------------------------------
# FIELD TYPE CLASSIFICATIONS (all camelCase — matches LISTINGS_COLUMNS)
# -------------------------------------------------------------------

BOOLEAN_FIELDS = [
    "preferred",
    "topFloor",
    "cornerUnit",
    "furnished",
    "noBoardApproval",
    "noBrokerFee",
]

NUMERIC_FIELDS = [
    "floorNumber",
    "bedrooms",
    "bathrooms",
    "squareFootage",
    "baseRent",
    "parkingFee",
    "amenityFee",
    "adminFee",
    "utilityFee",
    "otherFee",
    "totalMonthly",
    "securityDeposit",
    "applicationFee",
    "commuteTime",
    "walkScore",
    "transitScore",
    "bikeScore",
    "elementaryRating",
    "elementaryDistance",
    "middleRating",
    "middleDistance",
    "highRating",
    "highDistance",
]

DROPDOWN_FIELDS = [
    "status",
    "unitType",
    "acType",
    "laundry",
    "parkingType",
    "listingSite",
]

CATEGORY_FIELDS = [
    "utilitiesIncluded",
    "unitFeatures",
    "buildingAmenities",
    "petAmenities",
    "closeBy",
]

CHILDREN_GATED_FIELDS = [
    "elementarySchoolName",
    "elementaryRating",
    "elementaryGrades",
    "elementaryDistance",
    "middleSchoolName",
    "middleRating",
    "middleGrades",
    "middleDistance",
    "highSchoolName",
    "highRating",
    "highGrades",
    "highDistance",
]

CAR_GATED_FIELDS = [
    "parkingType",
    "parkingFee",
]

PETS_GATED_FIELDS = [
    "petAmenities",
]

# Fields used in baseline comparison (Compare screen)
BASELINE_COMPARED_FIELDS = [
    "baseRent",
    "squareFootage",
    "commuteTime",
    "walkScore",
    "acType",
    "laundry",
    "parkingType",
    "noBoardApproval",
    "noBrokerFee",
]

# Fields shown on listing cards
CARD_FIELDS = [
    "buildingName",
    "streetAddress",
    "neighborhood",
    "baseRent",
    "totalMonthly",
    "bedrooms",
    "bathrooms",
    "squareFootage",
    "unitType",
    "floorNumber",
    "cornerUnit",
    "topFloor",
    "listingSite",
    "status",
    "preferred",
    "photoUrl",
    "listingUrl",
    "parkingFee",
    "amenityFee",
    "adminFee",
    "utilityFee",
    "otherFee",
]

# -------------------------------------------------------------------
# COMPARISON COLOR THRESHOLDS
# -------------------------------------------------------------------
COMPARISON_COLORS = {
    "green":  "#10B981",
    "yellow": "#D97706",
    "red":    "#EF4444",
    "gray":   "#475569",
}

# -------------------------------------------------------------------
# APP SETTINGS
# -------------------------------------------------------------------
APP_TITLE = "PreferredHome"
APP_ICON  = "🏠"
NAV_PAGES = ["Home", "Listings", "Add", "Compare", "Profile"]
NAV_ICONS = ["🏠", "🏢", "➕", "⚖️", "👤"]
