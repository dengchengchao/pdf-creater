#!/usr/bin/python
#-*-coding:utf-8-*-
#Author:Citron
'''
     Parsing XML files to generate pdf_xmler object
'''
from pdf_xmler import pdf_xmler
from pdf_xmler import point
from pdf_xmler import pdf_list
import xml.etree.ElementTree as ET


#define  xml tag
tag_forward='{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}'
tag_formatting='formatting'
tag_charParams='charParams'
tag_charRecs='charRecVariants'
tag_charRec='charRecVariant'
tag_line='line'
class pdf_parser:
    def __init__(self,xml_path):
        self.root=ET.parse(xml_path).getroot()
        self.xml_list=[]
        self.init_pdf_xmler()


    def init_pdf_xmler(self):
        node_line_list=self.get_line_list(self.root)
        for node_line in node_line_list:
            line_point=self.get_point(node_line)
            line_pdf_list=pdf_list(point)
            node_format_list=self.get_formatting_list(node_line)
            for node_format in node_format_list:
                node_charParams=self.get_charParams_list(node_format)
                text_point=self.get_point(node_charParams)
                text=self.get_charRec_text(node_charParams)
                size=node_charParams.get('meanStrokeWidth')
                xmler=pdf_xmler(text_point,text,size)
                line_pdf_list.extend(xmler)
            xml_list.extend(line_pdf_list)


    def get_point(self,node_line):
        top=node_line.get('t')
        bottom=node_line.get('b')
        left=node_line.get('l')
        right=node_line.get('r')
        return point(top,bottom,left,right)


    def get_line_list(self,father_node):
        return father_node.iter(tag_forward+tag_line)

    def get_formatting_list(self,father_node):
        return father_node.findall(tag_forward+tag_formatting)

    def get_charParams_list(self,father_node):
        return father_node.findall(tag_forward+tag_charParams)

    def get_charRec_text(self,father_node):
        return father_node.finda(tag_forward+tag_charParams).find(tag_forward+tag_charRec).text




