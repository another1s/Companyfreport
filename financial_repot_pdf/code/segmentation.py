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


class Narcissus:
    def __init__(self):
        self.star_platinum = list()   # store string
        self.golden_experience = list()  # store bbox
        self.stone_free = list()     # font_type
        self.the_world = list()    # label
        self.crazy_diamond = dict()

    def filtering(self, rawdata):
        for onepiece in rawdata:
            if isinstance(onepiece, LTTextBoxHorizontal):
                self.golden_experience.append(onepiece.bbox)
                self.star_platinum.append(onepiece.get_text())
                self.stone_free.append(self.get_font_type(onepiece))
            elif isinstance(onepiece, LTTextBoxVertical):
                pass
            else:
                pass
        self.crazy_diamond['text'] = self.star_platinum
        self.crazy_diamond['bbox'] = self.golden_experience
        self.crazy_diamond['font'] = self.stone_free
        self.the_world = self.differentiate_text_block(self.stone_free, self.star_platinum)
        self.crazy_diamond['label'] = self.the_world
        return self.crazy_diamond

    def get_font_type(self, data):
        font_type = ""
        while(data):
            if isinstance(data, LTChar):
                font_type = data.fontname
                break
            elif isinstance(data._objs, list):
                data = data._objs[0]
            else:
                pass
        return font_type

    def differentiate_text_block(self, fonts, text):
        #  a paragraph followed by a table
        #  a table between two paragraph
        #  a table followed by a paragraph
        # no paragraph but a
        label = list()
        for onepiece in text:
            dot = onepiece.rfind('.')
            if dot == (len(onepiece)-1):    # if period is found at the end of sentence
                label.append(1)
            elif ord(onepiece[dot-1]) in range(65, 90) or ord(onepiece[dot-1]) in range(97, 122): # if period is found behind a character
                label.append(1)
            else:
                label.append(0)
        return label


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
data_collector = Narcissus()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    contents = layout._objs
    page_contents = data_collector.filtering(contents)
