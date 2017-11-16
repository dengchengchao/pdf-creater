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
        #canva.translate(1,1)   #reset the origin of coordinates
        for block in self.parser.block_list:
            for  index in range(0,len(block)):
              if(index!=0):
                 self.draw_text(canva,block[index],block[index-1])
              else:
                 self.forward_char=copy.deepcopy(block[0])
        canva.drawImage(self.image_path,0,0)
        canva.showPage()
        canva.save()



    def draw_text(self,canva,char,forward_char):
        #canva.setFont('myFont',size)
        #canva.drawString(point.left,self.get_height(point.top),text)
        text_object=canva.beginText()
        char_space=self.point_to_space(self.forward_char,char)       
        text_object.setCharSpace(char_space)
        origin_x=self.forward_char.point.left 
        origin_y=self.get_height(self.forward_char)
        text_object.setTextOrigin(origin_x,origin_y)
        text_object.setFont('myFont',char.size)
        text_object.textLines(self.forward_char.char+char.char)
        print(self.forward_char.char+char.char)
        self.set_point_modified(char,char_space,origin_x,origin_y)
        canva.drawText(text_object)
   
    #根据字间距和字体大小获取下一个字应在的坐标
    def set_point_modified(self,char,space,origin_x,origin_y):
        self.forward_char=copy.deepcopy(char)
        self.forward_char.point.left=origin_x+space+char.size 
        


    def point_to_space(self,forward_char,char):
       return char.point.left-forward_char.point.right






    #标点符号需要以top属性为准
    def get_height(self,char):
        if self.get_is_punctuation(char.char):
           return self.page_height-(char.point.top)+(char.point.bottom-char.point.top)/2
        else:
           return self.page_height-(char.point.top+char.point.bottom)/2#-(point.bottom-point.top)/2


    def get_is_punctuation(self,char,pun_list=":，、。？《》：！（）【】“”‘’；"+string.punctuation):
       return char in pun_list
xml2pdf("result.jpg",'result.xml','result.pdf').xml2pdf()


