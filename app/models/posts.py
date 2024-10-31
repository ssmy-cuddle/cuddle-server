from sqlalchemy import Column, String, Integer, TIMESTAMP, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from . import Base
from user import User

class Posts(Base):
    __tablename__ = "posts"

    post_id = Column(String(100), primary_key=True)  # 사용자가 입력한 uid
    uid = Column(String(50), ForeignKey('user.uid'), nullable=False)  # 사용자 ID
    created_at = Column(TIMESTAMP, server_default=func.now())  # 생성 시간
    is_deleted = Column(Boolean, nullable=False, default=False)  # 삭제 여부
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # 업데이트 시간
    post_likes = Column(Integer, nullable=False, default=0)  # 좋아요 수
    post_shares = Column(Integer, nullable=False, default=0)  # 공유 수
    visibility = Column(
        Enum('public', 'private', 'friends', name='visibility_enum'),
        default='public'
    )  # 공개 범위 (public, private, friends)
    title = Column(String(300), nullable=False)  # 게시글 제목
    content = Column(String, nullable=False)  # 게시글 본문

    user = relationship('User', back_populates='posts')
