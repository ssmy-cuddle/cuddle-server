from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.postComment_schema import PostCommentCreate, PostCommentUpdate, PaginatedPostCommentResponse, PostCommentResponse, PaginatedPostCommentResponseItems
from services.postComment_service import create_postComment, get_paging_postcomment, get_postComment_by_id, delete_postComment_by_id
from typing import List, Optional

router = APIRouter()

@router.post("/{post_id}", response_model=PostCommentResponse)
def create_postComment_endpoint(
    post_id: str, 
    postComment: PostCommentCreate, 
    db: Session = Depends(get_db),
    parent_id: Optional[int] = None
):
 
    return create_postComment(post_id=post_id, parent_id=parent_id, db=db, postComment=postComment)

# 댓글 페이징 
@router.get("/{post_id}", response_model=PaginatedPostCommentResponse)
def get_paging_postComment_endpoint(
    post_id: str,
    viewer_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    
    result = get_paging_postcomment(post_id=post_id, viewer_id=viewer_id, comment_id=None, db=db)
    return result

# 답글 조회
@router.get("/subComment/{comment_id}", response_model=PaginatedPostCommentResponse)
def get_paging_postComment_endpoint(
    comment_id: int,
    viewer_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    
    result = get_paging_postcomment(post_id=None, viewer_id=viewer_id, comment_id=comment_id, db=db)
    return result

@router.delete("/{comment_id}", response_model=dict)
def delete_postComment_endpoint(comment_id: int, db: Session = Depends(get_db)):
    postComment = get_postComment_by_id(db, comment_id)
    if not postComment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="comment not found"
        )
    delete_postComment_by_id(db, postComment)
    return {"detail": "comment deleted successfully"}
