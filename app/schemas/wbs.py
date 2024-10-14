# app/schemas/wbs.py
from pydantic import BaseModel, Field
from typing import List, Optional
from .activity import ActivityResponse

class WbsBase(BaseModel):
    name: str = Field(..., alias="name")
    date: Optional[str] = Field(None, alias="date")
    templateId: Optional[int] = None
    
    class Config:
        allow_population_by_field_name = True
        from_attributes = True

class WbsCreate(WbsBase):
    pass

class WbsResponse(WbsBase):
    wbsId: int = Field(..., alias="wbsId")
    activities: List[ActivityResponse] = []

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        from_attributes = True