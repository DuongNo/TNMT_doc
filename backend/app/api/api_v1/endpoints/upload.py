from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException,  UploadFile, File, Header
from app import services, models, schemas
from app.api import deps
from app.config import settings
from app.response import ResponseFormat
import uuid
import shutil
import os
import time
from app.plvb import predict

router = APIRouter()
response = ResponseFormat()
ALLOWED_EXTENSIONS = {"xlsx", "xlsm", "pdf", "docx", "csv"}


def fake(files_name, user_name, request_id):
    docs = []
    index = 1
    for file_name in files_name:
        file_name_origin = str(file_name).split("___")[1]
        # pa = "/home/vdc/project/nlp/PLVB/backend/static/input"
        # print("file_name_origin:",file_name_origin)
        # path = os.path.join(pa,file_name_origin)
        # print("path:",path)
        dvcc, outlabel, ndcv, sp, pt, th, ph = predict(file_name)
        docs.append({
            "ten_van_ban": file_name_origin,
            "don_vi_chu_tri": dvcc,
            "san_pham": sp,
            "phoi_hop": ph,
            "noi_dung_cong_viec": ndcv,
            "ma_cong_viec": outlabel,
            "nguoi_phu_trach": pt,
            "request_id": request_id,
            "upload_by": user_name,
            "ten_file": file_name_origin,
            "file_path": file_name
        })
        index += 1
    return docs


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/")
def upload_file(*, db: Session = Depends(deps.get_db), user_name: str = Header(...), files: List[UploadFile] = File(...)):
    print("user_name : ", user_name)
    for file in files:
        if not allowed_file(file.filename):
            raise HTTPException(
                status_code=400, detail="Invalid file extension. Only 'xlsx' and 'xlsm' are allowed.")
    file_paths = []
    for file in files:
        #  step 1: upload file
        unique_filename = str(uuid.uuid4()) + "___" + file.filename
        file_path = os.path.join("static", "input", unique_filename)
        # with open(file_path, "wb") as f:
        #     f.write(await file.read())
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(file_path)
    request_id = str(uuid.uuid4())
    data = fake(files_name=file_paths,
                user_name=user_name, request_id=request_id)
    result = []
    for row in data:
        doc = schemas.DocumentCreate(
            id=str(uuid.uuid4()), **row
        )
        doc_json = services.document.create(db=db, obj_in=doc)
        result.append(doc_json.to_json())
    return response.success(data=result)


@router.post("/text")
def upload_text(*, db: Session = Depends(deps.get_db), text: schemas.UploadText):

    unique_filename = str(uuid.uuid4())+"___"+str(uuid.uuid4()) + ".txt"
    upload_path = f"static/input/{unique_filename}"

    with open(upload_path, "w") as file:
        file.write(text.text)
    request_id = str(uuid.uuid4())
    data = fake(files_name=[upload_path],
                user_name=text.user_name, request_id=request_id)
    result = []
    for row in data:
        doc = schemas.DocumentCreate(
            id=str(uuid.uuid4()), **row
        )
        doc_json = services.document.create(db=db, obj_in=doc)
        result.append(doc_json)
    return {"result": result}
