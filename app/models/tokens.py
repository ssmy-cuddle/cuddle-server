from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from . import Base

class Token(Base):
    __tablename__ = "tokens"

    session_id = Column(Integer, primary_key=True, autoincrement=True)  # 세션 ID (pk)
    uid = Column(String(50), ForeignKey("users.uid"), nullable=False)  # 사용자 ID (fk)
    access_token = Column(Text, nullable=False)  # 액세스 토큰
    refresh_token = Column(Text, nullable=False)  # 리프레시 토큰
    provider = Column(String(50))  # 제공자 정보 (예: 자체 로그인, 구글, 페이스북 등)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)  # 생성 일자 (기본값: 현재 시간)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)  # 수정 일자 (기본값: 현재 시간)
    
    users = relationship("User", back_populates="tokens")  # 반려동물과의 관계 설정