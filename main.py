from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List

from preferredhome_api.core.settings import get_settings
from preferredhome_api.storage.sheets_storage import (
    load_listings_df, add_listing, update_listing, delete_listing,
    load_baseline, save_baseline,
    load_categories_df, add_category_item, delete_category_item,
)
from preferredhome_api.utils.helpers import generate_id

app = FastAPI(title="PreferredHome API", version="0.1.0")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/listings")
def listings_get():
    df = load_listings_df()
    return df.fillna("").to_dict(orient="records")

@app.post("/listings")
def listings_post(payload: Dict[str, Any]):
    # payload is listing fields; ID optional
    try:
        row = add_listing(payload)
        return row
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/listings/{listing_id}")
def listings_put(listing_id: str, payload: Dict[str, Any]):
    try:
        row = update_listing(listing_id, payload)
        return row
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/listings/{listing_id}")
def listings_delete(listing_id: str):
    try:
        delete_listing(listing_id)
        return {"ok": True}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/baseline")
def baseline_get():
    try:
        return load_baseline()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/baseline")
def baseline_put(payload: Dict[str, Any]):
    try:
        return save_baseline(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/categories")
def categories_get():
    df = load_categories_df()
    return df.fillna("").to_dict(orient="records")

@app.post("/categories")
def categories_post(payload: Dict[str, Any]):
    try:
        category = payload.get("Category") or payload.get("category")
        label = payload.get("Label") or payload.get("label")
        weight = payload.get("Weight") or payload.get("weight")
        notes = payload.get("Notes") or payload.get("notes") or ""
        if not category or not label:
            raise ValueError("Category and Label are required.")
        return add_category_item(category, label, weight=weight if weight!="" else None, notes=notes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/categories")
def categories_delete(category: str, label: str):
    try:
        delete_category_item(category, label)
        return {"ok": True}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
