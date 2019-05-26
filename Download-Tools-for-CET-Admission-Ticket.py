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
provinceCode = "62"
IDTypeCode = "1"
verificationCode = ""
countt = 0
IDNumberlist = []
Namelist = []
ssid = ""
pool = ""


class visit:
    def __init__(self):
        # 伪装爬虫 Camouflage Spider
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
        }

    def login(self, provinceCode, IDTypeCode, IDNumber, Name, verificationCode):
        # 页面相关设置 Page Related Settings
        global countt, end, flag, quest, ssid, pool, btn, IDNumberlist, Namelist
        infourl = 'http://cet.etest.net.cn/Home/ToQuickPrintTestTicket'
        try:
            # 获取下载SID
            postdata = {
                'provinceCode': provinceCode,
                'IDTypeCode': IDTypeCode,
                'IDNumber': IDNumber,
                'Name': Name,
                'verificationCode': verificationCode
            }
            cookies = {'ASP.NET_SessionId': ssid,
                       'BIGipServercet_pool': pool}
            r = self.s.post(infourl, postdata, cookies=cookies)
            if r.status_code == 200:
                r = r.content.decode('UTF-8', 'ignore')
                if "验证码已超时失效，请重新输入。" in r:
                    end = True
                    flag = False
                    if quest == False:
                        quest = True
                        T.insert(tk.END, "请刷新验证码！\n")
                        tkinter.messagebox .showerror(
                            '错误', '请刷新验证码！', parent=root)
                elif "验证码错误" in r:
                    end = True
                    flag = False
                    if quest == False:
                        quest = True
                        T.insert(tk.END, "验证码错误！\n")
                        tkinter.messagebox .showerror(
                            '错误', '验证码错误！', parent=root)
                else:
                    sids = re.findall(r'{\\"SID\\":\\"(.+?)\\"', str(r))
                    for sid in sids:
                        count = 0
                        if sid.isalnum():
                            downlink = "http://cet.etest.net.cn/Home/DownTestTicket?SID="+sid
                            download = self.s.get(downlink)
                            if download.status_code == 200:
                                download=download.content
                                if len(download) < 666:
                                    pass
                                else:
                                    count += 1
                                    w = open("Downloads/"+Name +
                                            str(count)+'.zip', 'wb')
                                    w.write(download)
                                    w.close()
                                    lb.insert(tk.END, Name)
                                    T.insert(tk.END, "成功下载"+Name+"的准考证，保存到" +
                                            Name+str(count)+".zip\n")
                            else:
                                return
                    countt += 1
                    Namelist.pop(IDNumberlist.index(IDNumber))
                    IDNumberlist.pop(IDNumberlist.index(IDNumber))
                    a.set("总计 "+str(countt)+" 个")
            threadmax.release()
        except Exception:
            threadmax.release()
            pass


# 使用多线程 Using multithreading
# 限制线程的最大数量为32个 The maximum number of restricted threads is 32
threadmax = threading.BoundedSemaphore(32)

# 定义爬虫线程 Define Spider Thread


def main():
    global flag, IDNumberlist, Namelist
    l = []
    for IDNumber in IDNumberlist:
        if end == True:
            return
        ind = IDNumberlist.index(IDNumber)
        Name = Namelist[ind]
        # 增加信号量，可用信号量减一 Increase the semaphore and subtract one from the semaphore
        threadmax.acquire()
        t = threading.Thread(target=visit().login, args=(
            provinceCode, IDTypeCode, IDNumber, Name, verificationCode))
        t.start()
        l.append(t)
    for t in l:
        t.join()
    tkinter.messagebox .showinfo(
        '完成', '下载完毕！可能一些账号仍未下载。\n请再次点击“开始”按钮下载', parent=root)
    flag = False


# 开始爬虫 Start Spidering
def run():
    global root, flag, end, ssid, pool, quest, verificationCode
    end = False
    quest = False
    if not os.path.exists('Downloads'):
        os.makedirs('Downloads')
    verificationCode = e.get()
    ssid = e1.get()
    pool = e2.get()
    if verificationCode == "":
        tkinter.messagebox .showerror('错误', '请输入验证码！', parent=root)
    elif ssid == "" or pool == "":
        tkinter.messagebox .showerror('错误', '请输入当前Cookies！', parent=root)
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
root.title('Download Tools for CET Admission Ticket -- By Hollow Man')
root.geometry('540x700')
try:
    # 打开数据文件 Open data files
    f = open("list.txt", encoding='UTF-8')
    line = f.readline()
    while line:
        li = line.split(" ")
        Namelist.append(li[0])
        IDNumberlist.append(li[1].replace("\n", ""))
        line = f.readline()
    f.close()
except FileNotFoundError:
    tkinter.messagebox .showerror(
        '错误', '请准备好数据文件list.txt并放在软件的同一目录下！', parent=root)
    root.destroy()
tk.Label(text='报名所在地：').pack(anchor=tk.W)
cmb = ttk.Combobox(root)
cmb.pack(anchor=tk.W)
cmb['value'] = ('北京', '天津', '河北', '吉林', '黑龙江', '上海', '江苏', '安徽', '福建', '山东',
                '河南', '湖北', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '甘肃', '青海', '宁夏', '澳门')
cmb.current(19)
val = {'北京': 11, '天津': 12, '河北': 13, '吉林': 22, '黑龙江': 23, '上海': 31, '江苏': 32, '安徽': 34, '福建': 35, '山东': 37, '河南': 41,
       '湖北': 42, '广东': 44, '广西': 45, '海南': 46, '重庆': 50, '四川': 51, '贵州': 52, '云南': 53, '甘肃': 62, '青海': 63, '宁夏': 64, '澳门': 82}


def func(*args):
    global provinceCode
    provinceCode = val[cmb.get()]


cmb.bind("<<ComboboxSelected>>", func)


tk.Label(text='证件类型：').pack(anchor=tk.W)
cmb1 = ttk.Combobox(root)
cmb1.pack(anchor=tk.W)
cmb1['value'] = ('中华人民共和国居民身份证', '台湾居民往来大陆通行证', '港澳居民来往内地通行证',
                 '护照', '香港身份证', '澳门身份证', '港澳居民居住证', '台湾居民居住证')
cmb1.current(0)
val1 = {'中华人民共和国居民身份证': 1, '台湾居民往来大陆通行证': 2, '港澳居民来往内地通行证': 3,
        '护照': 4, '香港身份证': 5, '澳门身份证': 6, '港澳居民居住证': 7, '台湾居民居住证': 8}


def func1(*args):
    global IDTypeCode
    IDTypeCode = val1[cmb1.get()]


cmb1.bind("<<ComboboxSelected>>", func1)


def pause():
    global end, flag
    flag = False
    end = True
    tkinter.messagebox .showinfo(
        '提示', '正在暂停所有线程，请稍后！...', parent=root)


tk.Label(text='验证码：').pack(anchor=tk.W)
e = tk.Entry(root)
e.pack(anchor=tk.W)
tk.Label(text='Cookies').pack(anchor=tk.W)
tk.Label(text='ASP.NET_SessionId：').pack(anchor=tk.W)
e1 = tk.Entry(root)
e1.pack(anchor=tk.W)
tk.Label(text='BIGipServercet_pool：').pack(anchor=tk.W)
e2 = tk.Entry(root)
e2.pack(anchor=tk.W)
tk.Label(text='已查询账号:').pack(anchor=tk.W)
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
quote = """警告：\n仅供测试使用，不可用于任何非法用途！\n对于使用本代码所造成的一切不良后果，本人将不负任何责任！\n\n说明：请将list.txt文件放在程序运行目录下后再运行本软件,list.txt一行代表一条数据，其格式为\n姓名 证件号\n运行软件的同时，请用浏览器打开\nhttp://cet.etest.net.cn/Home/QuickPrintTestTicket\n ，输入你看到的验证码到本软件中，并且获取Cookies中ASP.NET_SessionId和BIGipServercet_pool的值。\n如果提示验证码已过期，请点击网页中的验证码图片，以刷新验证码，再将该验证码输入到本软件中\n如果总提示验证码已过期，请考虑是否为Cookies输入错误\n程序运行过程中向list.txt添加账号是无效的，必须重新运行程序。\n程序重新运行时将恢复到初始状态。\n下载结束后，请多次点击开始按钮，直到已查询账号数字不再增加，从而确保所有账号都已被下载。\n\n"""
T.insert(tk.END, quote)

root.mainloop()
