# -*- coding:utf-8 -*-
# by 'hollowman6' from Lanzhou University(兰州大学)
'''
此脚本用于去重操作。

This script is used for de-duplication.

'''

f = open('result.txt')
dlist = []
line = f.readline()
while line:
    dlist.append(line)
    line = f.readline()
f.close()
fi = open('result.txt', 'w')
for line in set(dlist):
    fi.write(line)
fi.close()
