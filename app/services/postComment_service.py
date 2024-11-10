from sqlalchemy.orm import Session
from models.postComments import PostComment
from schemas.postComment_schema import PostCommentCreate, PostCommentUpdate, PaginatedPostCommentResponseItems, PaginatedPostCommentResponse
from datetime import datetime
from pytz import timezone
from pydantic import parse_obj_as
from sqlalchemy import or_, and_
from typing import List, Optional 

# 댓글생성
def create_postComment(post_id : str,  parent_id: Optional[int], db: Session, postComment: PostCommentCreate):

    db_postComment = PostComment(
        message=postComment.message,
        uid=postComment.uid,
        post_id=post_id,
        parent_id=parent_id
    )
    db.add(db_postComment)  # 게시물 추가 준비
    db.commit()  # 데이터베이스에 변경 사항 커밋
    db.refresh(db_postComment)  # 저장된 후 객체를 최신 상태로 갱신
    return db_postComment

def convert_posts_to_pydantic(items: List[PostComment], viewer_id: Optional[str]):
    response_items = []
    
    for item in items:
        # from_orm을 이용하여 기본 모델 생성
        pydantic_item = PaginatedPostCommentResponseItems.from_orm(item)
        
        # 수동으로 각 필드 업데이트
        pydantic_item.can_modify = "y" if (item.uid == viewer_id) else "n"
        pydantic_item.reactions = True
        pydantic_item.user_name = "str"  # 여기서 하드코딩된 값 설정
        pydantic_item.profile_image = None  # 하드코딩된 값 설정
        
        response_items.append(pydantic_item)

    return response_items

def get_postComment_by_id(db: Session, comment_id: int):
    return db.query(PostComment).filter(PostComment.comment_id == comment_id).first()

def delete_postComment_by_id(db: Session, postComment: PostComment):
    db.delete(postComment)
    db.commit()

def get_paging_postcomment(
    post_id : str,
    viewer_id : Optional[str],
    db: Session
):
    query = db.query(PostComment)
    query = db.query(PostComment).filter(PostComment.post_id == post_id)
    query = query.order_by(PostComment.created_at.desc())
    items = query.all()

    response_items_pydantic = convert_posts_to_pydantic(items, viewer_id)
    
    return PaginatedPostCommentResponse(
        items=response_items_pydantic, 
        has_more=None,
        next_cursor=None
    )