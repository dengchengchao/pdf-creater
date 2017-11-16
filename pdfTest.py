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
def hello():
   c=canvas.Canvas("helloword.pdf")
   obj=c.beginText()
   obj.setTextOrigin(0,0)
   obj.setFont('myFont',20)
   obj.setCharSpace(5)
   obj.textLines("测试一下")
   c.drawText(obj)
   c.showPage()
   c.save()
hello()
