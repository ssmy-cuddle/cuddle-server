from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    uid: str  # 사용자 ID
    title: str
    content: str
    visibility: Optional[str] = 'public'
    is_deleted: Optional[int] = 0
    post_likes: Optional[int] = 0
    post_shares: Optional[int] = 0

class PostCreate(PostBase):
    uid: str  # 필수: 작성자의 사용자 ID
    title: str  # 필수: 게시글 제목
    content: str  # 필수: 게시글 본문
    visibility: Optional[str] = 'public'  # 선택: 공개 범위


class PostUpdate(PostBase):
    title: Optional[str] = None  # 선택: 게시글 제목
    content: Optional[str] = None  # 선택: 게시글 본문
    visibility: Optional[str] = None  # 선택: 공개 범위
    is_deleted: Optional[int] = None  # 선택: 삭제 여부
    post_likes: Optional[int] = None  # 선택: 좋아요 수
    post_shares: Optional[int] = None  # 선택: 공유 수


class PostResponse(PostBase):
    post_id: str  # 게시글 ID
    created_at: datetime  # 생성 시간
    last_updated: datetime  # 마지막 업데이트 시간

    class Config:
        from_attributes = True  # ORM 객체에서 속성 매핑

# 11.02
class PaginatedPostResponse(BaseModel):
    items: List[PostResponse]  # 페이지네이션 결과로 포함된 게시물 리스트
    has_more: bool  # 다음 페이지 존재 여부
    next_cursor: Optional[str]  # 다음 페이지를 조회하기 위한 커서 값 (없으면 None)

    class Config:
        from_attributes = True  # ORM 객체에서 속성 매핑
