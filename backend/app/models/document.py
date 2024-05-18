from sqlalchemy import Column, ForeignKey, String, DateTime, func, Integer, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base
import datetime


class Document(Base):
    id = Column(String, primary_key=True)
    ten_van_ban = Column(String)
    don_vi_chu_tri = Column(String)
    san_pham = Column(String)
    ma_cong_viec = Column(String)
    noi_dung_cong_viec = Column(String)
    phoi_hop = Column(String)
    nguoi_phu_trach = Column(String)
    update_by = Column(String)
    request_id = Column(String)
    upload_by = Column(String, index=True)
    ten_file = Column(String)
    file_path = Column(String)
    created_at = Column(DateTime,  default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now())
    don_vi_chu_tri_cu = Column(String)
    ma_cong_viec_cu = Column(String)
    history = relationship("History", back_populates="document")

    def to_json(self):
        return {
            "id": self.id,
            "ten_van_ban": self.ten_van_ban,
            "don_vi_chu_tri": self.don_vi_chu_tri,
            "san_pham": self.san_pham,
            "ma_cong_viec": self.ma_cong_viec,
            "noi_dung_cong_viec": self.noi_dung_cong_viec,
            "phoi_hop": self.phoi_hop,
            "nguoi_phu_trach": self.nguoi_phu_trach,
            "update_by": self.update_by,
            "request_id": self.request_id,
            "upload_by": self.upload_by,
            "ten_file": self.ten_file,
            "file_path": self.file_path,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "don_vi_chu_tri_cu": self.don_vi_chu_tri_cu,
            "ma_cong_viec_cu": self.ma_cong_viec_cu
        }
