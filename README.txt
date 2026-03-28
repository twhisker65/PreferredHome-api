PreferredHome — Build 3.2.15.2 Hotfix
======================================
Diagnostic logging — helpers.py only.
Generated: March 2026

WHAT CHANGED
------------
API repo only. No mobile changes.

  preferredhome_api/utils/helpers.py
    — Added print() statements inside calculate_commute():
        [commute] api_key present=True/False
        [commute] origin=... dest=... mode=...
        [commute] status=... rows=...
        [commute] element_status=...
        [commute] result=N minutes  (or exception message)

  main.py
    — Version bump to 3.2.15.2 only. No logic changes.

PURPOSE
-------
recalculate-all fires and returns 200 OK but commute times do not update.
These logs will show exactly what Google Maps returns so the root cause
can be identified and fixed.

DEPLOY STEPS — API ONLY
------------------------
1. Copy these 2 files into PreferredHome-api repo (overwrite existing):
     preferredhome_api/utils/helpers.py
     main.py
2. Commit in GitHub Desktop:
     Build 3.2.15.2 Hotfix - add commute diagnostic logging
3. Push to MAIN
4. Render: "Deploy latest commit"
5. Verify: https://preferredhome-api.onrender.com/health
   Expected: { "ok": "PreferredHome API 3.2.15.2" }

AFTER DEPLOYING
---------------
1. Open Profile → change Work Address → close panel
2. Immediately check Render Logs
3. Look for lines starting with [commute]
4. Share the log output

COMMIT MESSAGE
--------------
Build 3.2.15.2 Hotfix - add commute diagnostic logging

RENDER HEALTH CHECK
-------------------
https://preferredhome-api.onrender.com/health
