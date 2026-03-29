# =============================================================
# config_constants.py — PreferredHome API Build 3.2.17
# Based on Build 3.2.14 / 3.2.15 / 3.2.16.
# Build 3.2.17: safetyScore and noiseScore added to LISTINGS_COLUMNS
# and NUMERIC_FIELDS. No other changes.
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
PROPERTY_TYPE_OPTIONS    = ["Apartment", "Condo", "Co-op", "Townhouse", "House", "Other"]
COOLING_TYPE_OPTIONS     = ["Central Air", "Wall Unit", "Window Unit", "None"]
HEATING_TYPE_OPTIONS     = ["Forced Air", "Baseboard", "Radiant", "Steam", "Electric", "Natural Gas", "Oil", "Propane", "None"]
LAUNDRY_OPTIONS          = ["In-Unit", "On Floor", "In Building", "None"]
PARKING_OPTIONS          = ["Shared Garage", "Shared Lot", "Covered Space", "Attached Garage", "Detached Garage", "Driveway", "Carport", "Street", "None", "Other"]
NUMBER_OF_FLOORS_OPTIONS = ["1", "2", "3", "4", "5+", "Unknown"]

# Listing sites — updated Build 3.2.14 (13-item list, matches mobile exactly)
LISTING_SITE_OPTIONS = [
    "Zillow",
    "Realtor.com",
    "Redfin",
    "Homes.com",
    "Apartments.com",
    "StreetEasy",
    "HotPads",
    "Trulia",
    "Rent.com",
    "Apartment Finder",
    "Rentals.com",
    "MLS / Broker",
    "Other",
]

# URL keywords for server-side listing site auto-detection — updated Build 3.2.14
# Checked in order — first match wins.
LISTING_SITE_URL_KEYWORDS = {
    "zillow.com":          "Zillow",
    "realtor.com":         "Realtor.com",
    "redfin.com":          "Redfin",
    "homes.com":           "Homes.com",
    "apartments.com":      "Apartments.com",
    "streeteasy.com":      "StreetEasy",
    "hotpads.com":         "HotPads",
    "trulia.com":          "Trulia",
    "rent.com":            "Rent.com",
    "apartmentfinder.com": "Apartment Finder",
    "rentals.com":         "Rentals.com",
    "mls":                 "MLS / Broker",
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
    # Transportation / Neighborhood scores
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
    # New fields — Build 3.2.17
    "safetyScore",
    "noiseScore",
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
    "safetyScore",
    "noiseScore",
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
    "status",
    "preferred",
    "id",
]

# -------------------------------------------------------------------
# BASELINE DEFAULTS — used when no baseline entry exists in the sheet
# -------------------------------------------------------------------
BASELINE_DEFAULTS = {
    "baseRent":      0,
    "squareFootage": 0,
    "commuteTime":   0,
    "walkScore":     0,
    "coolingType":   "None",
    "laundry":       "None",
    "parkingType":   "None",
    "noBoardApproval": False,
    "noBrokerFee":     False,
}
