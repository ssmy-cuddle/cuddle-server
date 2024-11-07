from sqlalchemy import Column, String, Integer
from . import Base

class postLikes(Base):
    __tablename__ = "postLikes"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 반려동물 ID (pk)
    post_id = Column(String(100), nullable=False)  # 사용자가 입력한 uid
    uid = Column(String(50), nullable=False)  # 사용자 ID

