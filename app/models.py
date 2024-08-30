from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, Date, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# User 테이블을 나타내는 클래스
class User(Base):
    __tablename__ = "users"

    # 기본 키 (Primary Key)
    user_id = Column(Integer, primary_key=True, index=True)

    # 사용자 이름
    username = Column(String, nullable=False)

    # 사용자 이메일, 고유값 (Unique)
    email = Column(String, unique=True, nullable=False)

    # 사용자 비밀번호 (소셜 로그인 사용 시 NULL 가능)
    password = Column(String)

    # 소셜 로그인 제공자 (카카오, 구글, 애플 중 하나)
    provider = Column(Enum('kakao', 'google', 'apple', name='provider_enum'), nullable=False)

    # 각 소셜 제공자가 주는 유니크한 ID
    provider_id = Column(String, unique=True, nullable=False)

    # 프로필 이미지 URL
    profile_image_url = Column(String)

    # 사용자 프로필 설명
    bio = Column(Text)

    # 사용자 전화번호
    phone_number = Column(String(20))

    # 사용자 상태 (활성, 비활성, 차단)
    status = Column(Enum('active', 'inactive', 'blocked', name='status_enum'), default='active')

    # 마지막 로그인 시간
    last_login = Column(TIMESTAMP)

    # 이메일 인증 여부
    email_verified = Column(Boolean, default=False)

    # 생성 시간
    created_at = Column(TIMESTAMP, default='now()')

    # 수정 시간
    updated_at = Column(TIMESTAMP, default='now()')

    # 관계 정의 (한 사용자 여러 게시글)
    posts = relationship("Post", back_populates="user")

    # 관계 정의 (한 사용자 여러 댓글)
    comments = relationship("Comment", back_populates="user")

    # 관계 정의 (한 사용자 여러 게시글 좋아요)
    post_likes = relationship("PostLike", back_populates="user")

    # 관계 정의 (한 사용자 여러 댓글 좋아요)
    comment_likes = relationship("CommentLike", back_populates="user")

    # 관계 정의 (한 사용자 하나의 프로필)
    profile = relationship("Profile", back_populates="user", uselist=False)

    # 관계 정의 (한 사용자 여러 공유)
    shares = relationship("Share", back_populates="user")

# Post 테이블을 나타내는 클래스
class Post(Base):
    __tablename__ = "posts"

    # 기본 키 (Primary Key)
    post_id = Column(Integer, primary_key=True, index=True)

    # 외래 키 (Foreign Key), 게시글 작성자와 연결
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # 게시글 제목
    title = Column(String)

    # 게시글 내용
    content = Column(Text)

    # 게시글 공개 범위 (공개, 비공개, 친구)
    visibility = Column(Enum('public', 'private', 'friends', name='visibility_enum'), default='public')

    # 삭제 여부 (소프트 삭제를 위한 필드)
    is_deleted = Column(Boolean, default=False)

    # 생성 시간
    created_at = Column(TIMESTAMP, default='now()')

    # 수정 시간
    updated_at = Column(TIMESTAMP, default='now()')

    # 관계 정의 (게시글 작성자)
    user = relationship("User", back_populates="posts")

    # 관계 정의 (한 게시글 여러 이미지)
    post_images = relationship("PostImage", back_populates="post")

    # 관계 정의 (한 게시글 여러 댓글)
    comments = relationship("Comment", back_populates="post")

    # 관계 정의 (한 게시글 여러 좋아요)
    post_likes = relationship("PostLike", back_populates="post")

    # 관계 정의 (한 게시글 여러 공유)
    shares = relationship("Share", back_populates="post")

# PostImage 테이블을 나타내는 클래스
class PostImage(Base):
    __tablename__ = "post_images"

    # 기본 키 (Primary Key)
    image_id = Column(Integer, primary_key=True, index=True)

    # 외래 키 (Foreign Key), 게시글과 연결
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)

    # 이미지 URL
    image_url = Column(String, nullable=False)

    # 이미지 순서 (게시글 내 이미지 순서)
    order = Column(Integer)

    # 이미지 대체 텍스트 (alt text)
    alt_text = Column(String)

    # 생성 시간
    created_at = Column(TIMESTAMP, default='now()')

    # 관계 정의 (게시글)
    post = relationship("Post", back_populates="post_images")

# Comment 테이블을 나타내는 클래스
class Comment(Base):
    __tablename__ = "comments"

    # 기본 키 (Primary Key)
    comment_id = Column(Integer, primary_key=True, index=True)

    # 외래 키 (Foreign Key), 게시글과 연결
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)

    # 외래 키 (Foreign Key), 댓글 작성자와 연결
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # 외래 키 (Foreign Key), 부모 댓글과 연결 (대댓글 기능)
    parent_comment_id = Column(Integer, ForeignKey("comments.comment_id"))

    # 댓글 내용
    content = Column(Text, nullable=False)

    # 삭제 여부 (소프트 삭제를 위한 필드)
    is_deleted = Column(Boolean, default=False)

    # 댓글 깊이 (0: 최상위 댓글, 1: 대댓글)
    depth = Column(Integer, default=0)

    # 생성 시간
    created_at = Column(TIMESTAMP, default='now()')

    # 수정 시간
    updated_at = Column(TIMESTAMP, default='now()')

    # 관계 정의 (게시글)
    post = relationship("Post", back_populates="comments")

    # 관계 정의 (사용자)
    user = relationship("User", back_populates="comments")

    # 관계 정의 (부모 댓글)
    parent = relationship("Comment", back_populates="children", remote_side=[comment_id])

    # 관계 정의 (대댓글들)
    children = relationship("Comment", back_populates="parent", remote_side=[parent_comment_id])

    # 관계 정의 (댓글 좋아요들)
    comment_likes = relationship("CommentLike", back_populates="comment")

# PostLike 테이블을 나타내는 클래스
class PostLike(Base):
    __tablename__ = "post_likes"

    # 기본 키 (Primary Key)
    like_id = Column(Integer, primary_key=True, index=True)

    # 외래 키 (Foreign Key), 게시글과 연결
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)

    # 외래 키 (Foreign Key), 사용자와 연결
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # 생성 시간
    created_at = Column(TIMESTAMP, default='now()')

    # 관계 정의 (게시글)
    post = relationship("Post", back_populates="post_likes")

    # 관계 정의 (사용자)
    user = relationship("User", back_populates="post_likes")

# CommentLike 테이블을 나타내는 클래스
class CommentLike(Base):
    __tablename__ = "comment_likes"

    # 기본 키 (Primary Key)
    like_id = Column(Integer, primary_key=True, index=True)

    # 외래 키 (Foreign Key), 댓글과 연결
    comment_id = Column(Integer, ForeignKey("comments.comment_id"), nullable=False)

    # 외래 키 (Foreign Key), 사용자와 연결
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # 생성 시간
    created_at = Column(TIMESTAMP, default='now()')

    # 관계 정의 (댓글)
    comment = relationship("Comment", back_populates="comment_likes")

    # 관계 정의 (사용자)
    user = relationship("User", back_populates="comment_likes")

# Profile 테이블을 나타내는 클래스
class Profile(Base):
    __tablename__ = "profiles"

    # 기본 키 (Primary Key)
    profile_id = Column(Integer, primary_key=True, index=True)

    # 외래 키 (Foreign Key), 사용자와 연결
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # 프로필 이미지 URL
    profile_image_url = Column(String)

    # 프로필 설명
    bio = Column(Text)

    # 웹사이트 URL
    website_url = Column(String)

    # 위치 정보
    location = Column(String)

    # 생년월일
    birthdate = Column(Date)

    # 성별
    gender = Column(Enum('male', 'female', 'other', name='gender_enum'))

    # 생성 시간
    created_at = Column(TIMESTAMP, default='now()')

    # 수정 시간
    updated_at = Column(TIMESTAMP, default='now()')

    # 관계 정의 (사용자)
    user = relationship("User", back_populates="profile")

# Share 테이블을 나타내는 클래스
class Share(Base):
    __tablename__ = "shares"

    # 기본 키 (Primary Key)
    share_id = Column(Integer, primary_key=True, index=True)

    # 외래 키 (Foreign Key), 게시글과 연결
    post_id = Column(Integer, ForeignKey("posts.post_id"), nullable=False)

    # 외래 키 (Foreign Key), 사용자와 연결
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # 공유된 대상 (예: 이메일 주소, 소셜 미디어 계정)
    shared_with = Column(String)

    # 공유된 플랫폼 (예: 카카오톡, 이메일 등)
    platform = Column(String)

    # 공유된 시간
    shared_at = Column(TIMESTAMP, default='now()')

    # 관계 정의 (게시글)
    post = relationship("Post", back_populates="shares")

    # 관계 정의 (사용자)
    user = relationship("User", back_populates="shares")
