#!/usr/bin/env python
import reportlab.pdfbase.ttfonts
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from pdf_parser import pdf_parser
from reportlab.lib.units import inch
pdfmetrics.registerFont(TTFont('myFont','/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'))
class xml2pdf:
    def __init__(self,image_path,xml_path,pdf_path):
        self.parser=pdf_parser(xml_path)
        self.image_path=image_path
        self.pdf_path=pdf_path
        self.page_height=self.parser.size_height
        self.page_width=self.parser.size_width
        print(self.page_height,self.page_width)
    def xml2pdf(self):
        canva=canvas.Canvas(self.pdf_path,pagesize=(self.page_width,self.page_height))
       # canva.translate(inch,inch)   #reset the origin of coordinates
        for block in self.parser.block_list:
            line_char=""
            for  char in block:
              line_char+=char.char
            self.draw_text(line_char,canva,block[0].size,block.line_point)
        canva.drawImage(self.image_path)
        canva.showPage()
        canva.save()

    def draw_text(self,text,canva,size,point):
        #canva.translate(0,0)   #reset the origin of coordinates
        canva.setFont('myFont',size)
        canva.drawString(point.left,self.get_height(point.top),text)
    def get_height(self,height):
        return self.page_height-height
xml2pdf("1.jpg",'result.xml','result.pdf').xml2pdf()


