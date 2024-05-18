import glob
import os
from pdfminer.pdfpage import PDFPage
from utils import *
from .findSoKyHieu import cut_text
import unicodedata
from pathlib import Path

def get_pdf_searchable_pages(fname):
    searchable_pages = []
    non_searchable_pages = []
    page_num = 0
    pdf_layer_type = None
    
    ### PDF có thể search được scan từ text, là type 2
    ### PDF không thể search được scan từ img, là type 1
    with open(fname, 'rb') as file:
        for page in PDFPage.get_pages(file):
            page_num += 1
            if 'Font' in page.resources.keys():
                searchable_pages.append(page_num)
            else:
                non_searchable_pages.append(page_num)

    if page_num > 0:
        if len(searchable_pages) == 0:
            pdf_layer_type = 1
            print("Document '{fname}' has {page_num} page(s). "
                    "Complete document is non-searchable")
        elif len(non_searchable_pages) == 0:
            pdf_layer_type = 2
            print("Document '{fname}' has {page_num} page(s). "
                    "Complete document is searchable")
        else:
            print("searchable_pages : {searchable_pages}")
            print("non_searchable_pages : {non_searchable_pages}")
    else:
        print("Not a valid document")

    return pdf_layer_type

def nameInclude_Signed(files):
    Files = []
    for file in files:
        if os.path.splitext(file)[0][-7:] == "_Signed":
            Files.append(file)
            
    if len(Files) < 1:
        Files.append(files[0])
    return Files

def getPdfFile(files):
    Files = []
    for file in files:
        if os.path.splitext(file)[1] == ".pdf":
            Files.append(file)
    return Files

def getTexts(files):
    texts = []
    for file in files:
        ret = get_pdf_searchable_pages(file)
        text = ""
        if ret == 2:
            print("file pdf is 2 layer")
            try:
                text = read_file(file)
                if text is None or len(text.strip())==0:
                    print("text is None or len = 0:",file_path)
                    continue
            except Exception as err:
                print(err)
                continue
        else:
            print("file pdf is 1 layer")
            text = ""

        text  = unicodedata.normalize('NFC', text)###
        texts.append([text,file])
    return texts

def compareSokyHieu(texts, _sokyhieu):
    Texts = []
    for text in texts:
        sokyhieu = cut_text(text[0])
        print("sokyhieu:",sokyhieu)
        print("_sokyhieu:",_sokyhieu)
        if sokyhieu == _sokyhieu:
            Texts.append(text)
            print("sokyhieu:",sokyhieu)
    if len(Texts) < 1:
        Texts.append(texts[0])
    return Texts


def getMainFile(files, info):
    #step1 - get file pdf
    files = getPdfFile(files)
    if len(files) > 0:
        if len(files) > 1:
            #step2 - check name of file include string "_Signed"
            files = nameInclude_Signed(files)
              
        # step3 - get text of pdf files
        texts = getTexts(files)
        if len(texts) >0:
            # step4 - check so ky hieu
            if len(texts) > 1:
                texts = compareSokyHieu(texts,info["số ký hiệu"])                   
   
            #mainFile = texts[0][1]
            #text = texts[0][0]
            #print("mainFile:",texts[0][1])
            return texts[0]
    return None, None

if __name__ == "__main__":
    src_files = "source_files/*"
    info = {"số ký hiệu":"20938/QD-BTNMT", "trích yếu":""}
    files = [f for f in glob.glob(src_files)]
    print("listFiles:",files)

    text, file = getMainFile(files)
    print("file:",file)