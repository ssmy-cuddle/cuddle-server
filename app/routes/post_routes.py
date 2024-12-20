from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.post_schema import get_journey_response,PostCreate, PostUpdate, PostResponse, PaginatedPostResponse, PaginatedPostResponseItems, PaginatedPostResponse2
from services.post_service import get_post_by_id2, delete_post_by_id, get_journey, create_post, get_post_by_id, update_post_by_id, get_paginated_posts, get_paginated_posts2
from typing import List, Optional #11.02 Optional 추가
import logging

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
    post = get_post_by_id2(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    updated_post = update_post_by_id(db, post, post_update)
    return updated_post

# 무한 스크롤 게시물 조회를 위한 페이지네이션 엔드포인트
@router.get("/userPosts/{inqr_id}/{viewer_id}", response_model=PaginatedPostResponse)
def get_posts_endpoint(
    inqr_id: str,
    viewer_id : str,
    cursor: Optional[str] = None,
    db: Session = Depends(get_db)
):
    limit: int = 10  # 페이지당 게시물 수
    result = get_paginated_posts(
             db=db, 
             uid=inqr_id, 
             viewer_id=viewer_id,
             cursor=cursor,
             #is_friend = null,
             limit=limit)
    return result

# 전체 조회 페이징
@router.get("/getAllPosts/{viewer_id}", response_model=PaginatedPostResponse2)
def get_posts_endpoint(
    viewer_id : str,
    cursor: Optional[str] = None,
    db: Session = Depends(get_db)
):
    logging.info(f"Received request for viewer_id: {viewer_id} with cursor: {cursor}")
                 
    limit: int = 10  # 페이지당 게시물 수
    result = get_paginated_posts2(
             db=db, 
             viewer_id=viewer_id,
             cursor=cursor,
             limit=limit)
    return result

# 전체 조회 페이징
@router.get("/{viewer_id}/{inqr_date}", response_model=get_journey_response)
def get_journey_endpoint(
    viewer_id : str,
    inqr_date : str,
    db: Session = Depends(get_db)
):

    result = get_journey(
             db=db, 
             viewer_id=viewer_id,
             inqr_date=inqr_date)

    return result

@router.delete("/{post_id}", response_model=dict)
def delete_post_endpoint(post_id: str, db: Session = Depends(get_db)):
    post = get_post_by_id2(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    delete_post_by_id(db, post)
    return {"detail": "Post deleted successfully"}