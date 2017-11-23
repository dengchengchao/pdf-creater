#!/usr/bin/env python
import reportlab.pdfbase.ttfonts
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from pdf_parser import pdf_parser
from reportlab.lib.units import inch
import string 
import copy
import time
import tools
import datetime
pdfmetrics.registerFont(TTFont('myFont','simsun.ttc'))
 
class xml2pdf:
    def __init__(self,image_path,xml_path,pdf_path):
        start = time.clock()
        self.parser=pdf_parser(xml_path)
        self.image_path=image_path
        self.pdf_path=pdf_path
        self.page_height=self.parser.size_height
        self.page_width=self.parser.size_width 
        print(self.page_height,self.page_width)
        end = time.clock()
        print((end-start))




    def xml2pdf(self):
        canva=canvas.Canvas(self.pdf_path,pagesize=(self.page_width,self.page_height))
        #canva.translate(1,1)   #reset the origin of coordinates
        for block in self.parser.block_list:
             line_text=''
             text_obj=canva.beginText()
             text_obj.setFont('myFont',block.char_size)
             text_obj.setCharSpace(block.char_space)
             text_obj.setTextOrigin(block.line_point.left,self.page_height-block.line_point.bottom)
             for char in block:
                  line_text+=char.text
                  #print(char.text)
             text_obj.textLine(line_text)
             canva.drawText(text_obj)
        canva.drawImage(self.image_path,0,0)
        canva.showPage()
        canva.save()



    # def draw_text(self,canva,line_text):
    #     text_obj.setTextOrigin(first_char.point.left,self.get_height(first_char))
    #     text_obj.textLine(line_text)
    #     canva.drawText(text_obj)
   
    #根据字间距和字体大小获取下一个字应在的坐标
    def set_point_modified(self,char,space,origin_x,origin_y):
        self.forward_char=copy.deepcopy(char)
        self.forward_char.point.left=origin_x+space+char.size 
        


    def point_to_space(self,forward_char,char):
       return char.point.left-forward_char.point.right






    #标点符号需要以top属性为准
    def get_height(self,char):
        if tools.is_punctuation(char.text):
           return self.page_height-(char.point.top)+(char.point.bottom-char.point.top)/2+10
        else:
           return self.page_height-(char.point.top+char.point.bottom)/2-15#-(point.bottom-point.top)/2


xml2pdf("result.jpg",'result.xml','result.pdf').xml2pdf()


