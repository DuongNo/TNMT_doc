from functools import lru_cache
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI,
                       pool_pre_ping=True, max_overflow=15, pool_size=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
