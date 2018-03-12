#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# FileName:RecommendGUI.py

import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from createPhoneList import *
from tkinter import messagebox

# 选择推荐人包的路径
def selectExcelFile():
    filename = askopenfilename(filetypes=[('Excel', '*.xls *.xlsx'), ('All Files', '*')])
    excelFile.set(filename)

# 工程路径
def selectProjectFile():
    filename = askopenfilename(filetypes = [('PROJECT', '*.xcodeproj .xcworkspace'), ('All Files', '*')])
    projectFile.set(filename)

# 选择推荐人包的路径 ==> 可以不选，如果不选择路径，默认在桌面生成一个"生成的ipa包"存放ipa包
def selectPath():
    path_ = askdirectory()
    if path_ != '':
        outputPath.set(path_)
    else:
        outputPath.set("")

# registerPhone.plist路径
def selectInfoPlistPath():
    plistPath = askopenfilename(filetypes = [('INFOPLIST', '*.plist'), ('All Files', '*')])
    infoPlistPath.set(plistPath)

# 判断是否选择了所有的路径
def judgePath(excelFile, projectFile, outputPath, infoPlistPath):
    if excelFile != '' and projectFile != '' and outputPath != '' and infoPlistPath != '':
        packPkg(excelFile, projectFile, outputPath, infoPlistPath)
    elif excelFile == '':
        messagebox.showinfo("温馨提示", "请选择excel表格的路径！" )
    elif projectFile == '':
        messagebox.showinfo("温馨提示", "请选择工程.xcodeproj/.xcworkspace路径！" )
    elif infoPlistPath == '':
        messagebox.showinfo("温馨提示", "请选择registerPhone.plist路径！" )
    else:
        packPkg(excelFile, projectFile, outputPath, infoPlistPath)

root = tk.Tk()
excelFile = StringVar()
projectFile = StringVar()
outputPath = StringVar()
infoPlistPath = StringVar()

# 推荐人excel表路径
label1 = tk.Label(root,text="推荐人excel表路径:").grid(row = 0, column = 0)
tk.Entry(root, textvariable = excelFile).grid(row = 0, column = 1)

button1 = tk.Button(root, text = "路径选择", command = selectExcelFile).grid(row = 0, column = 2, padx = 10, pady = 5)

# 工程路径
tk.Label(root,text = "工程路径:").grid(row = 1, column = 0)
tk.Entry(root, textvariable = projectFile).grid(row = 1, column = 1)
tk.Button(root, text = "路径选择", command = selectProjectFile).grid(row = 1, column = 2, padx = 10, pady = 5)

# ipa包输出路径
tk.Label(root,text = "ipa包输出路径:").grid(row = 2, column = 0)
tk.Entry(root, textvariable = outputPath).grid(row = 2, column = 1)
tk.Button(root, text = "路径选择", command = selectPath).grid(row = 2, column = 2, padx = 10, pady = 5)

# info.plist路径
tk.Label(root, text = "registerPhone.plist路径:").grid(row = 3, column = 0)
tk.Entry(root, textvariable = infoPlistPath).grid(row = 3, column = 1)
tk.Button(root, text = "路径选择", command = selectInfoPlistPath).grid(row = 3, column = 2, padx = 10, pady = 5)

# 修改推荐人列表的plist, 获取推荐人userid并打包
tk.Button(root, text = "开始打包", command = lambda:judgePath(excelFile.get(), projectFile.get(), outputPath.get(), infoPlistPath.get())).grid(row = 4, column = 0, pady = 10)
# "/Users/admin/Desktop/生成的ipa包",
#tk.Button(root, text = "开始打包", command = lambda:packPkg("/Users/admin/Desktop/工作簿1.xlsx","/Users/admin/ios/fmapp.xcodeproj",outputPath.get(), "/Users/admin/ios/fmapp/registerPhone.plist")).grid(row = 4, column = 0, pady = 10)
# 推荐人20180301  工作簿1
# "/Users/admin/Desktop/推荐人20180301.xlsx","/Users/admin/ios/fmapp.xcodeproj","/Users/admin/Desktop/生成的ipa包",
# excelFile.get(), projectFile.get(), outputPath.get(), infoPlistPath.get()
#tk.Button(root, text = "开始打包", command = lambda:judgePath("/Users/admin/Desktop/工作簿1.xlsx","/Users/admin/ios/fmapp.xcodeproj","/Users/admin/Desktop/生成的ipa包",infoPlistPath.get())).grid(row = 4, column = 0, pady = 10)

#print ("打包输出路径", "/Users/admin/Desktop/生成的ipa包")
## outputPath.get()
#tk.Button(root, text = "开始打包", command = lambda:changeFileName("/Users/admin/Desktop/生成的ipa包/111", "/Users/admin/Desktop/生成的ipa包")).grid(row = 4, column = 0, pady = 10)


root.mainloop()
