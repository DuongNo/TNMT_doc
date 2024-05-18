import json
from utils import *
from tqdm import tqdm
import os
import pandas as pd

dataFolder = "/home/vdc/project/nlp/TNMT/data/dataAll"

def getDataFromExcel():
    df = pd.read_excel("tinh-hinh-xu-ly-van-ban.xlsx",sheet_name="data_labeled", header=0,
                       converters={'File chính':str, 'Mã Công việc':str, 'Đơn vị chủ trì':str, "Trích yếu":str})
    df = df[["File chính","Mã công việc 22/12","ĐƠN VỊ CHỦ TRÌ", "Trích yếu"]]
    df = df[df["File chính"]!="@123!45&9*"]

    all_data = []
    list_file = []
    dict_label = {}
    number_file_notFound = 0
    for idx,row in tqdm(df.iterrows()):
        if pd.isna(row["File chính"]):
            continue
        filenames = row["File chính"].split(";")
        for file in filenames:
            filename = file.strip()
            break
        if pd.isna(row["ĐƠN VỊ CHỦ TRÌ"]):
            continue
        #macongviec = row["Mã công việc 22/12"].split(";")
        #for m in macongviec:
        #    ma = m.strip()
        #    break
        

        filePath = os.path.join(dataFolder,filename)
        if not os.path.isfile(filePath):  
            filePath = os.path.splitext(filePath)[0]+'.txt' 
            if not os.path.isfile(filePath):  
                filePath = os.path.splitext(filePath)[0]+'.doc'
                if not os.path.isfile(filePath):  
                    filePath = os.path.splitext(filePath)[0]+'.docx'
                    if not os.path.isfile(filePath):  
                        filePath = os.path.splitext(filePath)[0]+'.pdf'
                        if not os.path.isfile(filePath):  
                            filePath = os.path.splitext(filePath)[0]+'.PDF'
                            if not os.path.isfile(filePath):
                                list_file.append(filename)
                                number_file_notFound +=1
                                continue       
        
        sample = {"Phòng":row["ĐƠN VỊ CHỦ TRÌ"],"link":filePath, "Trích yếu":row["Trích yếu"]}
        all_data.append(sample)
        #if ma in dict_label:
        #    dict_label[ma] +=1
        #else:
        #    dict_label[ma] =1

    print("total samples:",len(all_data))
    print("total number_file_notFound:",number_file_notFound)
    print("list_file:",list_file)
    print("total samples not a file:",len(list_file))
    #print("dict_label:",dict_label)
    print("len of dict_label:",len(dict_label))

    with open("datasets/data3.json","w",encoding="utf-8") as fw:
        json.dump(all_data,fw, indent=2,ensure_ascii=False)

def getlabelMapping():
    df = pd.read_excel("tinh-hinh-xu-ly-van-ban.xlsx",sheet_name="DONVI-CONGVIEC", header=0,
                       converters={'Mã Công việc-3':str, 'Nội dung công việc':str, 'Phòng ban/Đơn vị':str, 'Sản phẩm':str,
                                   'Phụ trách':str, 'Thực hiện':str, 'Phối hợp':str})
    df = df[["Mã Công việc-3", "Nội dung công việc", "Phòng ban/Đơn vị", "Sản phẩm", "Phụ trách", "Thực hiện", "Phối hợp"]]
    df = df[df["Mã Công việc-3"]!="@123!45&9*"]

    all_data = []
    for idx,row in tqdm(df.iterrows()): 
        if pd.isna(row["Mã Công việc-3"]):
            continue
        
        if pd.isna(row["Nội dung công việc"]):
            row["Nội dung công việc"] = ""

        if pd.isna(row["Phòng ban/Đơn vị"]):
            row["Phòng ban/Đơn vị"] = ""

        if pd.isna(row["Sản phẩm"]):
            row["Sản phẩm"] = ""

        if pd.isna(row["Phụ trách"]):
            row["Phụ trách"] = ""

        if pd.isna(row["Thực hiện"]):
            row["Thực hiện"] = ""

        if pd.isna(row["Phối hợp"]):
            row["Phối hợp"] = ""

        sample = {"Mã Công việc":row["Mã Công việc-3"],"Nội dung công việc":row["Nội dung công việc"], "Phòng ban":row["Phòng ban/Đơn vị"],
                  "Sản phẩm":row["Sản phẩm"], "Phụ trách":row["Phụ trách"], "Thực hiện":row["Thực hiện"], "Phối hợp":row["Phối hợp"]}
        all_data.append(sample)

    with open("datasets/labelMapping.json","w",encoding="utf-8") as fw:
        json.dump(all_data,fw, indent=2,ensure_ascii=False)

def getFileUsed():
    df = pd.read_excel("tinh-hinh-xu-ly-van-ban.xlsx",sheet_name="02. VAN BAN DEN 2023-988", header=0,
                       converters={'File':str})
    df = df[["File"]]
    df = df[df["File"]!="@123!45&9*"]

    all_data = []
    for idx,row in tqdm(df.iterrows()):
        if pd.isna(row["File"]):
            continue
        fileName = os.path.splitext(row["File"])[0]
        sample = {"filename":fileName}
        all_data.append(sample)
    with open("datasets/fileUsed.json","w",encoding="utf-8") as fw:
        json.dump(all_data,fw, indent=2,ensure_ascii=False)

if __name__ == "__main__":
    getDataFromExcel()
    #getlabelMapping()
    #getFileUsed()