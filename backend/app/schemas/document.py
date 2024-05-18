from typing import Optional, Any, List

from pydantic import BaseModel, EmailStr, ValidationError, validator
from fastapi import HTTPException
import datetime


class DocumentBase(BaseModel):
    id: Optional[str]
    ten_van_ban: Optional[str]
    don_vi_chu_tri: Optional[str]
    ma_cong_viec: Optional[str]
    noi_dung_cong_viec: Optional[str]
    phoi_hop: Optional[str]
    nguoi_phu_trach: Optional[str]
    update_by: Optional[str]
    upload_by: Optional[str]
    ten_file: Optional[str]
    request_id: Optional[str]
    file_path: Optional[str]
    don_vi_chu_tri_cu: Optional[str]
    ma_cong_viec_cu: Optional[str]
    san_pham: Optional[str]

    class Config:
        orm_mode = True


class DocumentCreate(DocumentBase):
    pass


class DocumentOutput(DocumentBase):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class DocumentUpdate(DocumentBase):
    updated_at: Optional[datetime.datetime]
