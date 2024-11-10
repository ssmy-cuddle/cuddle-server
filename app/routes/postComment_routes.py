from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.postComment_schema import PostCommentCreate, PostCommentUpdate, PaginatedPostCommentResponse, PostCommentResponse, PaginatedPostCommentResponseItems
from services.postComment_service import create_postComment, get_paging_postcomment
from typing import List, Optional

router = APIRouter()

@router.post("/{post_id}", response_model=PostCommentResponse)
def create_postComment_endpoint(post_id: str, postComment: PostCommentCreate, db: Session = Depends(get_db)):
 
    return create_postComment(post_id=post_id, db=db, postComment=postComment)

# 댓글 페이징 
@router.get("/{post_id}", response_model=PaginatedPostCommentResponseItems)
def get_paging_postComment_endpoint(
    post_id: str,
    viewer_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    
    result = get_paging_postcomment(post_id=post_id, viewer_id=viewer_id, db=db)
    return result
