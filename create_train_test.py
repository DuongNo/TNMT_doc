import json
from utils import *
from tqdm import tqdm
import os
from cut_text import cut_text
import unicodedata
import pandas as pd

data_folder = "/home/vdc/project/nlp/TNMT/DATAOCR"
with open("datasets/data.json","r",encoding="utf-8") as fr:
    data = json.load(fr)
all_data = []
list_file = []
for e in tqdm(data):
    try:
        #file_path = f'datasets/files/{e["link"].split("/")[-1]}'
        #file_path = os.path.join(data_folder, e["link"])
        file_path = e["link"]
        text = read_file(file_path)
        if text is None or len(text.strip())==0:
            print(file_path)
            continue
    except Exception as err:
        print(err)
        list_file.append(e["link"])
        #file_path = os.path.splitext(file_path)[0]+'.txt'
        #print("try read file: ",file_path)
        #try:
        #    text = read_file(file_path)
        #    if text is None or len(text.strip())==0:
        #        print(file_path)
        #        continue
        #except Exception as err:
        #    print(err)
        #    continue
        continue
    
    if pd.isna(e["Phòng"]):
            continue
    text = unicodedata.normalize('NFC', text) 
    text = cut_text(text)
    sample = {'text':text,'label':e["Phòng"]}
    all_data.append(sample)
 
#print("list_file: ",list_file)
print("len(list_file):",len(list_file))
with open("datasets/all_data2.json","w",encoding="utf-8") as fw:
    json.dump(all_data,fw, indent=2,ensure_ascii=False)

from sklearn.model_selection import train_test_split
#train, test = train_test_split(all_data,test_size=0.1, random_state=42)
train = train_test_split(all_data, random_state=42)
with open("datasets/train2.json","w",encoding="utf-8") as fw:
    json.dump(train,fw, indent=2,ensure_ascii=False)
#with open("datasets/test2.json","w",encoding="utf-8") as fw:
#    json.dump(test,fw, indent=2,ensure_ascii=False)