from transformers import pipeline
from app.utils import *
#from rule_based import *
import json
from tqdm import tqdm
from app.log import LoggingDebug

logger = LoggingDebug("/home/vdc/project/nlp/PLVB/logs")

collect = False
if collect:
    fileProcessedFile = "/home/vdc/project/nlp/PLVB/datasets/fileUsed.json"
    with open(fileProcessedFile,"r",encoding="utf-8") as fr:
        fileProcessed = json.load(fr)

    collectNewDataFile = "/home/vdc/project/nlp/PLVB/datasets/collectNewData.json"
    with open(collectNewDataFile,"r",encoding="utf-8") as fr:
        collectNewData = json.load(fr)
    collectNewData = collectNewData["files"]

labelMapFile = "/home/vdc/project/nlp/PLVB/datasets/labelMapping.json"
with open(labelMapFile,"r",encoding="utf-8") as fr:
    labelMap = json.load(fr)

tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512}
cls_pipe = pipeline("text-classification",model="/home/vdc/project/nlp/PLVB/weights/v1_2000_epochs",**tokenizer_kwargs)
#cls_pipe = pipeline("text-classification",model="/home/vdc/project/nlp/PLVB/weights/v1_400_epochs",**tokenizer_kwargs)


def predict(tmp_file):
    #filename = tmp_file.name.split("___")[-1]
    #logger.info("got input file: " + filename)

    text = None
    if tmp_file is not None:
        try:
            text = read_file(tmp_file)
        except Exception as err:
            print("Exception:",err)
            #logger.error("Can't read this document: " + filename)
            return None, None, None, None, None, None,None
    else:
        return None, None, None, None, None, None,None
    
    if text == "" or text == None:
        #logger.error("Can't read this document: " + filename)
        return None, None, None, None, None, None,None
    
    #update new text
    '''
    if collect:
        check = {"fileName": filename}
        if check not in fileProcessed and check not in collectNewData:
            collectNewData.append(check)
            with open("/home/vdc/project/nlp/PLVB/datasets/collectNewData.json","r+",encoding="utf-8") as fw:
                file_data = json.load(fw)
                textfile = {"fileName": filename, "text":text}
                file_data["files"].append(check)
                file_data["textfile"].append(textfile)
                fw.seek(0)
                json.dump(file_data,fw, indent=2,ensure_ascii=False)
    '''

    outlabel = cls_pipe(text)[0]["label"]
    # Map ma cong viec vs phong ban
    notmap = True
    for e in tqdm(labelMap):
        if e["Mã Công việc"] == outlabel:
            dvcc = e["Phòng ban"]
            ndcv = e["Nội dung công việc"]
            sp = e["Sản phẩm"]
            pt = e["Phụ trách"]
            th = e["Thực hiện"]
            ph = e["Phối hợp"]
            #logger.info("file: " + filename + f': Mã công việc[{outlabel}]')
            notmap = False
    if notmap:
        logger.error("Can't map Mã công việc: " + outlabel)
        return None, outlabel, None, None, None, None,None

    return dvcc, outlabel, ndcv, sp, pt, th,ph