""" ---Document Conversion module
https://stackoverflow.com/questions/26494211/
extracting-text-from-a-pdf-file-using-pdfminer-in-python
user:2930045
https://euske.github.io/pdfminer/programming.html
"""

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

def pdf_to_txt(path: str)->str:
    "#TODO"
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr,
                           laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    with open(path, 'rb') as file:
        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
    text = retstr.getvalue()
    return text
