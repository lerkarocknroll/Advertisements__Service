from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AdvertisementBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    author: str

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None

class AdvertisementResponse(AdvertisementBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OKResponse(BaseModel):
    status: str = "ok"