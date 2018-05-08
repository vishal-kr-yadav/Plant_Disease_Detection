"""Cv pdf parshing """
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument 
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine,LTChar

from marshmallow import Schema, fields
from collections import Counter, defaultdict


"""Object serialization and deserialization"""
class basedSchema(Schema):
    text = fields.Function(lambda obj: obj.get_text())
    x0 = fields.Float()
    x1 = fields.Raw()
    y0 = fields.Raw()
    y1 = fields.Raw()
    height = fields.Raw()
    width = fields.Raw()
    
class boxSchema(basedSchema):
    index = fields.Raw()
    
class textSchema(basedSchema):
    fontname = fields.Method('get_font')

    def get_font(self, obj):
        fonts = []
        if not obj.is_empty():
            for word in obj:
                if isinstance(word, LTChar):
                    fonts.append(word.fontname)
        d = Counter(fonts)
        return max(fonts, key=d.get)
    
textSchema = textSchema()
boxSchema = boxSchema()

#main function
def pdf_miner(fp):
    laparams = LAParams()
    pdf_path = fp
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    text=[]
    # Process each page contained in the document.
    box_data = defaultdict(list)
    text_data = defaultdict(list)


    for i, page in enumerate(PDFPage.create_pages(document)):
        interpreter.process_page(page)
        layout = device.get_result()
        counter = 0
        for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    if isinstance(lt_obj, LTTextBox) and not lt_obj.is_empty():
                        r = boxSchema.dump(lt_obj)
                        box_data['page: '+str(i)+'-'+'Index: '+ str(counter)] = r.data
                        
                        for line in lt_obj:
                            if not line.is_empty():
                                r = textSchema.dump(line)
                                text_data['page: '+str(i)+'-'+'Index: '+ str(counter)].append(r.data)
                        counter += 1
                    else:
                        for line in lt_obj:
                            if not line.is_empty():
                                r = textSchema.dump(line)
                                text_data['page: '+str(i)+'-'+'Index: '+ str(counter)].append(r.data)
                        counter += 1
    return box_data, text_data

if __name__ == "__main__":
    box, text = pdf_miner('tmp/test.pdf')
    print(box)
    print(text)


