from sqlalchemy import Column, ForeignKey, String, DateTime, func, Integer, Boolean
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from app.db.base_class import Base
import datetime

if TYPE_CHECKING:
    from .document import Document  # noqa: F401


class History(Base):
    id = Column(String, primary_key=True)
    user_name = Column(String)
    doc_id = Column(String, ForeignKey("document.id"))
    ma_cong_viec_moi = Column(String)
    don_vi_chu_tri_moi = Column(String)
    ma_cong_viec_cu = Column(String)
    don_vi_chu_tri_cu = Column(String)
    created_at = Column(DateTime,  default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    document = relationship("Document", back_populates="history")

    def to_json(self):
        return {
            "id": self.id,
            "doc_id": self.ten_van_ban,
            "don_vi_chu_tri_moi": self.don_vi_chu_tri,
            "ma_cong_viec_moi": self.ma_cong_viec,
            "noi_dung_cong_viec": self.noi_dung_cong_viec,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "don_vi_chu_tri_cu": self.don_vi_chu_tri_cu,
            "ma_cong_viec_cu": self.ma_cong_viec_cu
        }
