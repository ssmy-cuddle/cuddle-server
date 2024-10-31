from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.post_schema import PostCreate, PostUpdate, PostResponse
from services.post_service import create_post, get_post_by_id, update_post_by_id
from typing import List

router = APIRouter()

@router.post("/", response_model=PostResponse)
def create_post_endpoint(pet: PostCreate, db: Session = Depends(get_db)):
    return create_post(db=db, pet=pet)

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

