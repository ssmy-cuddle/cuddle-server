from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostBase(BaseModel):
    post_id: str
    uid: str  # 사용자 ID
    title: str
    content: str
    visibility: Optional[str] = 'public'
    is_deleted: Optional[int] = 0
    post_likes: Optional[int] = 0
    post_shares: Optional[int] = 0

class PostCreate(BaseModel):
    uid: str  # 필수: 작성자의 사용자 ID
    title: str  # 필수: 게시글 제목
    content: str  # 필수: 게시글 본문
    visibility: Optional[str] = 'public'  # 선택: 공개 범위


class PostUpdate(BaseModel):
    title: Optional[str] = None  # 선택: 게시글 제목
    content: Optional[str] = None  # 선택: 게시글 본문


class PostResponse(PostBase):
    post_id: str  # 게시글 ID
    created_at: datetime  # 생성 시간
    last_updated: datetime  # 마지막 업데이트 시간

    class Config:
        from_attributes = True  # ORM 객체에서 속성 매핑

class PaginatedPostResponseItems(BaseModel):
    post_id: str
    uid: str  # 사용자 ID
    title: Optional[str]
    content: Optional[str]
    images: Optional[List] = None
    visibility: Optional[str] = 'public'
    postLike_cnt : Optional[int] = 0
    comment_cnt : Optional[int] = 0
    can_modify : Optional[str] = None
    created_at: datetime
    reactions: Optional[bool] = False

    class Config:
        orm_mode = True
        from_attributes = True  # ORM 객체에서 속성 매핑 가능하게 설정

# 11.02
class PaginatedPostResponse(BaseModel):
    model_name: str  # 모델의 이름을 저장하는 필드
    items: List[PaginatedPostResponseItems]  # 페이지네이션 결과로 포함된 게시물 리스트
    has_more: bool  # 다음 페이지 존재 여부
    next_cursor: Optional[str]  # 다음 페이지를 조회하기 위한 커서 값 (없으면 None)
    class Config:
        from_attributes = True  # ORM 객체에서 속성 매핑

# 11.06 POST 전체 조회
class PaginatedPostResponse2(BaseModel):
    items: List[PaginatedPostResponseItems]  # 페이지네이션 결과로 포함된 게시물 리스트
    has_more: bool  # 다음 페이지 존재 여부
    next_cursor: Optional[str] = None  # 다음 페이지를 조회하기 위한 커서 값 (없으면 None)
    class Config:
        from_attributes = True  # ORM 객체에서 속성 매핑
