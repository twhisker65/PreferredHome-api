PreferredHome — Build 3.2.14
============================
Listing Site auto-detect from URL + new 13-item Listing Sites list
Generated: March 2026

CHANGED FILES
-------------
Mobile repo:
  lib/api.ts                    — detectListingSite() function added
  app/(tabs)/add.tsx            — LISTING_SITES updated, useEffect for listingUrl added
  app/edit.tsx                  — LISTING_SITES updated, useEffect for listingUrl added, detectListingSite imported

API repo:
  preferredhome_api/core/config_constants.py  — LISTING_SITE_OPTIONS and LISTING_SITE_URL_KEYWORDS updated

WHAT CHANGED IN THIS BUILD
---------------------------

1. lib/api.ts
   - Added detectListingSite(url: string): string
     Pure client-side URL pattern match. No network call. Returns site name on match, "Other" on no match.
     Patterns checked in order: zillow.com, realtor.com, redfin.com, homes.com, apartments.com,
     streeteasy.com, hotpads.com, trulia.com, rent.com, apartmentfinder.com, rentals.com, mls.
   - All existing functions (getHealth, getListings, postListing, updateListing, deleteListing, lookupZip) unchanged.

2. app/(tabs)/add.tsx
   - Import updated: detectListingSite added alongside postListing and lookupZip.
   - LISTING_SITES array replaced: new 13-item list.
   - useEffect added (watches draft.listingUrl):
     Fires on every change to Listing URL field.
     Sets draft.listingSite to the auto-detected value.
     No guard — fires even on empty URL (returns "Other").

3. app/edit.tsx
   - Import updated: detectListingSite added alongside getListings and updateListing.
   - LISTING_SITES array replaced: new 13-item list.
   - useEffect added (watches draft?.listingUrl):
     Guard: only fires if draft is loaded AND listingUrl is non-empty.
     Prevents overriding a stored listingSite when a listing without a URL is opened.
     Sets draft.listingSite to the auto-detected value.

4. preferredhome_api/core/config_constants.py
   - LISTING_SITE_OPTIONS: replaced with new 13-item list.
   - LISTING_SITE_URL_KEYWORDS: replaced with new 13-item patterns.
   - Constant names NOT changed — helpers.py imports LISTING_SITE_URL_KEYWORDS by name. Safe.
   - All other constants unchanged.

NEW LISTING SITES LIST (13 items — mobile and API now match exactly)
----------------------------------------------------------------------
  Zillow
  Realtor.com
  Redfin
  Homes.com
  Apartments.com
  StreetEasy
  HotPads
  Trulia
  Rent.com
  Apartment Finder
  Rentals.com
  MLS / Broker
  Other

DEPLOY STEPS — MOBILE
----------------------
1. Copy these 3 files into your PreferredHome-mobile repo (overwrite existing):
     lib/api.ts
     app/(tabs)/add.tsx
     app/edit.tsx
2. Commit in GitHub Desktop using the commit message below.
3. Push to GitHub.
4. Restart Expo using the command below.
5. Test on your physical device using the test checklist.

DEPLOY STEPS — API
-------------------
1. Copy this 1 file into your PreferredHome-api repo (overwrite existing):
     preferredhome_api/core/config_constants.py
2. Commit in GitHub Desktop using the commit message below.
3. Push to GitHub.
4. In Render: click "Deploy latest commit" — do NOT use Restart.
5. Wait ~60 seconds.
6. Verify at https://preferredhome-api.onrender.com/health

COMMIT MESSAGE — MOBILE
-----------------------
Build 3.2.14 - Listing Site auto-detect from URL, new 13-item listing sites list

COMMIT MESSAGE — API
--------------------
Build 3.2.14 - LISTING_SITE_OPTIONS and URL_KEYWORDS updated to 13-item list

EXPO RESTART COMMAND
--------------------
cd C:\Users\twhis\OneDrive\Documents\GitHub\PreferredHome-mobile && npx expo start --tunnel --clear

TEST CHECKLIST — BUILD 3.2.14
------------------------------
[ ] T1 — Open Add screen. Listing Site dropdown shows all 13 new options.
[ ] T2 — On Add, type a Zillow URL into Listing URL. Listing Site auto-changes to "Zillow".
[ ] T3 — On Add, type a StreetEasy URL. Listing Site auto-changes to "StreetEasy".
[ ] T4 — On Add, type a URL containing "mls". Listing Site auto-changes to "MLS / Broker".
[ ] T5 — On Add, type an unrecognized URL. Listing Site stays as "Other".
[ ] T6 — On Add, paste a URL, then manually override Listing Site. Manual selection sticks.
[ ] T7 — Open Edit screen on any listing. Listing Site dropdown shows all 13 new options.
[ ] T8 — On Edit, change Listing URL to a Realtor.com URL. Listing Site auto-changes to "Realtor.com".
