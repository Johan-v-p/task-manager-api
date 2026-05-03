from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True