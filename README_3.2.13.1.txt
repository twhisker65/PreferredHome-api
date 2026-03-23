PreferredHome — Build 3.2.13.1 (Hotfix)
========================================
API crash fix — PARKING_OPTIONS restored in config_constants.py
API repo only. No mobile changes. No Expo restart needed.
Generated: March 2026

ROOT CAUSE
----------
Build 3.2.13 delivered a config_constants.py that renamed PARKING_OPTIONS
to PARKING_TYPE_OPTIONS without instruction. helpers.py imports PARKING_OPTIONS
by name. This caused an ImportError on startup, crashing the API immediately.

CHANGED FILES
-------------
preferredhome_api/core/config_constants.py  — PARKING_OPTIONS restored
main.py                                     — unchanged from 3.2.13 delivery

WHAT CHANGED
------------
config_constants.py:
  - PARKING_OPTIONS restored exactly as it was in Build 3.2.11.
  - totalUpfront added to LISTINGS_COLUMNS (the only authorized change).
  - totalUpfront added to NUMERIC_FIELDS (the only authorized change).
  - No other changes from Build 3.2.11 original.

main.py:
  - Identical to the 3.2.13 delivery. Included here for completeness.

DEPLOY STEPS
------------
1. Copy both files into your local PreferredHome-api repo:
     main.py  (repo root)
     preferredhome_api/core/config_constants.py
2. Commit using the commit message below.
3. Push to GitHub.
4. Render dashboard → Manual Deploy → Deploy latest commit.
5. Wait ~60 seconds for green Live status.
6. Verify: https://preferredhome-api.onrender.com/health
   Expected: {"ok":"PreferredHome API 3.2.13"}

COMMIT MESSAGE
--------------
Build 3.2.13.1 -- Hotfix: restore PARKING_OPTIONS in config_constants, fix API crash
