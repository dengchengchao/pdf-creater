#!/usr/bin/python
# -*-coding:utf-8-*-
# Author:Citron
'''
       Used to save objects generated by parsing XML files

'''
import copy
import tools
import define
import split

# single text text
class pdf_char:
    def __init__(self, point, text, size):
        self.point = point
        self.size = int(size)
        self.text = text


# single line text
class pdf_char_line(list):
    '''
       存储字体大小、字间距相差不大并且连载一起的对象。用于连续的绘画文字
    '''
    def __init__(self):
        list.__init__([])
        self.begin_point=0
        self.char_size=0
        self.char_line=''
        self.last_point=0
        self.property=''



class point:
    def __init__(self, top, bottom, left, right):
        self.top = int(top)
        self.bottom = int(bottom)
        self.left = int(left)
        self.right = int(right)
        self.max=max(self.bottom-self.top,self.right-self.left)


# block和pdf_char_line的区别在于，一行（block)可能包含多个行文本（char_line）
class block:
    """
        用于整理区分出一个块中包含多少个行文本，以及计算这个行文本的平均字间距、字体大小等
        block_list:存放划分完成的char_line的对象
     """

    def __init__(self, line_list):
        '''
         :param line_list: 解析xml中line节点得到的原始line
         '''
        self.block_list = []
        self.unclassified_block_list = []
        self.line_list = line_list
        self.split_block()
        self.deal_unclassified_block_list()


    def split_block(self):
        '''
        根据字间距，找出逻辑上的一块
        '''
        is_block_begin = True
        for index in range(0, len(self.line_list)):
            # 如果相邻两个汉字的字间距小于这个字的大小，则认为这个字是同一个块
            if((self.line_list[index].point.left - self.line_list[index - 1].point.right) < self.get_line_list_max_size()):
                if is_block_begin:
                    block = pdf_char_line()
                    is_block_begin = False
                block.append(self.line_list[index])
                block.char_line+=self.line_list[index].text
            else:
                 #self.add_to_block_list(block)
                 self.unclassified_block_list.append(block)
                 block = pdf_char_line()
                 block.append(self.line_list[index])
                 block.char_line += self.line_list[index].text
                 is_block_begin = False
        self.unclassified_block_list.append(block)


    def get_line_list_max_size(self):
        max_size=0
        for char in self.line_list:
            if char.point.max>max_size:
                max_size=char.point.max
        return max_size




    def deal_unclassified_block_list(self):
        for line_block in self.unclassified_block_list:
            self.split_kind_block(line_block)

    def split_kind_block(self,block_split):
        '''
        处理逻辑上的块。
        标点符号、数字、字母、汉字等应该采用不同的方式绘画，
        但是逻辑上应该连接到一块上
        '''
        last_is_digit = False
        is_block_begin = True
        if len(block_split)==0:return
        for index in range(0, len(block_split)):
           #处理数字
           if(tools.is_digit(block_split[index].text)):
               if not is_block_begin:
                   self.add_chinese_to_block_list(block,index-1,block_split)
                   is_block_begin = True
               if not last_is_digit:
                   block=self.init_block(block_split[index])
                   #is_block_begin = False
               block.append(block_split[index])
               block.char_line += block_split[index].text
               last_is_digit = True
               if index==len(block_split)-1:
                   self.add_chinese_to_block_list(block, index, block_split)
               continue
           else:
               if last_is_digit:
                    self.add_digit_to_block_list(block,index-1,block_split)
                    is_block_begin = True
               last_is_digit = False

            # 处理标点符号
           if (tools.is_punctuation(block_split[index].text)):
                if not is_block_begin:
                    block.append(block_split[index])
                    block.char_line += block_split[index].text
                    self.add_chinese_to_block_list(block, index, block_split)

                else:
                   block = self.init_block(block_split[index])
                   block.append(block_split[index])
                   block.char_line += block_split[index].text
                   self.add_punctuation_to_block_list(block,index,block_split)
                is_block_begin = True
           else:
               if (is_block_begin):
                   block = self.init_block(block_split[index])
                   is_block_begin = False
               block.append(block_split[index])
               block.char_line += block_split[index].text
        if not is_block_begin:
               self.add_chinese_to_block_list(block,index,block_split)


    def add_chinese_to_block_list(self,block,index,total_block):
           chinese_block=split.default_split(block,index,total_block)
           chinese_block.add_to_block_list(self.block_list)


    def add_punctuation_to_block_list(self,block,index,total_block):
        punctuation_block = split.punctuation_split(block, index, total_block)
        punctuation_block.add_to_block_list(self.block_list)

    def add_digit_to_block_list(self,block,index,total_block):
        digit_block=split.digit_split(block,index,total_block)
        digit_block.add_to_block_list(self.block_list)

    def init_block(self, char):
        block = pdf_char_line()
        block.property=self.get_property(char.text)
        return block


    def get_property(self,text):
        if tools.is_punctuation(text): return  define.property_punctuation
        if tools.is_digit(text):return  define.property_digit
        return define.property_chinese



