from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    uid: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    status: Optional[int]
    profile_intro: Optional[str] = None
    profile_image: Optional[int] = None

    file_name: Optional[str] = None
    file_url: Optional[str] = None

    class Config:
        orm_mode = True

class UserProfileUpdate(BaseModel):
    user_name: Optional[str] = None
    profile_intro: Optional[str] = None
    profile_image: Optional[int] = None

    class Config:
        orm_mode = True

class CheckUserId(BaseModel):
    uid: str

class UserIdExistsResponse(BaseModel):
    uid: str
    exists: bool