BUILD_3.2.2.2_HOTFIX_README
===========================
PreferredHome API — Hotfix Build 3.2.2.2
Generated: March 2026
Repo: PreferredHome-api (MAIN branch)

CHANGED FILES (in folder order)
---------------------------------
main.py

ROOT CAUSE
----------
Row 13 in the Google Sheet has a corrupted value in the id column.
Pandas reads this corrupted value as float infinity (inf).

The prior sanitization code caught NaN (blank/missing) values but was
never written to catch inf values. When listings_get() tried to serialize
the data to JSON, Python's JSON encoder rejected inf as an illegal value
and threw a ValueError — crashing the entire response with HTTP 500.

WHAT CHANGED
------------
main.py — two targeted changes only:

1. _sanitize_value() — now catches inf and -inf in addition to NaN.
   Any infinity value in any field is replaced with empty string
   before it can reach the JSON serializer.

2. listings_get() — the DataFrame now has both fillna("") and
   replace(inf/-inf, "") applied before converting to a list of rows.
   This is a second line of defense covering every field in every row.

3. Version string updated to "PreferredHome API 3.2.2.2" in both
   the health endpoint and the FastAPI app declaration.

No other logic changed.

NOTE ON YOUR GOOGLE SHEET
--------------------------
Row 14 in your Listings sheet (row 13 counting from 0, or row 15 if
you count the header row as row 1) has a corrupted id value. After
this deploy the app will load normally. That row will appear with a
blank id. You can open your Google Sheet and manually delete that row
when convenient. It will not block the app from working.

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
   Expected: {"ok":"PreferredHome API 3.2.2.2"}
   If it shows an older version — stop and do not proceed.
7. Sync the GitHub connection in your Claude Project
   (Claude Project → GitHub connection → Sync now).

COMMIT MESSAGE
--------------
```
Build 3.2.2.2 — Hotfix: catch inf values in sanitization to fix HTTP 500 on listings load
```
