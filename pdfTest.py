#!/usr/bin/env python
import reportlab.pdfbase.ttfonts
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab import platypus
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle

pdfmetrics.registerFont(TTFont('myFont','/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'))
def draw_Text(c,space):
   obj=c.beginText()
   obj.setTextOrigin(0,0)
   obj.setFont('myFont',20)
   obj.setCharSpace(space)
   obj.textLines("测一测")
   c.drawText(obj)
   obj=c.beginText()
   obj.setTextOrigin(50,0)
   obj.setFont('myFont',23)
   obj.setCharSpace(space)
   obj.textLines("测一测中国的一个是吧")
   c.drawText(obj)
 
    

def hello():
   c=canvas.Canvas("helloword.pdf")
   draw_Text(c,5)
  # draw_Text(c,50)
   c.showPage()
   c.save()
hello()
