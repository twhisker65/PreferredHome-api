from pydantic import BaseModel, Field
from typing import Optional, Any, Dict

class Listing(BaseModel):
    id: str = Field(..., alias="id")
    data: Dict[str, Any] = Field(default_factory=dict)
    class Config:
        populate_by_name = True

class ListingCreate(BaseModel):
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
