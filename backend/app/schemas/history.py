from typing import Optional, Any, List

from pydantic import BaseModel, EmailStr, ValidationError, validator
from fastapi import HTTPException
import datetime
from .document import DocumentOutput


class HistoryBase(BaseModel):
    id: Optional[str]
    doc_id: str
    don_vi_chu_tri_moi: Optional[str]
    ma_cong_viec_moi: Optional[str]
    don_vi_chu_tri_cu: Optional[str]
    ma_cong_viec_cu: Optional[str]

    class Config:
        orm_mode = True
class HistoryCreate(HistoryBase):
    pass


class HistoryOutput(HistoryBase):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    document: Optional[DocumentOutput]

class HistoryUpdate(HistoryBase):
    pass