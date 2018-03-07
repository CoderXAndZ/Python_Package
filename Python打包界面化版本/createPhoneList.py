#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import xlrd
from tkinter import messagebox
import shutil
from PackPackage import *

# 获取推荐人 userid: excel路径，工程路径，输出路径
def packPkg(excelFile, projectFile, outputPath):
    print("推荐人excel地址是", excelFile) #/Users/admin/Desktop/推荐人20180301.xlsx
    print("ipa包地址是", projectFile) #/Users/admin/ios/fmapp.xcodeproj
    print("IPA的输出地址是", outputPath) #/Users/admin/Desktop/生成的ipa包
    # 读取表格
    excel_data = xlrd.open_workbook(excelFile)
    # 第一列
    table_one = excel_data.sheet_by_index(0) # 根据sheet索引获取sheet的内容
    # 表格的总行数
    lines = table_one.nrows
    cols = table_one.ncols
    print ("表格的总行数:",lines)
    print ("表格的总列数:",cols)
    last_output_dir = ''
    
    list = []

    for i in range(0,lines):
        # 获取excel表格一行的数据
        row_values = table_one.row_values(i)
        tuijianren_id = str(int(row_values[0]))
        
        list.append(tuijianren_id)
    
    print ("===========创建的列表是：",list)
    if len(list) == lines:
        # 调用打包程序
        beginToPackage(projectFile, outputPath, list)
    else:
        print ("读取Excel失败")



