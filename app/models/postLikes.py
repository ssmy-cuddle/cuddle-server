from sqlalchemy import Column, String, Integer, TIMESTAMP
from . import Base
from datetime import datetime

class PostLike(Base):
    __tablename__ = "postLikes"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    post_id = Column(String(100), nullable=False) 
    uid = Column(String(50), nullable=False) 
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # 생성 시간

