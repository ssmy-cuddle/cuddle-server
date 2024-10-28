from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    uid: str
    user_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    status: Optional[int]

    class Config:
        from_attributes = True