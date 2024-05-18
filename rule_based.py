import re
import string
def get_loaivanban(text):
    print(text[0:500])
    rows = text.split("\n")
    rows = [e.strip().lower() for e in rows if len(e.strip())>0]
    rows = rows[0:20]
    if "Chỉ thị".lower() in rows:
        return "Chỉ thị"
    elif "Luật".lower() in rows:
        return "Luật"
    elif "Nghị định".lower() in rows:
        return "Nghị định"
    elif "Quyết định".lower() in rows:
        return "Quyết định"
    elif "Thông tư".lower() in rows:
        return "Thông tư"
    elif "Thông tư liên tịch".lower() in rows:
        return "Thông tư liên tịch"
    else:
        return "Không xác định"

def get_co_quan_ban_hanh(text):
    rows = text.split("\n")
    rows = [e.strip().lower() for e in rows if len(e.strip())>0]
    co_quan = rows[0].split("  ")[0].strip()
    co_quan = co_quan.translate(str.maketrans('', '', string.punctuation))
    return co_quan.title()

def get_doi_tuong_ap_dung(text):
    rows = text.split("\n\n")
    rows = [e.strip().lower() for e in rows if len(e.strip())>0]
    for i in range(len(rows)):
        if ("đối tượng áp dụng" in rows[i]) and len(rows[i].split())<8:
            return rows[i+1]
    return "Không xác định"

