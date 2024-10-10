from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserInDB(UserBase):
    hashed_password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

class OAuthProvider(BaseModel):
    provider: str  # 'kakao' or 'ios'
    access_token: str

class OAuthUser(BaseModel):
    provider: OAuthProvider
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None