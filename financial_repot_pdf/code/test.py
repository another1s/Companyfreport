import tabula
from pdfminer3.pdfparser import *
from pdfminer3.pdfdocument import *
from pdfminer3.pdfpage import *
from pdfminer3.pdfpage import *
from pdfminer3.pdfinterp import *
from pdfminer3.pdfinterp import *
from pdfminer3.pdfdevice import *
from pdfminer3.layout import *
from pdfminer3.converter import *
# Open a PDF file.
fp = open('../datafolder/ltn20130918379.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
document = PDFDocument(parser)
rsrcmgr = PDFResourceManager()
# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    contains =layout._objs
    for i in contains:
        if isinstance(i, LTTextBoxHorizontal):
            res = i.get_text()
