import json
from utils import *

### special characters
aSign = ('a', 'á', 'à', 'ạ', 'ả','ã','â','ấ','ầ','ậ','ẩ','ẫ','ă','ắ','ằ','ặ','ẳ','ẵ')
ASign = ('A','Á','À','Ạ','Ả','Ã','Â','Ấ','Ầ','Ậ','Ẩ','Ẫ','Ă','Ắ','Ằ','Ặ','Ẳ','Ẵ')
eSign = ('e','é','è','ẹ','ẻ','ẽ','ê','ế','ề','ệ','ể','ễ')
ESign = ('E','É','È','Ẹ','Ẻ','Ẽ','Ê','Ế','Ề','Ệ','Ể','Ễ')
oSign = ('o', 'ó','ò','ọ','ỏ','õ','ô','ố','ồ','ộ','ổ','ỗ','ơ','ớ','ờ','ợ','ở','ỡ')
OSign = ('O','Ó','Ò','Ọ','Ỏ','Õ','Ô','Ố','Ồ','Ộ','Ổ','Ỗ','Ơ','Ớ','Ờ','Ợ','Ở','Ỡ')
uSign = ('u','ú','ù','ụ','ủ','ũ','ư','ứ','ừ','ự','ử','ữ')
USign = ('U','Ú','Ù','Ụ','Ủ','Ũ','Ư','Ứ','Ừ','Ự','Ử','Ữ')
iSign = ('i', 'í','ì','ị','ỉ','ĩ')
ISign = ('I', 'Í','Ì','Ị','Ỉ','Ĩ')
dSign = ('d','đ')
DSign = ('D','Đ')
ySign = ('y','ý','ỳ','ỵ','ỷ','ỹ')
YSign = ('Y','Ý','Ỳ','Ỵ','Ỷ','Ỹ')

sign = (aSign, ASign , eSign , ESign , oSign , OSign , uSign , USign , iSign, ISign, dSign, DSign, ySign, YSign)

def removeSign4VietnameseString(text):
    for si in sign:
        for i in range(1, len(si)):
            text = text.replace(si[i], si[0])

    return text

    # Nội dung các văn bản đang được lưu trong trường 'text' của file json
def cut_text(text):
    line = text
    result = ''
    list_data = []
    list_data = line.split('\n')

    posSo = 0
    posDau = 0
    for i in range(len(list_data)):
        list_data[i] = removeSign4VietnameseString(list_data[i])
        engData = list_data[i]
        engData = engData.lower()
        if engData.find("so") != -1:
            engData = engData[engData.find("so"):]
            #print(engData)
            break
    
    list_check = engData.split(' ')
    for check in list_check:
        if check.find('/') != -1 or check.find('-') != -1:
            result = check
            result = result.upper()
            result = result.replace('|','')
            result = result.replace('.','')
            if result.find('--') != -1 or len(result) < 3 or len(result) > 25:
                result = ''          

    return result

def cut_text0(file):
    with open(file, encoding='utf8') as file:
        dict_list = json.loads(file.read())

    idx = 0
    results = []
    for dic in dict_list:
        line = dic['text']
        result = ''
        list_data = []
        list_data = line.split('\n')

        posSo = 0
        posDau = 0
        for i in range(len(list_data)):
            list_data[i] = removeSign4VietnameseString(list_data[i])
            engData = list_data[i]
            engData = engData.lower()
            if engData.find("so") != -1:
                engData = engData[engData.find("so"):]
                print(engData)
                break
        
        list_check = engData.split(' ')
        for check in list_check:
            if check.find('/') != -1 or check.find('-') != -1:
                result = check
                result = result.upper()
                result = result.replace('|','')
                result = result.replace('.','')
                if result.find('--') != -1 or len(result) < 3 or len(result) > 25:
                    result = ''          
        results.append(result)
        print(idx)
        idx+=1

    return results

if __name__ == '__main__':
    file = "text_clasification/data/train.json"
    pdf_file = "source/2938-qd-btnmt_Signed.pdf"
    try:
        text = read_file(pdf_file)
        if text is None or len(text.strip())==0:
            print(file_path)
    except Exception as err:
        print(err)
    print(cut_text(text))