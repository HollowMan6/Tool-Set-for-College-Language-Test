# -*- coding:utf-8 -*-
# by 'hollowman6' from Lanzhou University(兰州大学)
'''
此脚本用于数据爬取成功后的去重操作。

This script is used for de-duplication after successful data crawling.

'''

f = open('success.txt')
dlist = []
line = f.readline()
while line:
    dlist.append(line)
    line = f.readline()
f.close()
fi = open('success.txt', 'w')
for line in set(dlist):
    fi.write(line)
fi.close()
