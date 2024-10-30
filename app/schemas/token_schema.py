from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TokenCreate(BaseModel):
    uid: str
    access_token: str
    refresh_token: str
    provider: str

class TokenUpdate(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True

class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True