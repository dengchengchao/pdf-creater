#!/usr/bin/env python
import reportlab.pdfbase.ttfonts
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from pdf_parser import pdf_parser
from reportlab.lib.units import inch
pdfmetrics.registerFont(TTFont('myFont','/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
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
        canva.translate(1,1)   #reset the origin of coordinates
        for block in self.parser.block_list:
            line_char=""
            for  char in block:
              line_char+=char.char
              self.draw_text(char.char,canva,char.size,char.point,1)
        canva.drawImage(self.image_path,0,0)
        canva.showPage()
        canva.save()

    def draw_text(self,text,canva,size,point,space):
        #canva.translate(0,self.page_height)   #reset the origin of coordinates
        #canva.setFont('myFont',size)
        #canva.drawString(point.left,self.get_height(point.top),text)
        text_object=canva.beginText()
        text_object.setTextOrigin(point.left,self.get_height(text,point))
        text_object.setFont('myFont',33)
        text_object.setCharSpace(7)
        text_object.textLines(text)
        canva.drawText(text_object)

    def get_height(self,char,point):
        if self.get_is_punctuation(char):
           print("punctuation    "+char)
           return self.page_height-(point.top)+(point.bottom-point.top)/2
        else:
           return self.page_height-(point.top+point.bottom)/2#-(point.bottom-point.top)/2


    def get_is_punctuation(self,char):
        import string
        pun_list=":，、。？《》：！（）【】“”‘’；"+string.punctuation
        return char in pun_list
xml2pdf("result.jpg",'result.xml','result.pdf').xml2pdf()


