from sqlalchemy.orm import Session
from models.posts import Posts
from schemas.post_schema import PostCreate, PostUpdate

# 게시물 생성 함수
def create_post(db: Session, post: PostCreate):
    db_post = Posts(
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
