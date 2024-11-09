from sqlalchemy import Column, String, Integer
from . import Base

class postLikes(Base):
    __tablename__ = "postLikes"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    post_id = Column(String(100), nullable=False) 
    uid = Column(String(50), nullable=False) 

