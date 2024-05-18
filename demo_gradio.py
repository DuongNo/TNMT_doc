import gradio as gr
from transformers import pipeline
from utils import *
import tempfile
from rule_based import *
import json
from tqdm import tqdm
from log import LoggingDebug

logger = LoggingDebug("./logs")

collect = False
if collect:
    fileProcessedFile = "datasets/fileUsed.json"
    with open(fileProcessedFile,"r",encoding="utf-8") as fr:
        fileProcessed = json.load(fr)

    collectNewDataFile = "datasets/collectNewData.json"
    with open(collectNewDataFile,"r",encoding="utf-8") as fr:
        collectNewData = json.load(fr)
    collectNewData = collectNewData["files"]

labelMapFile = "datasets/labelMapping.json"
with open(labelMapFile,"r",encoding="utf-8") as fr:
    labelMap = json.load(fr)

tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512}
#cls_pipe = pipeline("text-classification",model="outputs/IDLV",**tokenizer_kwargs)
cls_pipe = pipeline("text-classification",model="weights/v1_400_epochs",**tokenizer_kwargs)
def predict(tmp_file, text):
    filename = tmp_file.name.split("/")[-1]
    logger.info("got input file: " + filename)

    if text=="":
        text = None
    if tmp_file is not None:
        try:
            text = read_file(tmp_file.name)
        except Exception as err:
            print("Exception:",err)
            logger.error("Can't read this document: " + filename)
            return None, None, None, None, None, None,None
    else:
        return None, None, None, None, None, None,None
    
    if text == "" or text == None:
        gr.Error("Can't read this document")
        logger.error("Can't read this document: " + filename)
        return None, None, None, None, None, None,None
    
    #update new text
    if collect:
        check = {"fileName": filename}
        if check not in fileProcessed and check not in collectNewData:
            collectNewData.append(check)
            with open("datasets/collectNewData.json","r+",encoding="utf-8") as fw:
                file_data = json.load(fw)
                textfile = {"fileName": filename, "text":text}
                file_data["files"].append(check)
                file_data["textfile"].append(textfile)
                fw.seek(0)
                json.dump(file_data,fw, indent=2,ensure_ascii=False)

    #outlabel = cls_pipe(text)[0]["label"]
    output = cls_pipe(text)
    output = output[0]
    outlabel = output["label"]
    #loai_van_ban = get_loaivanban(text)
    #co_quan = get_co_quan_ban_hanh(text)
    #doi_tuong = get_doi_tuong_ap_dung(text)

    # Map ma cong viec vs phong ban
    notmap = True
    for e in tqdm(labelMap):
        if e["Mã Công việc"] == outlabel:
            dvcc = e["Phòng ban"]
            ndcv = e["Nội dung công việc"]
            sp = e["Sản phẩm"]
            pt = e["Phụ trách"]
            th = e["Thực hiện"]
            th = e["Phối hợp"]
            logger.info("file: " + filename + f': Mã công việc[{outlabel}]')
            notmap = False
    if notmap:
        logger.error("Can't map Mã công việc: " + outlabel)
        return None, outlabel, None, None, None, None,None

    return dvcc, outlabel, ndcv, sp, pt, th,th
gradio_ui = gr.Interface(
    fn=predict,
    title="Document Classification",
    description="",
    inputs=[gr.File(type="file",label="Tài liệu"), gr.inputs.Textbox(lines=10, label="Hoặc nhập văn bản tại đây")],
    outputs=[
        gr.outputs.Textbox(label="Đơn vị chủ trì"),
        gr.outputs.Textbox(label="Mã công việc"),    
        gr.outputs.Textbox(label="Nội dung công việc"),
        gr.outputs.Textbox(label="Sản phẩm"),
        gr.outputs.Textbox(label="Phụ trách"),
        gr.outputs.Textbox(label="Thực hiện"),
        gr.outputs.Textbox(label="Phối hợp"),
    ],
)
gradio_ui.launch(server_name="0.0.0.0",server_port=18555)