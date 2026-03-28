PreferredHome — Build 3.2.15.4 Hotfix
======================================
Fix: column names corrected to camelCase in commute endpoints.
Generated: March 2026

ROOT CAUSE
----------
The recalculate-all and calculate endpoints were checking for
"Street Address", "City", "State", "Commute Time" — title case.
The Google Sheet headers are camelCase: streetAddress, city, state,
commuteTime. Every listing was skipped because no columns matched.

CHANGED FILES
-------------
API repo only. No mobile changes.

  main.py
    — recalculate-all endpoint: fixed column names to camelCase
    — calculate/{listing_id} endpoint: fixed column names to camelCase
    — diagnostic print statements removed
    — Version: 3.2.15.4

DEPLOY STEPS — API ONLY
------------------------
1. Copy main.py into PreferredHome-api repo (overwrite existing)
2. Commit: Build 3.2.15.4 Hotfix - fix camelCase column names in commute endpoints
3. Push to MAIN
4. Render: Deploy latest commit
5. Verify: https://preferredhome-api.onrender.com/health
   Expected: { "ok": "PreferredHome API 3.2.15.4" }

TEST CHECKLIST
--------------
[ ] T1 — Add a listing with a street address. Save.
         Open listing — Commute Time shows minutes.
[ ] T2 — Edit a listing. Change street address. Save.
         Commute Time updates.
[ ] T3 — Open Profile. Change Work Address. Close panel.
         All listing commute times update.
[ ] T4 — Google Sheet: no duplicate rows.

COMMIT MESSAGE
--------------
Build 3.2.15.4 Hotfix - fix camelCase column names in commute endpoints

RENDER HEALTH CHECK
-------------------
https://preferredhome-api.onrender.com/health
