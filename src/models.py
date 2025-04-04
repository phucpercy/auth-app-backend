from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from src.database import Base
from src.config import get_settings


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime, default=datetime.utcnow)


class Session(Base):
  __tablename__ = "sessions"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  expires_at = Column(DateTime,
                      default=lambda: datetime.utcnow() + timedelta(minutes=get_settings().REFRESH_TOKEN_EXPIRE_MINUTES))
