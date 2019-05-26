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
    fp = open(path, 'rb')
    #用文件对象创建一个PDF文档分析器
    parser = PDFParser(fp)
    #创建一个PDF文档
    doc = PDFDocument()
    #连接分析器，与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    #提供初始化密码，如果没有密码，就创建一个空的字符串
    doc.initialize()

    #检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF，资源管理器，来共享资源
        rsrcmgr = PDFResourceManager()
        #创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        #创建一个PDF解释其对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        results=""
        #循环遍历列表，每次处理一个page内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            #接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if(isinstance(x, LTTextBoxHorizontal)):
                    results+=x.get_text()
        info = ''.join(re.findall(r'准考证号：(.+)\n', str(results)))
        info+=" "
        info += ''.join(re.findall(r'姓名：(.+)\n', str(results)))
        return info

def get_files(path='Downloads', rule=".pdf"):
    all = []
    for fpathe, dirs, fs in os.walk(path):   # os.walk获取所有的目录
        for f in fs:
            filename = os.path.join(fpathe, f)
            if filename.endswith(rule):  # 判断是否是".pdf"结尾
                all.append(filename)
    return all
if __name__ == '__main__':
    pdflist=get_files()
    fw = open("info.txt", 'a',encoding="UTF-8")
    for name in pdflist:
        fw.write(parse(name)+"\n")
    fw.close()
