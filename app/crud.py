from sqlalchemy.orm import Session
from . import models, schemas

# 사용자 생성 함수
# UserCreate 스키마로부터 전달된 데이터를 사용하여 새로운 사용자를 생성합니다.
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        provider=user.provider,
        provider_id=user.provider_id,
        bio=user.bio,
        phone_number=user.phone_number,
        status=user.status,
        email_verified=user.email_verified
    )
    db.add(db_user)  # 새 사용자 객체를 데이터베이스 세션에 추가
    db.commit()  # 세션에 있는 변경 사항을 커밋하여 데이터베이스에 저장
    db.refresh(db_user)  # 새로 생성된 사용자 객체를 최신 상태로 갱신
    return db_user  # 생성된 사용자 객체를 반환

# 특정 사용자 검색 함수
# user_id로 특정 사용자를 검색하여 반환합니다.
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

# 이메일로 사용자 검색 함수
# 이메일을 사용하여 특정 사용자를 검색하여 반환합니다.
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# 소셜 제공자의 ID로 사용자 검색 함수
# 소셜 로그인에서 사용되는 provider_id를 사용하여 사용자를 검색합니다.
def get_user_by_provider_id(db: Session, provider_id: str):
    return db.query(models.User).filter(models.User.provider_id == provider_id).first()

# 모든 사용자 검색 함수
# 페이징을 적용하여 사용자를 목록으로 반환합니다.
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# 사용자 업데이트 함수
# user_id로 특정 사용자를 검색한 후, 전달된 데이터로 업데이트합니다.
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)  # 객체의 속성을 업데이트
        db.commit()
        db.refresh(db_user)
    return db_user

# 사용자 삭제 함수
# user_id로 특정 사용자를 검색한 후, 데이터베이스에서 삭제합니다.
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)  # 사용자 객체를 데이터베이스 세션에서 삭제
        db.commit()
    return db_user

# 게시글 생성 함수
# PostCreate 스키마로부터 전달된 데이터를 사용하여 새로운 게시글을 생성합니다.
def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(
        title=post.title,
        content=post.content,
        visibility=post.visibility,
        user_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# 특정 게시글 검색 함수
# post_id로 특정 게시글을 검색하여 반환합니다.
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.post_id == post_id).first()

# 모든 게시글 검색 함수
# 페이징을 적용하여 게시글을 목록으로 반환합니다.
def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

# 게시글 업데이트 함수
# post_id로 특정 게시글을 검색한 후, 전달된 데이터로 업데이트합니다.
def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in post_update.dict(exclude_unset=True).items():
            setattr(db_post, key, value)  # 객체의 속성을 업데이트
        db.commit()
        db.refresh(db_post)
    return db_post

# 게시글 삭제 함수
# post_id로 특정 게시글을 검색한 후, 데이터베이스에서 삭제합니다.
def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)  # 게시글 객체를 데이터베이스 세션에서 삭제
        db.commit()
    return db_post

# 댓글 생성 함수
# CommentCreate 스키마로부터 전달된 데이터를 사용하여 새로운 댓글을 생성합니다.
def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int, post_id: int):
    db_comment = models.Comment(
        content=comment.content,
        user_id=user_id,
        post_id=post_id,
        parent_comment_id=comment.parent_comment_id,
        depth=1 if comment.parent_comment_id else 0  # 대댓글인 경우 깊이를 1로 설정
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# 특정 댓글 검색 함수
# comment_id로 특정 댓글을 검색하여 반환합니다.
def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.comment_id == comment_id).first()

# 특정 게시글의 모든 댓글 검색 함수
# post_id로 특정 게시글에 대한 댓글을 페이징하여 반환합니다.
def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Comment).filter(models.Comment.post_id == post_id).offset(skip).limit(limit).all()

# 댓글 업데이트 함수
# comment_id로 특정 댓글을 검색한 후, 전달된 데이터로 업데이트합니다.
def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        for key, value in comment_update.dict(exclude_unset=True).items():
            setattr(db_comment, key, value)  # 객체의 속성을 업데이트
        db.commit()
        db.refresh(db_comment)
    return db_comment

# 댓글 삭제 함수
# comment_id로 특정 댓글을 검색한 후, 데이터베이스에서 삭제합니다.
def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)  # 댓글 객체를 데이터베이스 세션에서 삭제
        db.commit()
    return db_comment

# PostImage 생성 함수
# PostImageCreate 스키마로부터 전달된 데이터를 사용하여 새로운 게시글 이미지를 생성합니다.
def create_post_image(db: Session, post_image: schemas.PostImageCreate):
    db_post_image = models.PostImage(
        post_id=post_image.post_id,
        image_url=post_image.image_url,
        order=post_image.order,
        alt_text=post_image.alt_text
    )
    db.add(db_post_image)
    db.commit()
    db.refresh(db_post_image)
    return db_post_image

# 특정 이미지 검색 함수
# image_id로 특정 이미지를 검색하여 반환합니다.
def get_post_image(db: Session, image_id: int):
    return db.query(models.PostImage).filter(models.PostImage.image_id == image_id).first()

# 이미지 삭제 함수
# image_id로 특정 이미지를 검색한 후, 데이터베이스에서 삭제합니다.
def delete_post_image(db: Session, image_id: int):
    db_post_image = get_post_image(db, image_id)
    if db_post_image:
        db.delete(db_post_image)  # 이미지 객체를 데이터베이스 세션에서 삭제
        db.commit()
    return db_post_image

# PostLike 생성 함수
# PostLikeCreate 스키마로부터 전달된 데이터를 사용하여 새로운 게시글 좋아요를 생성합니다.
def create_post_like(db: Session, post_like: schemas.PostLikeCreate):
    db_post_like = models.PostLike(
        post_id=post_like.post_id,
        user_id=post_like.user_id
    )
    db.add(db_post_like)
    db.commit()
    db.refresh(db_post_like)
    return db_post_like

# 게시글 좋아요 삭제 함수
# post_id와 user_id로 특정 좋아요를 검색하여 데이터베이스에서 삭제합니다.
def delete_post_like(db: Session, post_id: int, user_id: int):
    db_post_like = db.query(models.PostLike).filter(
        models.PostLike.post_id == post_id,
        models.PostLike.user_id == user_id
    ).first()
    if db_post_like:
        db.delete(db_post_like)  # 좋아요 객체를 데이터베이스 세션에서 삭제
        db.commit()
    return db_post_like

# CommentLike 생성 함수
# CommentLikeCreate 스키마로부터 전달된 데이터를 사용하여 새로운 댓글 좋아요를 생성합니다.
def create_comment_like(db: Session, comment_like: schemas.CommentLikeCreate):
    db_comment_like = models.CommentLike(
        comment_id=comment_like.comment_id,
        user_id=comment_like.user_id
    )
