from fastapi import FastAPI,  UploadFile, File, Header, Form
from fastapi.responses import FileResponse, StreamingResponse, Response
import aiofiles
import sys

#myFolderPath = '/home/vdc/project/nlp/TNMT/api/'
#sys.path.append(myFolderPath)
from .text_classification import text_classification, getHighLight
from .mainFile import *
import base64

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def check():
    return {"message": "Hello World"}

@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    file_names = [file.filename for file in files]
    print("file_names:",file_names)
    return {"filenames": [file.filename for file in files]}

@app.post("/process")
async def process(
                        files: list[UploadFile],
                        #trichyeu: str = Header(None),
                        sokyhieu: str = Form(...),
                        trichyeu: str = Form(...)
                    ):
    result = 0
    message = "PLVB complete"
    #info = {"số ký hiệu":"20938/QD-BTNMT", "trích yếu":""}
    info = {"số ký hiệu":sokyhieu, "trích yếu":trichyeu}
    print("info:",info)

    #file = [file for file in files if file.filename == "   "][0]
    #print("file_origin:",file.filename)

    file_names = [file.filename for file in files]
    print("file_names:",file_names)

    Files = []
    for file in files:
        path = f"/home/vdc/project/nlp/TNMT/api/output/{file.filename}"
        async with aiofiles.open(path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)  # async write
        Files.append(path)

    text, file_name = getMainFile(Files, info)
    print("mainfile_name:",file_name)
    #with open("ocr.txt", "w") as output_file:
    #    output_file.write(text)

    if text is not None and text != "":
        print("process text classification:")
        macongviec, dvcc, ndcv, sanpham, phutrach, thuchien, phoihop = text_classification(text)
    else:
        print("Dont have text")
        return {"result": str(1)}
    
    print("macongviec:",macongviec)
    print("dvcc:",dvcc)
    print("ndcv:",ndcv)
    print("sanpham:",sanpham)
    pdf_path = f"/home/vdc/project/nlp/TNMT/api/output/out.pdf"
    getHighLight(text, file_name, pdf_path)

    with (open(pdf_path, "rb") as f):
        pdf_content_pdf = base64.b64encode(f.read()).decode()
        
    result = {
                "result": str(result),
                "macongviec": macongviec,
                "donvichucchi": dvcc,
                "noidungcongviec": ndcv,
                "sanpham": sanpham,
                "phutrach": phutrach,
                "thuchien": thuchien,
                "phoihop": phoihop,
                "content": pdf_content_pdf,
                "tomtat":"",
                "message": message
            }
    return result

def decode_to_pdf_file(content):
  pdf_bytes = base64.b64decode(content)	
  with open("decoded_file.pdf", "wb") as file:
    file.write(pdf_bytes)

if __name__ == "__main__":
    file_path = "pdf.txt"
    text = read_file(file_path)
    decode_to_pdf_file(text)