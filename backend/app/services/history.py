from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.services.base import BaseService
from app.models import History
from app.schemas import HistoryUpdate, HistoryCreate


class HistoryService(BaseService[History, HistoryCreate, HistoryUpdate]):
    def get_by_user_name_and_doc_id(self, db: Session, user_name: str, doc_id: str, limit: int = 50, skip: int = 0):
        return db.query(History).filter(and_(History.user_name == user_name, History.doc_id == doc_id)).order_by(
            History.created_at.desc()).all()


history = HistoryService(History)
