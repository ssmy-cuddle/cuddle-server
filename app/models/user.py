from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    uid = Column(String(50), primary_key=True)  # 사용자가 입력한 uid
    user_name = Column(String(50), nullable=False)  # 사용자 이름
    email = Column(String(100), unique=True, nullable=False)  # 이메일 주소
    password = Column(String(64), nullable=False)  # SHA256 해시된 비밀번호
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # 생성 시간
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)  # 업데이트 시간
    status = Column(Integer, nullable=False, default=1)  # 사용자 상태 (1: 활성, 0: 비활성)