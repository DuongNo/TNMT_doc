from pydantic import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    SERVER_URL: str = "http://localhost:8000"
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:123456@db/poc"
    PROJECT_NAME: str = "POC Smart Document Classification"
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
