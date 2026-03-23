# =============================================================
# config_constants.py — PreferredHome API Build 3.2.13.1
# Based on Build 3.2.11 original — identical except:
#   1. "totalUpfront" added to LISTINGS_COLUMNS (after "totalMonthly")
#   2. "totalUpfront" added to NUMERIC_FIELDS
# No other changes. PARKING_OPTIONS unchanged.
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

STATUS_COLORS = {
    "New":        "#2563EB",
    "Contacted":  "#2563EB",
    "Scheduled":  "#2563EB",
    "Viewed":     "#2563EB",
    "Shortlisted":"#D97706",
    "Applied":    "#2563EB",
    "Approved":   "#10B981",
    "Signed":     "#0D9488",
    "Rejected":   "#EF4444",
    "Archived":   "#475569",
    "Unknown":    "#475569",
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
PROPERTY_TYPE_OPTIONS = ["Apartment", "Condo", "Co-op", "Townhouse", "House", "Other"]
COOLING_TYPE_OPTIONS  = ["Central Air", "Wall Unit", "Window Unit", "None"]
HEATING_TYPE_OPTIONS  = ["Forced Air", "Baseboard", "Radiant", "Steam", "Electric", "Natural Gas", "Oil", "Propane", "None"]
LAUNDRY_OPTIONS       = ["In-Unit", "On Floor", "In Building", "None"]
PARKING_OPTIONS       = ["Shared Garage", "Shared Lot", "Covered Space", "Attached Garage", "Detached Garage", "Driveway", "Carport", "Street", "None", "Other"]
NUMBER_OF_FLOORS_OPTIONS = ["1", "2", "3", "4", "5+", "Unknown"]

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
# LISTINGS COLUMNS (camelCase — matches Google Sheet column headers)
# -------------------------------------------------------------------
LISTINGS_COLUMNS = [
    # Status & ID
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
    # Property Details
    "propertyType",
    "bedrooms",
    "bathrooms",
    "squareFootage",
    "furnished",
    "leaseLength",
    "dateAvailable",
    "coolingType",
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
    "totalUpfront",
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
    # New fields — Build 3.2.11
    "numberOfFloors",
    "heatingType",
    "shortTermAvailable",
    "rentersInsuranceRequired",
    "petFee",
    "storageRent",
    "brokerFee",
    "moveInFee",
    "privateOutdoorSpaceTypes",
    "storageTypes",
    "roomTypes",
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
    "shortTermAvailable",
    "rentersInsuranceRequired",
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
    "totalUpfront",
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
    "numberOfFloors",
    "petFee",
    "storageRent",
    "brokerFee",
    "moveInFee",
]

DROPDOWN_FIELDS = [
    "status",
    "propertyType",
    "coolingType",
    "heatingType",
    "numberOfFloors",
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
    "privateOutdoorSpaceTypes",
    "storageTypes",
    "roomTypes",
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

BASELINE_COMPARED_FIELDS = [
    "baseRent",
    "squareFootage",
    "commuteTime",
    "walkScore",
    "coolingType",
    "laundry",
    "parkingType",
    "noBoardApproval",
    "noBrokerFee",
]

CARD_FIELDS = [
    "buildingName",
    "streetAddress",
    "neighborhood",
    "baseRent",
    "totalMonthly",
    "bedrooms",
    "bathrooms",
    "squareFootage",
    "propertyType",
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
