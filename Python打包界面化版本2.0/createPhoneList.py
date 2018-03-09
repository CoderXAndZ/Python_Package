#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import xlrd
#from tkinter import messagebox
import shutil
from plistlib import *
from PackPackage import *
import re

#packPkg("/Users/admin/Desktop/推荐人20180301.xlsx","/Users/admin/ios/fmapp.xcodeproj","/Users/admin/Desktop/生成的ipa包")

# 获取推荐人 userid: excel路径，工程路径，输出路径
def packPkg(excelFile, projectFile, outputPath, infoPlistPath):
    print("推荐人excel地址是", excelFile) #/Users/admin/Desktop/推荐人20180301.xlsx
    print("ipa包地址是", projectFile) #/Users/admin/ios/fmapp.xcodeproj
    print("IPA的输出地址是", outputPath) #/Users/admin/Desktop/生成的ipa包
    print("infoPlistPath的输出地址是", infoPlistPath) #
    # 读取表格
    excel_data = xlrd.open_workbook(excelFile)
    # 取出Excel的第一个sheet数据
    table_one = excel_data.sheet_by_index(0) # 根据sheet索引获取sheet的内容
    # 表格的总行数
    lines = table_one.nrows
    cols = table_one.ncols
    print ("表格的总行数:",lines)
    print ("表格的总列数:",cols)
    last_output_dir = ''
    
    idList = []
    infoPlist = []
    
    for i in range(0,lines):
        # 获取excel表格一行的数据
        row_values = table_one.row_values(i)
        tuijianren_id = str(int(row_values[0]))
        
        tuijianren_phone = str(int(row_values[1]))
        
        dict = {"fmuserid": tuijianren_id, "fmmobile": tuijianren_phone}
        
        idList.append(tuijianren_id)
        # 将Excel表格中的数据转成数组
        infoPlist.append(dict)
        
    # 删除旧的plist数据，导入新的
    plist = readPlist(infoPlistPath)
    print ("原plist是：", plist)
    writePlist(infoPlist, infoPlistPath)

    print ("===========创建的列表是：",idList)
    print ("读取的手机号列表是：", infoPlist)
    plist = readPlist(infoPlistPath)
    print ("修改之后的列表是：", plist)
    if len(idList) == lines:
        # 调用打包程序
        beginToPackage(projectFile, outputPath, idList)
    else:
        print ("读取Excel失败")

# 修改打包好的ipa的名字：app109
# outputPath:所有的ipa包的文件夹的上层文件夹 /Users/admin/Desktop/生成的ipa包
# path:打包好的ipa包的文件夹路径 /Users/admin/Desktop/生成的ipa包/120
def changeFileName(exportPath, outputPath):
    if not os.path.isdir(exportPath):
        return False
    if os.path.isdir(exportPath):
        fileName = os.path.basename(exportPath)
        pathOld = exportPath + "/rzjrapp.ipa"
        print ("获取文件名：",fileName)
        pathNew = exportPath + "/app" + fileName + ".ipa"
        os.rename(pathOld , pathNew)
#        # 将所有的ipa包移动到统一的文件夹
#        ipaPath = os.makedirs(outputPath + "/所有的ipa包")
        #将要移动的文件夹
        pathMoved = outputPath + "/所有的ipa包"
        shutil.move(pathNew, pathMoved)

