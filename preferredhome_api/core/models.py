from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List

class Listing(BaseModel):
    id: str = Field(..., alias="ID")
    # Keep fields flexible: we store additional sheet columns as-is
    data: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        populate_by_name = True

class ListingCreate(BaseModel):
    # Client can omit ID; backend will generate
    data: Dict[str, Any]

class ListingUpdate(BaseModel):
    data: Dict[str, Any]

class Baseline(BaseModel):
    data: Dict[str, Any]

class Toggles(BaseModel):
    data: Dict[str, Any]

class CategoryItem(BaseModel):
    category: str
    label: str
    weight: Optional[float] = None
    notes: Optional[str] = None
