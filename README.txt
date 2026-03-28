PreferredHome — Build 3.2.15.3 Hotfix
======================================
Diagnostic logging — main.py only.
Generated: March 2026

WHAT CHANGED
------------
API repo only. No mobile changes.

  main.py
    — Added print() statements at the top of POST /commute/recalculate-all:
        [recalc-all] keys=... workAddress=...
        [recalc-all] work_address=... method=...
        [recalc-all] early return — work address empty  (if triggered)
        [recalc-all] loaded N listings
    — Version bump to 3.2.15.3

PURPOSE
-------
recalculate-all fires and returns 200 OK but no [commute] log lines appear,
meaning calculate_commute() is never called. These logs will show what
workAddress value the API is actually receiving in the payload.

DEPLOY STEPS — API ONLY
------------------------
1. Copy main.py into PreferredHome-api repo (overwrite existing)
2. Commit in GitHub Desktop:
     Build 3.2.15.3 Hotfix - add recalculate-all payload logging
3. Push to MAIN
4. Render: "Deploy latest commit"
5. Verify: https://preferredhome-api.onrender.com/health
   Expected: { "ok": "PreferredHome API 3.2.15.3" }

AFTER DEPLOYING
---------------
1. Open Profile → change Work Address → close panel
2. Immediately check Render Logs
3. Share lines starting with [recalc-all]

COMMIT MESSAGE
--------------
Build 3.2.15.3 Hotfix - add recalculate-all payload logging

RENDER HEALTH CHECK
-------------------
https://preferredhome-api.onrender.com/health
