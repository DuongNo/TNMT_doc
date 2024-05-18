from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import services, models, schemas
from app.api import deps
from app.config import settings
from app.response import ResponseFormat
import uuid
import datetime
router = APIRouter()
response = ResponseFormat()


@router.put("/{doc_id}", response_model=schemas.ResponseModelSingleItem[schemas.DocumentCreate],
            responses={
                422: {"model": schemas.ValidatorErrorResponse},
                400: {"model": schemas.BadRequestResponseModel}
})
def update(*, db: Session = Depends(deps.get_db), doc: schemas.DocumentUpdate, doc_id: str):
    current_doc = services.document.get(db=db, id=doc_id)
    if not current_doc:
        raise HTTPException(status_code=400, detail="Documnet not found !")
    doc.don_vi_chu_tri_cu = current_doc.don_vi_chu_tri
    doc.ma_cong_viec_cu = current_doc.ma_cong_viec
    doc.updated_at = datetime.datetime.now()
    new_doc_update = services.document.update(
        db=db, db_obj=current_doc, obj_in=doc)

    hit = schemas.HistoryCreate(
        id=str(uuid.uuid4()),
        doc_id=current_doc.id,
        don_vi_chu_tri_moi=doc.don_vi_chu_tri,
        ma_cong_viec_moi=doc.ma_cong_viec,
        don_vi_chu_tri_cu=doc.don_vi_chu_tri_cu,
        ma_cong_viec_cu=doc.ma_cong_viec_cu,
        user_name=current_doc.update_by
    )
    services.history.create(db=db, obj_in=hit)
    return response.success(data=new_doc_update.to_json())


@router.get("/", response_model=schemas.ResponseModelListItemWithPagination[schemas.DocumentCreate],
            responses={
                422: {"model": schemas.ValidatorErrorResponse},
                400: {"model": schemas.BadRequestResponseModel}
})
def get_list(db: Session = Depends(deps.get_db),
             skip: int = 0,
             limit: int = 100,
             user_name: str = None
             ):
    """Get list documents by user

    Args:
        db (Session, optional): 
        skip (int, optional): Number records to skip. Defaults to 0.
        limit (int, optional): Number records to limit. Defaults to 100.
        user_name(str, optional): user name

    Returns:
        List[Design]: List Documents
    """
    docs, total = services.document.get_by_user_name(
        db, skip=skip,
        limit=limit,
        user_name=user_name
    )
    return response.success(data={
        "data": docs,
        "paging": {
            "limit": limit,
            "skip": skip,
            "total": total
        }
    })


@router.get("/{id}",
            response_model=schemas.ResponseModelSingleItem[schemas.DocumentCreate],
            responses={
                422: {"model": schemas.ValidatorErrorResponse},
                400: {"model": schemas.BadRequestResponseModel}
            })
def get_by_id(db: Session = Depends(deps.get_db), id: str = None):
    """Get by id

    Args:
        db (Session, optional): Session of db. Defaults to Depends(deps.get_db).
        id (str, optional): id of category. Defaults to None.

    Returns:
        Document Id : infomation of that DesignCategory
    """
    doc = services.document.get(
        db, id=id)
    if not doc:
        raise HTTPException(
            status_code=400, detail="Document not found !")
    return response.success(data=doc)


@router.post("/", response_model=schemas.ResponseModelSingleItem[schemas.DocumentCreate],
             responses={
    422: {"model": schemas.ValidatorErrorResponse},
    400: {"model": schemas.BadRequestResponseModel}
})
def create(*,
           db: Session = Depends(deps.get_db),
           doc: schemas.DocumentCreate):
    doc.id = str(uuid.uuid4())
    doc_created = services.document.create(db=db, obj_in=doc)
    return response.success(data={
        "data":  doc_created.to_json()
    })
