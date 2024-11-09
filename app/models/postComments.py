from sqlalchemy import Column, String, Integer
from . import Base

class PostComment(Base):
    __tablename__ = "postComments"

    comment_id = Column(Integer, primary_key=True, autoincrement=True) 
    message = Column(String(3000), nullable=False)  
    post_id = Column(String(100), nullable=False)  
    uid = Column(String(50), nullable=False)  # 사용자 ID
    parent_id = Column(Integer)