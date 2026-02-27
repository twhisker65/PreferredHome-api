# PreferredHome API (Google Sheets backend)

This is a small FastAPI service that reads/writes apartment listings stored in a Google Sheet.

## Endpoints
- GET `/health`
- GET `/listings`
- POST `/listings` (body: JSON fields, ID optional)
- PUT `/listings/{id}`
- DELETE `/listings/{id}`
- GET `/baseline`
- PUT `/baseline`
- GET `/categories`
- POST `/categories`
- DELETE `/categories?category=...&label=...`

## Required environment variables (Render)
- `GOOGLE_SERVICE_ACCOUNT_JSON` : the full service account JSON (as a single JSON string)
- `SPREADSHEET_NAME` : Google Sheet name (or set `SPREADSHEET_URL`)
- `CORS_ALLOW_ORIGINS` : '*' or comma-separated origins (optional)

## Google Sheet access
Share the sheet with the service account `client_email` as an editor.

