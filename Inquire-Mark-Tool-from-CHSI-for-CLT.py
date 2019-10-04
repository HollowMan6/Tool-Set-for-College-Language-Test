# -*- coding:utf-8 -*-
# by 'hollowman6' from Lanzhou University(兰州大学)

'''
警告：
仅供测试使用，不可用于任何非法用途！
对于使用本代码所造成的一切不良后果，本人将不负任何责任！

Warning:
For TESTING ONLY, not for any ILLIGAL USE!
I will not be responsible for any adverse consequences caused by using this code.

'''

# 多线程 Multithreading
import threading
# 文件处理 File processing
import os
# 爬虫库导入 Import Spider
import requests
from lxml import etree
# 图形界面 UI
import tkinter as tk
import tkinter.messagebox

# 变量设定
end = True
flag = False
quest = False
countt = 0
dlist = []
host = "https://www.chsi.com.cn/cet/query"
# 将锁内的代码串行化 Serialization of code in locks
lock = threading.Lock()


class check:
    def __init__(self):
        # 伪装爬虫 Camouflage Spider
        self.s = requests.Session()
        self.s.headers = {'Referer': 'https://www.chsi.com.cn/cet/index.jsp'}
    # 教务系统登录 Login STU-INFO System

    def login(self, kind, adnum, name):
        global countt, end, flag, quest, dlist
        # 页面相关设置 Page Related Settings
        try:
            # 查询 check
            postdata = {'zkzh': adnum, 'xm': name}
            response = self.s.post(host, postdata, verify=False)
            if "查询失败，请稍后重新查询。" in response.text:
                end = True
                flag = False
                if quest == False:
                    quest = True
                    T.insert(tk.END, "查询出错！\n")
                    tkinter.messagebox .showerror(
                        '错误', '查询出错！', parent=root)
            else:
                html = etree.HTML(response.text)
                exam = html.xpath('//*[@id="leftH"]/div/table/tr[3]/td/text()')
                id_num = ""
                score = ""
                if exam:
                    exam = exam[0].replace(" ", "").replace(
                        "\t", "").replace("\r", "").replace("\n", "")
                    if "英语" in exam:
                        score = html.xpath(
                            '//*[@id="leftH"]/div/table/tr[6]/td/span/text()')
                        if score:
                            score = score[0].replace(" ", "").replace(
                                "\t", "").replace("\r", "").replace("\n", "")
                        else:
                            score = ' '
                        id_num = html.xpath(
                            '//*[@id="leftH"]/div/table/tr[5]/td/text()')
                        if id_num:
                            id_num = id_num[0].replace(" ", "").replace(
                                "\t", "").replace("\r", "").replace("\n", "")
                        else:
                            id_num = ' '
                    else:
                        id_num = html.xpath(
                            '//*[@id="leftH"]/div/table/tr[4]/td/text()')
                        if id_num:
                            id_num = id_num[0].replace(" ", "").replace(
                                "\t", "").replace("\r", "").replace("\n", "")
                        else:
                            id_num = ' '
                        score = html.xpath(
                            '//*[@id="leftH"]/div/table/tr[5]/td/span/text()')
                        if score:
                            score = score[0].replace(" ", "").replace(
                                "\t", "").replace("\r", "").replace("\n", "")
                        else:
                            score = ' '
                else:
                    end = True
                    flag = False
                    if quest == False:
                        quest = True
                        T.insert(tk.END, adnum+"失败！\n")  # Fail
                        tkinter.messagebox .showerror(
                            '错误', '需要验证码！请更换IP后再试', parent=root)
                    # 释放信号量，可用信号量加一 Release semaphores, add one semaphore
                    threadmax.release()
                    return
                name = html.xpath('//*[@id="leftH"]/div/table/tr[1]/td/text()')
                if name:
                    name = name[0].replace(" ", "").replace(
                        "\t", "").replace("\r", "").replace("\n", "")
                else:
                    # 释放信号量，可用信号量加一 Release semaphores, add one semaphore
                    threadmax.release()
                    return
                school = html.xpath(
                    '//*[@id="leftH"]/div/table/tr[2]/td/text()')
                if school:
                    school = school[0].replace(" ", "").replace(
                        "\t", "").replace("\r", "").replace("\n", "")
                else:
                    school = ' '

                listening = html.xpath(
                    '//*[@id="leftH"]/div/table/tr[7]/td[2]/text()')
                if listening:
                    listening = listening[0].replace(" ", "").replace(
                        "\t", "").replace("\r", "").replace("\n", "")
                else:
                    listening = ' '
                reading = html.xpath(
                    '//*[@id="leftH"]/div/table/tr[8]/td[2]/text()')
                if reading:
                    reading = reading[0].replace(" ", "").replace(
                        "\t", "").replace("\r", "").replace("\n", "")
                else:
                    reading = ' '
                writing = html.xpath(
                    '//*[@id="leftH"]/div/table/tr[9]/td[2]/text()')
                if writing:
                    writing = writing[0].replace(" ", "").replace(
                        "\t", "").replace("\r", "").replace("\n", "")
                else:
                    writing = ' '
                oral_num = html.xpath(
                    '//*[@id="leftH"]/div/table/tr[11]/td/text()')
                if oral_num:
                    oral_num = oral_num[0].replace(" ", "").replace("\t", "").replace(
                        "\r", "").replace("\n", "").replace("--", "")
                else:
                    oral_num = ' '
                rank = html.xpath(
                    '//*[@id="leftH"]/div/table/tr[12]/td/text()')
                if rank:
                    rank = rank[0].replace(" ", "").replace("\t", "").replace(
                        "\r", "").replace("\n", "").replace("--", "")
                else:
                    rank = ' '
                # 上锁，第一个线程如果申请到锁，会在执行公共数据的过程中持续阻塞后续线程
                # 即后续第二个或其他线程依次来了发现已经被上锁，只能等待第一个线程释放锁
                # 当第一个线程将锁释放，后续的线程会进行争抢
                # Lock. If the first thread applies for a lock, it will continue to block subsequent threads while executing public data.
                # That is, the next second or other thread comes in turn and finds that it has been locked and can only wait for the first thread to release the lock.
                # When the first thread releases the lock, subsequent threads compete.
                lock.acquire()
                fw = open("result.txt", 'a')
                fw.write(id_num+'\t'+name+'\t'+school+'\t'+exam+'\t'+score+'\t'+listening +
                         '\t'+reading+'\t'+writing+'\t'+oral_num+'\t'+rank+'\n')
                fw.close()
                lb.insert(tk.END, name)
                T.insert(tk.END, "成功查询到考生 "+name+" 的成绩\n")
                # 释放锁 Release lock
                lock.release()
                # 释放信号量，可用信号量加一 Release semaphores, add one semaphore
                countt += 1
                dlist.pop(dlist.index(kind+' '+adnum+' '+name+'\n'))
                a.set("总计 "+str(countt)+" 个")
            threadmax.release()
        except Exception:
            threadmax.release()


dlist = []

# 使用多线程 Using multithreading
# 限制线程的最大数量为32个 The maximum number of restricted threads is 32
threadmax = threading.BoundedSemaphore(32)

# 定义爬虫线程 Define Spider Thread


def main():
    global flag, dlist
    l = []
    for line in dlist:
        if end == True:
            return
        kind, adnum, name = line.split(" ", 3)
        name = name.replace("\n", "")
        if len(name) > 3:
            name = name[0:3]
        # 增加信号量，可用信号量减一 Increase the semaphore and subtract one from the semaphore
        threadmax.acquire()
        t = threading.Thread(target=check().login,
                             args=(kind, adnum, name))
        t.start()
        l.append(t)
    for t in l:
        t.join()
    tkinter.messagebox .showinfo(
        '完成', '下载完毕！可能一些考生仍未检查。\n请再次点击“开始”按钮下载', parent=root)
    flag = False


# 开始爬虫 Start Spidering
def run():
    global root, flag, end, quest, host
    end = False
    quest = False
    if not os.path.exists('Downloads'):
        os.makedirs('Downloads')
    if flag == True:
        tkinter.messagebox .showwarning(
            '警告', '已经在下载中，请耐心等待！退出请点击“退出”按钮。', parent=root)
    else:
        flag = True
        t = threading.Thread(target=main)
        t.setDaemon(True)
        t.start()


# Tkinter 界面设定 UI Setting
root = tk.Tk()
root.title('Inquire Mark Tool from CHSI for CLT -- By Hollow Man')
root.geometry('500x400')
try:
    # 打开数据文件 Open data files
    f = open("info.txt", encoding='utf-8')
    line = f.readline()
    while line:
        dlist.append(line)
        line = f.readline()
    f.close()
except FileNotFoundError:
    tkinter.messagebox .showerror(
        '错误', '请先运行Get-Info-from-CET-Admission-Ticket解析数据！', parent=root)
    root.destroy()


def pause():
    global end, flag
    flag = False
    end = True
    tkinter.messagebox .showinfo(
        '提示', '正在暂停所有线程，请稍后！...', parent=root)


tk.Label(text='已查询考生:').pack(anchor=tk.W)
a = tk.StringVar()
a.set("总计 0 个")
tk.Label(textvariable=a).pack(anchor=tk.W)
lbv = tk.StringVar()
lb = tk.Listbox(root, selectmode=tk.SINGLE, listvariable=lbv)
scr = tk.Scrollbar(root)
lb.pack()
tk.Button(root, text="开始", command=run).pack(anchor=tk.CENTER)
tk.Button(root, text="暂停", command=pause).pack(anchor=tk.CENTER)
tk.Button(root, text="退出", command=root.destroy).pack(anchor=tk.CENTER)
lb.config(yscrollcommand=scr.set)
scr.config(command=lb.yview)
lb.pack(side=tk.LEFT, fill=tk.Y)
scr.pack(side=tk.LEFT, fill=tk.Y)
S = tk.Scrollbar(root)
T = tk.Text(root, height=4, width=50)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.RIGHT, fill=tk.Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = """警告：\n仅供测试使用，不可用于任何非法用途！\n对于使用本代码所造成的一切不良后果，本人将不负任何责任！\n\n说明：使用前请首先运行Inquire-Mark-Tool-for-CET\n当提示更换IP时请更换IP，如更换后还是频繁提示请检查info.txt中特定数据是否有误\n程序运行过程中向info.txt添加考生信息是无效的，必须重新运行程序。\n程序重新运行时将恢复到初始状态。\n下载结束后，请多次点击开始按钮，直到已查询考生数字不再增加，从而确保所有考生都已被查询。\n\n"""
T.insert(tk.END, quote)
root.mainloop()
