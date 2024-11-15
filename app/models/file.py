
from sqlalchemy import Column, String, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime

class File(Base):
    __tablename__ = "file"

    file_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(String(500), unique=True, nullable=False)
    file_url = Column(Text, nullable=False)
    uid = Column(String(50), ForeignKey("users.uid"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationship with User model
    users = relationship("User", back_populates="files")