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
    profile_intro: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    profile_intro: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True

class CheckUserId(BaseModel):
    uid: str

class UserIdExistsResponse(BaseModel):
    uid: str
    exists: bool