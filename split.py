import tools
import copy
import define


class point:
    def __init__(self, top, bottom, left, right):
        self.top = int(top)
        self.bottom = int(bottom)
        self.left = int(left)
        self.right = int(right)
        self.max=max(self.bottom-self.top,self.right-self.left)


#汉字的计算方法
class default_split:
    def __init__(self,block,index,total_block):
        self.block =block
        self.index=index
        self.total_block=total_block
        self.total_len=len(total_block)

    # 计算字体大小
    def get_char_size(self):
        if(len(self.block)<1):return 0
        list_size=[]
        for char in self.block:
            if not tools.is_punctuation(char.text):
               list_size.append(char.point.max)
        return tools.get_average(list_size)

    # 计算绘画的y坐标
    def get_block_bottom(self):
        list_bottom = []
        for char in self.block:
            if(tools.is_punctuation(char.text)):continue
            list_bottom.append(char.point.bottom + (char.point.max - (char.point.bottom - char.point.top)) / 2)
        return tools.get_average(list_bottom)


    # 计算块结束的x坐标
    def get_end_x_point(self):
        #如果汉字后面是数字就把汉字延长到下个块的开头/消除空格
        if(self.total_len-1 ==self.index):
            if tools.is_punctuation(self.total_block[self.index].text):
                pun_dis=self.block.char_size
            else:
                pun_dis=0
            return self.total_block[self.index].point.right+pun_dis
        return self.total_block[self.index+1].point.left

    def print(self):
        text=""
        for char in self.total_block:
            text+=char.text
        print("aaa"+text)


    # 计算一行的开始绘画的坐标
    def get_line_begin_point(self):
        return point(self.block[0].point.top,self.get_block_bottom(), self.block[0].point.left, self.block[0].point.right)

    def add_to_block_list(self,block_list):
        self.block.char_size = self.get_char_size()
        self.block.begin_point = self.get_line_begin_point()
        self.block.last_point = self.get_end_x_point()
        block_list.append(copy.deepcopy(self.block))


class punctuation_split(default_split):
      '''拆分标点符号
         需要重写的有：
         @begin_point
         @char_size
      '''

      def __init__(self, block, index, total_block):
          super(punctuation_split, self).__init__(block,index,total_block)

      def get_line_begin_point(self):
          char=self.block[0]
          if self.index<self.total_len-1:
            x_distance=(self.total_block[self.index+1].point.left-char.point.right)/2#-self.block[0].size
          else:
            x_distance=0
          return point(char.point.top,char.point.top+char.point.max, char.point.left+x_distance, char.point.right)


      def get_char_size(self):
           return self.block[0].size


      def get_end_x_point(self):
          return  self.block.begin_point.right+self.block.char_size/2


class digit_split(default_split):
    def __init__(self, block, index, total_block):
        super(digit_split, self).__init__(block, index, total_block)

    def get_char_size(self):
        if (len(self.block) < 1): return 0
        list_size = []
        for char in self.block:
            list_size.append(char.point.max)
        return tools.get_average(list_size)

    # def get_end_x_point(self):
    #     return self.total_block[self.index ].point.right