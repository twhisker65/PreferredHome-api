BUILD_3.2.2.1_HOTFIX_README
===========================
PreferredHome API — Hotfix Build 3.2.2.1
Generated: March 2026
Repo: PreferredHome-api (MAIN branch)

CHANGED FILES (in folder order)
---------------------------------
main.py

ROOT CAUSE
----------
After Build 3.2.2, the Listings, Home, and Calendar screens all showed
a load error. These three screens all call GET /listings when they open.

The listings_get() function in main.py had no try/except block. Any
exception thrown while reading from Google Sheets (corrupted data,
unexpected column format, NaN value, network blip) caused FastAPI to
return an unhandled HTTP 500 with no detail message — making it
impossible to diagnose and impossible for the app to display a
meaningful error to the user.

WHAT CHANGED
------------
main.py:
  - listings_get() now wrapped in try/except.
    On success: returns listings as before.
    On failure: returns HTTP 500 with the error detail so the app can
    display it and it can be diagnosed.
  - Version string updated: "PreferredHome API 3.2.2.1"
    (in both the health endpoint and FastAPI app declaration)

No other logic changed. All other endpoints are untouched.

DEPLOY STEPS
------------
1. Copy main.py from this ZIP into the root of your local
   PreferredHome-api repo (overwrite existing file).
2. Commit via GitHub Desktop using the commit message below.
3. Push to GitHub.
4. Render dashboard → Manual Deploy → Deploy latest commit.
5. Wait ~60 seconds for green Live status.
6. Open this URL in a browser and confirm the response:
   https://preferredhome-api.onrender.com/health
   Expected: {"ok":"PreferredHome API 3.2.2.1"}
   If it still shows an older version — the correct code did not
   reach GitHub. Do not proceed until this is resolved.
7. Sync the GitHub connection in your Claude Project
   (Claude Project → GitHub connection → Sync now).

COMMIT MESSAGE
--------------
```
Build 3.2.2.1 — Hotfix: wrap listings_get in try/except to fix HTTP 500 on all load screens
```
