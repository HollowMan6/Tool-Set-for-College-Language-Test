#!/bin/bash 
echo "正在解压文件......"
echo "Unzipping files..."
unzip -O CP936 -d ./Downloads ./Downloads/\*.zip
echo "Done!"
echo "完成！"
echo "正在运行提取信息脚本......"
echo "Running the script..."
python3 ./Get-Info-from-CET-Admission-Ticket.py
echo "Done!"
echo "成功！"
