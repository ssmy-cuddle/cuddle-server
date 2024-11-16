from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CommunityBase(BaseModel):
    post_id: str
    uid: str  # 사용자 ID
    title: str
    content: str


class CommunityResponse(BaseModel):
    # 이미지, 제목, 내용,작성자 정보
    post_id: str
    uid: str  # 사용자 ID
    user_name: str
    profile_image_url: Optional[str] = None

    title: Optional[str]
    content: Optional[str]

    file_name: Optional[str] = None
    file_url: Optional[str] = None

    class Config:
        orm = True