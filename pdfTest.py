#!/usr/bin/env python
import reportlab.pdfbase.ttfonts
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
pdfmetrics.registerFont(TTFont('myFont','/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'))
def hello():
    c=canvas.Canvas("helloword.pdf",pagesize=(2603,3593))
    c.setFont('myFont',57)
    c.translate(0,0)
    c.drawCentredString(779,407,"中国一直是我的家")


    c.showPage()
    c.save()
hello()








































