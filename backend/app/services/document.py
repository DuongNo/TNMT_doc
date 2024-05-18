from typing import Any, Dict, List, Union
from app.models.document import Document
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.services.base import BaseService
from app.models import Document
from app.schemas import DocumentUpdate, DocumentCreate, HistoryCreate
from .history import history
import uuid


class DocumentService(BaseService[Document, DocumentCreate, DocumentUpdate]):
    def get_by_user_name(self, db: Session, user_name: str, limit: int = 50, skip: int = 0):
        docs = db.query(Document).filter(and_(Document.upload_by == user_name)).order_by(
            Document.created_at.desc()).offset(skip).limit(limit).all()
        total = db.query(Document).filter(
            and_(Document.upload_by == user_name)).count()
        return docs, total

    # def update(self, db: Session, *, db_obj: Document, obj_in: Union[DocumentUpdate, Dict[str, Any]]) -> Document:
    #     hit = HistoryCreate(
    #         id=str(uuid.uuid4()),
    #         doc_id=db_obj.id,
    #         don_vi_chu_tri_moi=obj_in.don_vi_chu_tri,
    #         ma_cong_viec_moi=obj_in.ma_cong_viec,
    #         don_vi_chu_tri_cu=obj_in.don_vi_chu_tri_cu,
    #         ma_cong_viec_cu=obj_in.ma_cong_viec_cu,
    #         user_name=obj_in.update_by
    #     )
    #     history.create(db=db, obj_in=hit)
    #     print(obj_in.don_vi_chu_tri, obj_in.don_vi_chu_tri_cu)
    #     return super().update(db, db_obj=db_obj, obj_in=obj_in)


document = DocumentService(Document)
