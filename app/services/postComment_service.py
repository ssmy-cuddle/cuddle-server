from sqlalchemy.orm import Session
from models.postComments import PostComment
from schemas.postComment_schema import PostCommentCreate, PostCommentUpdate, PaginatedPostCommentResponseItems, PaginatedPostCommentResponse
from datetime import datetime
from pytz import timezone
from pydantic import parse_obj_as
from sqlalchemy import or_, and_
from typing import List, Optional 
from services.post_service import get_user_by_uid

# 댓글생성
def create_postComment(
    post_id : str,  
    parent_id: Optional[int],
    db: Session, 
    postComment: PostCommentCreate
):

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

def convert_posts_to_pydantic(db: Session, items: List[PostComment], viewer_id: Optional[str]):
    response_items = []
    
    for item in items:
        # from_orm을 이용하여 기본 모델 생성
        pydantic_item = PaginatedPostCommentResponseItems.from_orm(item)
        
        # 유저정보
        user_query = get_user_by_uid(db, item.uid)
        child_comment_cnt = get_child_postComment_cnt(db, item.comment_id)

        # 수동으로 각 필드 업데이트
        pydantic_item.can_modify = "y" if (item.uid == viewer_id) else "n"
        pydantic_item.reactions = True

        pydantic_item.user_name = user_query.user_name  
        pydantic_item.profile_image = user_query.profile_image  

        pydantic_item.child_comment_cnt = child_comment_cnt
        
        response_items.append(pydantic_item)

    return response_items

def get_postComment_by_id(db: Session, comment_id: int):
    return db.query(PostComment).filter(PostComment.comment_id == comment_id).first()

def delete_postComment_by_id(db: Session, postComment: PostComment):
    db.delete(postComment)
    db.commit()

def get_paging_postcomment(
    db: Session,
    post_id : str,
    viewer_id : str,
    comment_id : int
):
    # 메인댓글
    if comment_id is None:
        query = db.query(PostComment)
        query = query.filter(PostComment.post_id == post_id)  # post_id에 대한 필터 추가
        query = query.filter(PostComment.parent_id.is_(None))  # parent_id가 NULL인 경우 필터 추가
        query = query.order_by(PostComment.created_at.desc())  # 생성 시간 역순으로 정렬
        items = query.all()  # 최종 결과 가져오기


        response_items_pydantic = convert_posts_to_pydantic(db, items, viewer_id)
    
        return PaginatedPostCommentResponse(
            items=response_items_pydantic, 
            has_more=None,
            next_cursor=None
        )
    else :
    # 대댓글
        query = db.query(PostComment)
        query = query.filter(PostComment.parent_id == comment_id)  # comment_id로 필터링
        query = query.order_by(PostComment.created_at.desc())  # 생성 시간을 기준으로 내림차순 정렬
        items = query.all()  # 최종 결과 리스트 가져오기
        response_items_pydantic = convert_posts_to_pydantic(db, items, viewer_id)
    
        return PaginatedPostCommentResponse(
            items=response_items_pydantic, 
            has_more=None,
            next_cursor=None
        )
    
def get_postComment_cnt(db: Session, post_id: str):
    return db.query(PostComment).filter(PostComment.post_id == post_id).count()

def get_child_postComment_cnt(db: Session, comment_id: int):
    return db.query(PostComment).filter(PostComment.parent_id == comment_id).count()