from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostCommentBase(BaseModel): #기본
    message: str  
    post_id: str
    uid: str
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None

class PostCommentCreate(BaseModel): # 댓글 생성
    post_id: str
    message: str  
    uid: str  
    parent_id: Optional[str] = None  

class PostCommentUpdate(BaseModel):
    message: Optional[str] = None

class PaginatedPostCommentResponseItems(BaseModel):
    #db 요소
    comment_id: int
    message: Optional[str] = None
    post_id: Optional[str] = None
    uid: Optional[str] = None
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None

    #그외 세팅
    user_name: Optional[str] = None
    profile_image: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True  # ORM 객체에서 속성 매핑 가능하게 설정

class PaginatedPostCommentResponse(BaseModel):
    items: List[PaginatedPostCommentResponseItems]  # 페이지네이션 결과로 포함된 게시물 리스트
    has_more: bool  # 다음 페이지 존재 여부
    next_cursor: Optional[str] = None  # 다음 페이지를 조회하기 위한 커서 값 (없으면 None)

    class Config:
        from_attributes = True  # ORM 객체에서 속성 매핑

class PostCommentResponse(PostCommentBase):
    comment_id: int

    class Config:
        from_attributes = True
