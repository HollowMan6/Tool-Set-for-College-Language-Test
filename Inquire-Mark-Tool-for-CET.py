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
import io
import os
# 正则表达式搜索 Regular expression search
import re
# 爬虫库导入 Import Spider
import requests
# 图形界面 UI
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

# 变量设定
end = True
flag = False
quest = False
countt = 0
dlist = []
host = ""
# 将锁内的代码串行化 Serialization of code in locks
lock = threading.Lock()


class check:
    def __init__(self):
        # 伪装爬虫 Camouflage Spider
        self.s = requests.Session()
        self.s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
                          'Referer': 'http://cet.neea.edu.cn/cet/query.html', 'Connection': 'keep-alive', 'Host': 'cache.neea.edu.cn'}
    # 教务系统登录 Login STU-INFO System

    def login(self, host, kind, adnum, name):
        global countt, end, flag, quest, btn, dlist
        # 页面相关设置 Page Related Settings
        try:
            # 查询 check
            response = self.s.get(host+'='+kind+'%2C'+adnum+'%2C'+name)
            if "result.err" in response.text:  # Refuse to access
                T.insert(tk.END, adnum+"失败！\n")  # Fail
                dlist.pop(dlist.index(kind+' '+adnum+' '+name+'\n'))
                # 释放信号量，可用信号量加一 Release semaphores, add one semaphore
                threadmax.release()
            else:
                id_num = re.compile("z:'(.*?)'").findall(response.text)
                if id_num:
                    id_num = id_num[0]
                else:
                    end = True
                    flag = False
                    if quest == False:
                        quest = True
                        T.insert(tk.END, "查询错误！请检查查询服务器设置！\n")
                        tkinter.messagebox .showerror(
                            '错误', '查询错误！请检查查询服务器设置！', parent=root)
                    # 释放信号量，可用信号量加一 Release semaphores, add one semaphore
                    threadmax.release()
                    return
                name = re.compile("n:'(.*?)'").findall(response.text)
                if name:
                    name = name[0]
                else:
                    end = True
                    flag = False
                    if quest == False:
                        quest = True
                        T.insert(tk.END, "查询错误！请检查查询服务器设置！\n")
                        tkinter.messagebox .showerror(
                            '错误', '查询错误！请检查查询服务器设置！', parent=root)
                    # 释放信号量，可用信号量加一 Release semaphores, add one semaphore
                    threadmax.release()
                    return
                school = re.compile("x:'(.*?)'").findall(response.text)
                if school:
                    school = school[0]
                else:
                    school = ' '
                score = re.compile("s:(.*?),").findall(response.text)
                if score:
                    score = score[0]
                else:
                    score = ' '
                listening = re.compile("l:(.*?),").findall(response.text)
                if listening:
                    listening = listening[0]
                else:
                    listening = ' '
                reading = re.compile("r:(.*?),").findall(response.text)
                if reading:
                    reading = reading[0]
                else:
                    reading = ' '
                writing = re.compile("w:(.*?),").findall(response.text)
                if writing:
                    writing = writing[0]
                else:
                    writing = ' '
                oral_num = re.compile("kyz:(.*?),").findall(response.text)
                if oral_num:
                    oral_num = oral_num[0]
                else:
                    oral_num = ' '
                rank = re.compile("kys:'(.*?)'").findall(response.text)
                if rank:
                    rank = rank[0]
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
                fw.write(id_num+'\t'+name+'\t'+school+'\t'+score+'\t'+listening +
                         '\t'+reading+'\t'+writing+'\t'+oral_num+'\t'+rank+'\n')
                fw.close()
                lb.insert(tk.END, name)
                T.insert(tk.END, "成功查询到考生"+name+"的成绩\n")
                # 释放锁 Release lock
                lock.release()
                dlist.remove()
                # 释放信号量，可用信号量加一 Release semaphores, add one semaphore
                countt += 1
                dlist.pop(kind+' '+adnum+' '+name+'\n')
                a.set("总计 "+str(countt)+" 个")
                threadmax.release()
        except Exception:
            threadmax.release()
            pass


dlist = []

# 使用多线程 Using multithreading
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
                             args=(host, kind, adnum, name))
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
    host = e.get()
    if host == "":
        tkinter.messagebox .showerror('错误', '请输入成绩查询服务器地址！', parent=root)
    elif flag == True:
        tkinter.messagebox .showwarning(
            '警告', '已经在下载中，请耐心等待！退出请点击“退出”按钮。', parent=root)
    else:
        flag = True
        t = threading.Thread(target=main)
        t.setDaemon(True)
        t.start()


# Tkinter 界面设定 UI Setting
root = tk.Tk()
root.title('Inquire Mark Tool for CET -- By Hollow Man')
root.geometry('400x400')
try:
    # 打开数据文件 Open data files
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


tk.Label(text='成绩查询服务器：').pack(anchor=tk.W)
e = tk.Entry(root)
e.insert(0, "http://47.94.127.138/cet/query?data")
e.pack(anchor=tk.W)
tk.Label(text='已查询考生:').pack(anchor=tk.W)
a = tk.StringVar()
a.set("总计 0 个")
tk.Label(textvariable=a).pack(anchor=tk.W)
lbv = tk.StringVar()
lb = tk.Listbox(root, selectmode=tk.SINGLE, listvariable=lbv)
scr = tk.Scrollbar(root)
lb.pack()
btn = tk.Button(root, text="开始", command=run).pack(anchor=tk.CENTER)
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
quote = """警告：\n仅供测试使用，不可用于任何非法用途！\n对于使用本代码所造成的一切不良后果，本人将不负任何责任！\n\n说明：此版本为无验证码查询版，此版本一般于刚刚开放查询成绩入口时有效。使用前请首先运行Inquire-Mark-Tool-for-CET\n程序运行过程中向info.txt添加考生信息是无效的，必须重新运行程序。\n程序重新运行时将恢复到初始状态。\n下载结束后，请多次点击开始按钮，直到已查询考生数字不再增加，从而确保所有考生都已被查询。\n\n"""
T.insert(tk.END, quote)
root.mainloop()
