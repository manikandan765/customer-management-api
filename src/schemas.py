from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = None


class CustomerOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    city: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True