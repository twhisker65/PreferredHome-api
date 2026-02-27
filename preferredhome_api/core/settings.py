import json
import os
from functools import lru_cache
from typing import Any, Dict, Union

from pydantic import BaseModel, Field

# Load .env if present (local dev). On Render this is harmless.
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass


class Settings(BaseModel):
    # Preferred for local dev: point to the downloaded JSON file
    google_service_account_json_path: str = Field(default="", alias="GOOGLE_SERVICE_ACCOUNT_JSON_PATH")

    # Alternative: paste JSON into env var (common in hosted environments)
    google_service_account_json: str = Field(default="", alias="GOOGLE_SERVICE_ACCOUNT_JSON")

    # Spreadsheet selection (optional; your app may use config.py/constants instead)
    spreadsheet_name: str = Field(default="", alias="SPREADSHEET_NAME")
    spreadsheet_url: str = Field(default="", alias="SPREADSHEET_URL")

    # CORS (comma-separated or '*')
    cors_allow_origins: str = Field(default="*", alias="CORS_ALLOW_ORIGINS")

    def cors_origins_list(self):
        v = (self.cors_allow_origins or "*").strip()
        if v in ("", "*"):
            return ["*"]
        return [x.strip() for x in v.split(",") if x.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    data: Dict[str, Any] = {}
    for k in (
        "GOOGLE_SERVICE_ACCOUNT_JSON_PATH",
        "GOOGLE_SERVICE_ACCOUNT_JSON",
        "SPREADSHEET_NAME",
        "SPREADSHEET_URL",
        "CORS_ALLOW_ORIGINS",
    ):
        v = os.getenv(k)
        if v is not None:
            data[k] = v
    return Settings(**data)


def _normalize_private_key(d: Dict[str, Any]) -> Dict[str, Any]:
    pk = d.get("private_key")
    if isinstance(pk, str):
        # tolerate escaped newlines
        d["private_key"] = pk.replace("\\n", "\n")
    return d


def load_service_account_dict(source: Union[Settings, str, None] = None) -> Dict[str, Any]:
    """
    Loads the service account JSON dict from either:
      1) GOOGLE_SERVICE_ACCOUNT_JSON_PATH (file path)  [best for local dev]
      2) GOOGLE_SERVICE_ACCOUNT_JSON (raw JSON string) [common on Render]

    Backwards-compatible:
      - If you pass a string, it's treated as the raw JSON string.
      - If you pass Settings, it uses path first, then raw JSON.
      - If you pass None, it reads env vars via get_settings().
    """
    if source is None:
        settings = get_settings()
        json_path = settings.google_service_account_json_path.strip()
        raw = settings.google_service_account_json.strip()
    elif isinstance(source, str):
        json_path = ""
        raw = source.strip()
    else:
        settings = source
        json_path = settings.google_service_account_json_path.strip()
        raw = settings.google_service_account_json.strip()

    # Prefer file path if provided
    if json_path:
        if not os.path.exists(json_path):
            raise ValueError(f"GOOGLE_SERVICE_ACCOUNT_JSON_PATH does not exist: {json_path}")
        raw = open(json_path, "r", encoding="utf-8").read().strip()

    if not raw:
        raise ValueError("Missing GOOGLE_SERVICE_ACCOUNT_JSON_PATH or GOOGLE_SERVICE_ACCOUNT_JSON.")

    try:
        d = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON.") from e

    return _normalize_private_key(d)
