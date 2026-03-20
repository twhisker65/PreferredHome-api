BUILD 3.2.11A — API Data Model Update
Repo: twhisker65/PreferredHome-api
Branch: MAIN

CHANGED FILES
-------------
preferredhome_api/core/config_constants.py
preferredhome_api/utils/helpers.py

UNCHANGED FILES (Do Not Touch)
-------------------------------
main.py
preferredhome_api/storage/sheets_storage.py
preferredhome_api/core/models.py
preferredhome_api/core/settings.py
All other files in the repo

WHAT CHANGED
------------

config_constants.py
  - LISTINGS_COLUMNS: unitType renamed to propertyType; acType renamed to coolingType;
    11 new fields added at end: numberOfFloors, heatingType, shortTermAvailable,
    rentersInsuranceRequired, petFee, storageRent, brokerFee, moveInFee,
    privateOutdoorSpaceTypes, storageTypes, roomTypes
  - BOOLEAN_FIELDS: added shortTermAvailable, rentersInsuranceRequired
  - NUMERIC_FIELDS: added numberOfFloors, petFee, storageRent, brokerFee, moveInFee
  - DROPDOWN_FIELDS: unitType/acType removed; propertyType, coolingType, heatingType,
    numberOfFloors added
  - CATEGORY_FIELDS: added privateOutdoorSpaceTypes, storageTypes, roomTypes
  - CATEGORY_DEFINITIONS: full replacement with expanded option lists
  - CARD_FIELDS: unitType renamed to propertyType
  - BASELINE_COMPARED_FIELDS: acType renamed to coolingType
  - Dropdown constants: UNIT_TYPE_OPTIONS replaced by PROPERTY_TYPE_OPTIONS;
    AC_TYPE_OPTIONS replaced by COOLING_TYPE_OPTIONS; HEATING_TYPE_OPTIONS added;
    PARKING_OPTIONS updated; NUMBER_OF_FLOORS_OPTIONS added

helpers.py (Option A — surgical import fix)
  - Import: AC_TYPE_OPTIONS renamed to COOLING_TYPE_OPTIONS
  - get_comparison_color(): field check "acType" renamed to "coolingType";
    AC_TYPE_OPTIONS reference renamed to COOLING_TYPE_OPTIONS

DEPLOY STEPS
------------
1. Copy both changed files into your local PreferredHome-api repo at the exact paths shown above
2. Commit via GitHub Desktop using the commit message below
3. Push to GitHub
4. Render dashboard → Manual Deploy → Deploy latest commit
5. Wait ~60 seconds for green Live status

VERIFY
------
6. Open https://preferredhome-api.onrender.com/health — confirm healthy response
7. Open https://preferredhome-api.onrender.com/listings — confirm listings return without error
8. Open the app in Expo Go — confirm existing listings display correctly

COMMIT MESSAGE
--------------
Build 3.2.11A — API data model update: property type expansion, 11 new fields, rename unitType/acType

EXPO RESTART (Part B only — not needed for Part A)
--------------
cd C:\Users\twhis\OneDrive\Documents\GitHub\PreferredHome-mobile
npx expo start --tunnel --clear
