from sqlalchemy.orm import Session
from models.posts import Posts
from schemas.post_schema import PostCreate, PostUpdate, PaginatedPostResponse
from datetime import datetime
from pytz import timezone

# 11.02 Paginator
from utils.paginator import Paginator  # Paginator 임포트
from sqlalchemy import or_, and_
from typing import List, Optional #11.02 Optional 추가


# 게시물 생성 함수
def create_post(db: Session, post: PostCreate):
    post_index = get_post_index(db)

    db_post = Posts(
        post_id=post_index,
        uid=post.uid,
        title=post.title,
        content=post.content,
        visibility=post.visibility,
        is_deleted=post.is_deleted,
        post_likes=post.post_likes,
        post_shares=post.post_shares
    )
    db.add(db_post)  # 게시물 추가 준비
    db.commit()  # 데이터베이스에 변경 사항 커밋
    db.refresh(db_post)  # 저장된 후 객체를 최신 상태로 갱신
    return db_post

def get_post_index(db: Session) -> str:
    str_date = datetime.now(timezone('Asia/Seoul')).strftime('%Y%m%d%H%M%S') #이거바꾸니까 서버 죽음
    seq = 0

    while True:
        seq += 1
        str_seq = str(seq).zfill(4)
        str_index = str_date + str_seq

        exists = True if db.query(Posts).filter(Posts.post_id == str_index).one_or_none() else False

        if not exists:
            return str_index


# 특정 게시물 조회 함수
def get_post_by_id(db: Session, post_id: str):
    return db.query(Posts).filter(Posts.post_id == post_id).first()  # 특정 post_id로 필터링

# 특정 게시물 수정 함수
def update_post_by_id(db: Session, post: Posts, post_update: PostUpdate):
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    if post_update.visibility is not None:
        post.visibility = post_update.visibility
    if post_update.is_deleted is not None:
        post.is_deleted = post_update.is_deleted
    if post_update.post_likes is not None:
        post.post_likes = post_update.post_likes
    if post_update.post_shares is not None:
        post.post_shares = post_update.post_shares

    db.commit()  # 수정된 내용을 데이터베이스에 반영
    db.refresh(post)  # 저장된 후 객체를 최신 상태로 갱신
    return post

# 11.02 게시물 페이지네이션 조회 함수
def get_paginated_posts(
    db: Session, 
    cursor: Optional[str] = None, 
    limit: int = 10, 
    viewer_id: Optional[str] = None
    #is_friend: bool = False
):
    query = db.query(Posts)

    # 가시성 필터 설정
    if viewer_id:
        visibility_filter = or_(
            Posts.uid == viewer_id,  # 본인의 게시물은 모두 조회 가능 private 포함
            Posts.visibility == 'public',  # 공개 게시물은 모두 조회 가능
            (is_friend and Posts.visibility == 'friends')  # 친구일 경우 친구에게만 공개된 게시물도 조회 가능
        )
        query = query.filter(visibility_filter)
    else:
        # viewer_id가 없는 경우 공개 게시물만 조회 가능
        query = query.filter(Posts.visibility == 'public')

    # Paginator 인스턴스 생성 및 페이지네이션 수행
    paginator = Paginator(Posts, query)
    paginated_result = paginator.get_paginated_result(
        cursor=cursor,
        sorts=["-created_at"],  # 가장 최근에 작성된 게시물부터 조회
        limit=limit
    )

    # 다음 페이지 여부 확인 및 아이템 반환
    items = paginated_result.main_query.all()
    has_more = len(items) > limit  # limit + 1로 가져왔을 경우 다음 데이터가 존재함을 의미함

    # 실제 반환할 데이터만 슬라이싱 (limit으로 제한)
    items = items[:limit]

    # PostResponse로 변환
    response_items = [
        PostResponse(
            post_id=item.post_id,
            uid=item.uid,
            title=item.title,
            content=item.content,
            visibility=item.visibility,
            is_deleted=item.is_deleted,
            post_likes=item.post_likes,
            post_shares=item.post_shares,
            created_at=item.created_at,
            last_updated=item.last_updated
        )
        for item in items
    ]

    return PaginatedPostResponse(
        items=response_items,  # 현재 페이지의 게시물 리스트
        has_more=has_more,  # 다음 페이지 존재 여부
        next_cursor=response_items[-1].post_id if has_more and response_items else None  # 다음 커서 값 설정 (있다면 마지막 아이템의 ID)
    )