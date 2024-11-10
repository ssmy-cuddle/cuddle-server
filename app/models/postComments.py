from sqlalchemy import Column, String, Integer, TIMESTAMP
from . import Base
from datetime import datetime

class PostComment(Base):
    __tablename__ = "postComments"

    comment_id = Column(Integer, primary_key=True, autoincrement=True) 
    message = Column(String(3000), nullable=False)  
    post_id = Column(String(100), nullable=False)  
    uid = Column(String(50), nullable=False)  # 사용자 ID
    parent_id = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # 생성 시간