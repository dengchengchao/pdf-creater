#-*-coding:utf-8-*-
#Author:Citron
'''
     Parsing XML files to generate pdf_xmler object
'''
from pdf_char import pdf_char
from pdf_char import point
from pdf_char import pdf_char_line
from pdf_char import block
import xml.etree.ElementTree as ET

tag_line='line'
tag_char='chars'
tag_page='page'
tag_height='height'
tag_width='width'

class pdf_parser:
    def __init__(self,xml_path):
        self.root=ET.parse(xml_path).getroot()
        self.size_width = 0
        self.size_height = 0
        self.xml_list = []
        self.block_list = []
        self.init_pdf_xmler()
        self.deal_line_to_block()
        self.init_size()



    def init_size(self):
        self.size_width=int(self.root.get(tag_width))
        self.size_height=int(self.root.get(tag_height))



    def init_pdf_xmler(self):
        node_line_list=self.get_text_list(self.root)
        for node_line in node_line_list:    #line
            line_pdf_list = pdf_char_line()
            for nodes in node_line:         #chars
                for node in nodes:          #char
                    text_point=self.get_point(node)
                    text=self.get_charRec_text(node)
                    xmler=pdf_char(text_point,text,max(text_point.bottom-text_point.top,text_point.right-text_point.left))
                    line_pdf_list.append(xmler)
            self.xml_list.append(line_pdf_list)


    def get_text_list(self,father_node):
        if father_node != None:
            return father_node.iter(tag_line)

    def get_point(self,node_line):
        top = node_line.get('t')
        bottom = node_line.get('b')
        left = node_line.get('l')
        right = node_line.get('r')
        return point(top, bottom, left, right)

    def get_charRec_text(self,father_node):
        if father_node!=None:
           return father_node.text.strip()



    def deal_line_to_block(self):
        for line in self.xml_list:
            line_block=block(line)
            for block_node in line_block.block_list:
                self.block_list.append(block_node)

#pdf_parser(r"C:\Users\Citron\Desktop\pdf\result.xml")