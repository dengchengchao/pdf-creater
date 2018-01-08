# -*-coding:utf-8-*-
# Author:Citron

'''
   By parsing the XML result returned by ABBYY OCR,
      The text is pasted in the upper layer of the PDF
'''

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdf_parser_baidu import pdf_parser
import define
import logging
import log
import sys
import os

_FONT_NAME_='myFont'
_FONT_STYLE_='simsun.ttc'
pdfmetrics.registerFont(TTFont(_FONT_NAME_,_FONT_STYLE_))

class xml2pdf:
    def __init__(self,image_path,xml_path,pdf_path):
        '''
        :param image_path:图片的路径
        :param xml_path: xml文件的路径
        :param pdf_path:生成的pdf路劲
        '''
        try:
            self.parser=pdf_parser(xml_path)
            self.log_info("parsing")
            self.image_path=image_path
            self.pdf_path=pdf_path
            self.page_height=self.parser.size_height
            self.log_info("image height：%s"%(self.page_height))
            self.page_width=self.parser.size_width
            self.log_info("image width：%s"%(self.page_width))
        except BaseException as e :
           self.log_error(e)



    def xml2pdf(self):
        try:
            canva=canvas.Canvas(self.pdf_path,pagesize=(self.page_width,self.page_height))
            for index in range(0,len(self.parser.block_list)):
                 text_obj=self.init_text_object(self.parser.block_list[index],canva)
                 canva.drawText(text_obj)
            canva.drawImage(self.image_path,0,0)
            canva.showPage()
            canva.save()
            return define.status_success
        except BaseException as e :
           self.log_error(e)
           return define.status_error


    def init_text_object(self, draw_block, canva):
        deviation=draw_block.char_size*0.2  #误差
        text_obj = canva.beginText()
        text_obj.setFont(_FONT_NAME_, draw_block.char_size)
        text_obj.setHorizScale(
            100 * (draw_block.last_point+deviation - draw_block[0].point.left) / canva.stringWidth(
                draw_block.char_line, _FONT_NAME_, draw_block.char_size))
        text_obj.setTextOrigin(draw_block.begin_point.left-deviation, self.page_height - draw_block.begin_point.bottom)
        text_obj.textLine(draw_block.char_line)
        self.log_info("""
                      [draw_block info]: 
                      text :%s
                      char_size：%s
                      point:%s,%s
                      property:%s
                      """ % (draw_block.char_line , str(draw_block.char_size) , str(draw_block.begin_point.left) , str(self.page_height - draw_block.begin_point.bottom),draw_block.property))
        return text_obj

    #通用信息记录
    def log_info(self,msg):
        logger=logging.getLogger(__name__)
        logger.info(msg)

    #错误信息记录
    def log_error(self,msg):
        logger=logging.getLogger(__name__)
        logger.error(msg)
        print(define.status_error)

#log.setup_logging()
# start = time.clock()
#xml2pdf("C://Users//Citron//Desktop//pdf//result.jpg",'C://Users//Citron//Desktop//pdf//result.xml','C://Users//Citron//Desktop//pdf//result.pdf').xml2pdf()
# end = time.clock()
#logger = logging.getLogger(__name__)
#logger.info("success,run time：%s" % (end - start))


def check_file_exit(file_path):
    if  os.path.exists(file_path):return True
    logger = logging.getLogger(__name__)
    print(file_path+ "  not exists")
    logger.error(file_path+" not exists")
    return  False



if __name__=='__main__':
    if len(sys.argv) !=4:
        print("""Error Parameter: You should  pass parameter like this :image_path,  xml_path,  pdf_save_path
             """)
        print(define.status_error)
    image_path=sys.argv[1]
    xml_path=sys.argv[2]
    pdf_path = sys.argv[3]
    if (check_file_exit(image_path) and check_file_exit(xml_path)):
       result=xml2pdf(image_path,xml_path,pdf_path).xml2pdf()
       print(result)





