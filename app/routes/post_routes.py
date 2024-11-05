from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.post_schema import PostCreate, PostUpdate, PostResponse, PaginatedPostResponse
from services.post_service import create_post, get_post_by_id, update_post_by_id, get_paginated_posts
from typing import List, Optional #11.02 Optional 추가

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post_endpoint(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db=db, post=post)

@router.get("/{post_id}", response_model=PostResponse)
def get_post_endpoint(post_id: str, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

@router.patch("/{post_id}", response_model=PostResponse)
def update_post_endpoint(post_id: str, post_update: PostUpdate, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    updated_post = update_post_by_id(db, post, post_update)
    return updated_post

# 무한 스크롤 게시물 조회를 위한 페이지네이션 엔드포인트
@router.get("/userPosts/{uid}", response_model=PaginatedPostResponse)
def get_posts_endpoint(
    uid: str,
    cursor: Optional[str] = None,
    db: Session = Depends(get_db)
):
    limit: int = 10  # 페이지당 게시물 수
    result = get_paginated_posts(db=db, uid=uid, cursor=cursor, limit=limit)
    return result
