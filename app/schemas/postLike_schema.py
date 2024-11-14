from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostLikeResponse(BaseModel):
    id: Optional[int] = None
    post_id: Optional[str] = None
    uid: Optional[str] = None
    created_at: Optional[datetime] = None

class PostLikeCreate(BaseModel):
    post_id: str
    uid: str