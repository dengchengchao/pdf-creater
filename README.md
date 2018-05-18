# pdf-creater
xml2pdf是一个用于处理ocr结果的[双层pdf](https://baike.baidu.com/item/%E5%8F%8C%E5%B1%82pdf/6554147?fr=aladdin)生成器。
xml2pdf目前支持两种ocr转换：
- 百度ocr生成的xml文件
- abbyy ocr生成的xml文件

## TODO
项目是可扩展的，xml是主要是用于描述文字大小，内容，坐标。任何来源的xml只需要转换为pdf_parser.py相同的对象，即可正确的运行代码生成双层pdf。


## Geting Started

**Windows**
- 安装python3(记得将python.exe 加入到环境变量)
- 安装reportlab
  - pip install reportlab



**Linux**
- 安装python3(linux 默认自带python2.7)
- 安装reportlab
  - pip install reportlab


运行xml2pdf：    
python xml2pdf.py  imagePath xmlPath pdfPath

返回：会在pdfPath生成pdf文件   
```
__ERROR__    //错误，详情记录在日志文件（log//error）中   
__SUCCESS__  //生成成功
```



项目只是一个小小的工具，在此记录下各个问题的处理过程,提供参考

---

### 11.20 
更换算法，更换计算各个字体之间关系的算法

----
### 11.21
- 未解决问题
  - 字体之间的空格如何消除   **重要**
- 解决方案   
下载ABBYY的图像识别查看原型
- 成果
  - ABBYY之所以没有空格是因为字体大小
  - ABBYY固定使用一种字体
  - ABBYY如果字体过小，也会出现空格
- 解决思路   
  通过计算字间距，选择合适的字体大小   
-----
**经过测试，发现：**
- 之所以出现空格是因为两个字如果字体大小不一样、字间距不一样
- 使用windows下的simsun.ttc字体效果比较好，字间距最大可以达到14不出现空格，ABBYY也是使用的这个字体


准备：优化block算法，找出字大小差不多的作为一块

**优化规则：**
- 字体大小误差：中间数 的1/3
- 字体大小取右Max(减左，下减上)
- 标点符号特殊区分
- 字体大小仅用于判断块大小，具体绘画字体大小按实际需求画


### 12.1
**笔记：使用下面的函数可以调整平均的字间距和字体大小**
```
text_obj.setHorizScale(
            100 * (draw_block.last_point - draw_block[0].point.left) / canva.stringWidth(
                draw_block.char_line, _FONT_NAME_, draw_block.char_size))
```
**新的问题：**   
直接将数字、汉字、字母、标点符号混合绘画，会出现对不齐图片中的汉字的情况。   

**解决方案：**   

将每个块继续按照不同的属性进行拆分   
每个块的绘画方式也不同    
汉字块：每次绘画到下个逻辑块的left，字体大小取max   
英文块/数字块:每次绘画到下个逻辑块的left,字体大小取size   
标点块:标点块特别容易出现空格，因此标点绘画加入到上一个块的末尾
