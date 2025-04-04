from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
  """Application settings."""
  APP_NAME: str = "Auth Notification App"
  DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/auth_app")
  SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 3 # 3 minutes
  REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60 # 7 days
  BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

  class Config:
    env_file = ".env"
    case_sensitive = True


@lru_cache()
def get_settings():
  return Settings()