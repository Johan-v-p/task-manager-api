from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    user_id: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    is_active: bool
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True    
