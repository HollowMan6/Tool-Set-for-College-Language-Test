# -*- coding:utf-8 -*-
# by 'hollowman6' from Lanzhou University(兰州大学)


from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
import os.path
# 正则表达式搜索 Regular expression search
import re


def parse(path):
    '''解析PDF文本，并保存到TXT文件中'''
    '''parses PDF text and saves it to TXT file'''
    fp = open(path, 'rb')
    # 用文件对象创建一个PDF文档分析器 Create a PDF document analyzer with file objects
    parser = PDFParser(fp)
    # 创建一个PDF文档 Create a PDF document
    doc = PDFDocument()
    # 连接分析器，与文档对象 Connect the analyzer to the document object
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，如果没有密码，就创建一个空的字符串 Provides an initialization password, and if there is no password, creates an empty string
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略 Check whether the document provides TXT conversion, ignore it if it does not
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器来共享资源 Create PDF Resource Manager to share resources
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象 Create a PDF device object
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释其对象 Create a PDF to explain its object
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        results = ""
        # 循环遍历列表，每次处理一个page内容 创建PDF以解释其对象
        # doc.get_pages() 获取page列表 Get page list
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象 The LTPage object that accepts the page
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 Here layout is an LTPage object that stores the various objects parsed by this page.
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 Generally include LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal and so on.
            # 想要获取文本就获得对象的text属性 Get the text attribute of the object if you want to get the text
            for x in layout:
                if(isinstance(x, LTTextBoxHorizontal)):
                    results += x.get_text()
        info = ''.join(re.findall(r'准考证号：(.+)\n', str(results)))
        info += " "
        info += ''.join(re.findall(r'姓名：(.+)\n', str(results)))
        return info


def get_files(path='Downloads', rule=".pdf"):
    all = []
    # os.walk获取所有的目录 Get all the directories
    for fpathe, dirs, fs in os.walk(path):
        for f in fs:
            filename = os.path.join(fpathe, f)
            # 判断是否是"<rule>"结尾 Judge whether it is the end of "<rule>"?
            if filename.endswith(rule):
                all.append(filename)
    return all


if __name__ == '__main__':
    pdflist = get_files()
    fw = open("info.txt", 'a', encoding="UTF-8")
    print("正在提取中，请稍后...")
    for name in pdflist:
        fw.write(parse(name)+"\n")
    fw.close()
    print("成功！")
