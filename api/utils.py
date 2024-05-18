import textract
import io
import re
import unicodedata
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
def read_word(file_path):
    text = textract.process(file_path)
    text = text.decode("utf-8")
    return text
def read_pdf(file_path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(file_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)



    fp.close()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    text = re.sub(r'\n+','\n',text).strip()
    text = re.sub(r'\t+',' ',text).strip()
    text = text.replace("\xa0","")
    text = text.replace("\x0c","")
    text = text.replace(chr(0),"")
    text = text.replace(chr(1),"")
    text = unicodedata.normalize("NFKD", text)
    return text
def read_file(file_path):
    if file_path.lower().endswith(".doc") or file_path.lower().endswith(".docx"):
        text = read_word(file_path)
    elif file_path.lower().endswith(".pdf"):
        text = read_pdf(file_path)
    elif file_path.lower().endswith(".txt"):
        with open(file_path,"r",encoding="utf-8") as fr:
            text = fr.read().strip()
    else:
        text = None
    return text
if __name__ == "__main__":
    file_path = "datasets/files/TTLT 179-2014 Hướng dẫn sử dụng kinh phí cho hoạt động kiểm kê đất đai, lập bản đồ hiện trạng sử dụng đất năm 2014.pdf"
    print(read_pdf(file_path)[0:1000])