import shutil
from tempfile import TemporaryDirectory
from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from pdfminer.pdfpage import PDFPage
#import fitz
from OCR_process.run import ocr_process
import os
from OCR.preprocess_img_OCR import preprocess_rotate_ver2
import cv2

class OCR():
    def __init__(self, detect_weight, recogn_weight) -> None:
        self.detect_weight = detect_weight
        self.recogn_weight = recogn_weight
        # self.PDF_file_input = Path(PDF_file_input)

    def process_ocr(self, PDF_file_input):
        output_result = ''
        tempdir = 'OCR/data_temp/temp-dir'
        # alldir = 'PLVB/page_data'
        # Store all the pages of the PDF in a variable
        image_file_list = []
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)
        # Create a temporary directory to hold our temporary images.
        """
        Part #1 : Converting PDF to images
        """
        pdf_pages = convert_from_path(PDF_file_input, 600)
        # Read in the PDF file at 500 DPI
        # Iterate through all the pages stored above
        for page_enumeration, page in enumerate(pdf_pages, start=1):
            # Create a file name to store the image
            filename = f"{tempdir}/page_{page_enumeration:03}.jpg"
            # filename_all = f"{alldir}/img/{PDF_file.name[:-4]}_page_{page_enumeration:03}.jpg"
            # Save the image of the page in system
            page.save(filename, "JPEG")
            page = cv2.imread(filename)
            page = preprocess_rotate_ver2(page)
            # cv2.imwrite(filename_all, page)
            cv2.imwrite(filename, page)
            image_file_list.append(filename)

        """
        Part #2 - Recognizing text from the images using OCR
        """
        for image_file in image_file_list:
            print('Process...')
            # text = pytesseract.image_to_string(Image.open(image_file), lang='vie')
            # text = text.replace("-\n", "")
            texts = ocr_process(self.detect_weight, self.recogn_weight, image_file, PDF_file_input.name[:-4])
            for text in texts:
                output_result += f'{text}\n'

        shutil.rmtree(tempdir)

        return output_result

if __name__ == "__main__":
    PDF_file_input = '/home/vdc/project/nlp/TNMT/api/37503_Signed.pdf'
    detect_weight = 'OCR/OCR_process/weights/PANNet_best_map.pth'
    recogn_weight = 'OCR/OCR_process/weights/transformerocr.pth'
    ocr = OCR(detect_weight, recogn_weight)
    ### Text output after OCR
    text = ocr.process_ocr(Path(PDF_file_input))
    print(text)
    text_file="ocr.txt"
    with open(text_file, "w") as output_file:
        output_file.write(text)
