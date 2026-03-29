PreferredHome — Build 3.2.17
============================
Neighborhood section — Transportation renamed to Neighborhood.
Neighborhood field moved from Property section. Near By moved from
Features section. New fields added: safetyScore and noiseScore.
All fields manually enterable. Both mobile and API updated.
Generated: March 2026

CHANGED FILES (in folder order)
---------------------------------
PreferredHome-mobile/
  components/ListingForm.tsx        — Neighborhood section, new fields, moved fields
  components/ViewPanel.tsx          — Neighborhood section, safetyScore/noiseScore display

PreferredHome-api/
  preferredhome_api/core/config_constants.py  — safetyScore and noiseScore registered

WHAT CHANGED IN THIS BUILD
----------------------------

1. components/ListingForm.tsx
   - Draft type: safetyScore and noiseScore added as string fields.
   - BLANK_DRAFT: safetyScore and noiseScore initialised to "".
   - rawToDraft: safetyScore and noiseScore mapped from raw data.
   - buildPayload: safetyScore and noiseScore included as numeric values.
   - open state: key renamed from "transportation" to "neighborhood".
   - Property section: Neighborhood field REMOVED (moved to Neighborhood section).
   - Features section: Close By picker REMOVED (moved to Neighborhood section).
   - Transportation section RENAMED to Neighborhood section with new field order:
       1. Neighborhood (text field — first)
       2. Commute Time (min)
       3. Walk Score (0-100)
       4. Transit Score (0-100)
       5. Bike Score (0-100)
       6. Safety Score (0-100) — NEW
       7. Noise Score (0-100) — NEW
       8. Close By (multi-select — last)

2. components/ViewPanel.tsx
   - safetyScore and noiseScore extracted from raw data.
   - hasScores updated to include safetyScore and noiseScore.
   - Neighborhood field (hood) REMOVED from Property display area.
   - Features section: Close By REMOVED (moved to Neighborhood section).
   - Transportation SectionHead RENAMED to "Neighborhood".
   - Neighborhood section now shows:
       - Neighborhood name (first, conditional on value)
       - Commute time (conditional on value)
       - Score badges: Walk, Transit, Bike, Safety, Noise
       - Close By (last, always shown via CommaField)

3. preferredhome_api/core/config_constants.py
   - "safetyScore" and "noiseScore" appended to LISTINGS_COLUMNS.
   - "safetyScore" and "noiseScore" added to NUMERIC_FIELDS after "bikeScore".
   - No other constants changed.

DEPLOY STEPS
------------
Mobile repo:
1. Copy components/ListingForm.tsx into PreferredHome-mobile/components/
2. Copy components/ViewPanel.tsx into PreferredHome-mobile/components/
3. Commit in GitHub Desktop using the commit message below.
4. Push to GitHub.
5. Restart Expo using the command below.
6. Test on your physical device.

API repo:
1. Copy preferredhome_api/core/config_constants.py into the matching path.
2. Commit in GitHub Desktop using the commit message below.
3. Push to GitHub — Render will auto-deploy.
4. Wait ~60 seconds, then verify: https://preferredhome-api.onrender.com/health

COMMIT MESSAGES
---------------
Mobile repo — copy and paste exactly:

Build 3.2.17 - Neighborhood section — Transportation renamed, Neighborhood and Close By moved in, safetyScore and noiseScore added

API repo — copy and paste exactly:

Build 3.2.17 - Register safetyScore and noiseScore in config_constants

EXPO RESTART COMMAND
--------------------
Copy and paste exactly:

cd C:\Users\twhis\OneDrive\Documents\GitHub\PreferredHome-mobile && npx expo start --tunnel --clear

RENDER HEALTH CHECK
-------------------
https://preferredhome-api.onrender.com/health

TEST CHECKLIST
--------------
[ ] 1. Open Add screen → Property section: confirm NO Neighborhood text field present.
[ ] 2. Open Add screen → Features section: confirm NO Close By picker present.
[ ] 3. Open Add screen → Neighborhood section: confirm label reads "Neighborhood" (not "Transportation").
[ ] 4. Open Add screen → Neighborhood section: confirm field order is:
        Neighborhood → Commute Time → Walk Score → Transit Score →
        Bike Score → Safety Score → Noise Score → Close By
[ ] 5. Enter a value in Safety Score and Noise Score. Tap Save.
        Open the listing in ViewPanel. Confirm both scores appear as
        circular badges in the Neighborhood section.
[ ] 6. Open ViewPanel for any listing → Neighborhood section shows
        neighborhood name first (if set), then commute, then score
        badges, then Close By last.
[ ] 7. Open ViewPanel → Features section: confirm Close By is NOT shown there.
[ ] 8. Open ViewPanel → confirm no standalone Neighborhood row appears
        in the property area at the top.
[ ] 9. Select Close By values in Neighborhood section. Save.
        Open ViewPanel. Confirm Close By values display under Neighborhood.
[ ] 10. Verify /health returns OK after Render deploy.
