#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from createPhoneList import *

# 选择推荐人包的路径
def selectExcelFile():
    filename = askopenfilename(filetypes=[('Excel', '*.xls *.xlsx'), ('All Files', '*')])
    excelFile.set(filename)

# 工程路径
def selectProjectFile():
    filename = askopenfilename(filetypes = [('PROJECT', '*.xcodeproj .xcworkspace'), ('All Files', '*')])
    projectFile.set(filename)

# 选择推荐人包的路径
def selectPath():
    path_ = askdirectory()
    outputPath.set(path_)

root = tk.Tk()
excelFile = StringVar()
projectFile = StringVar()
outputPath = StringVar()

label1 = tk.Label(root,text="推荐人excel表路径:").grid(row = 0, column = 0)
#excelFile
tk.Entry(root, textvariable = excelFile).grid(row = 0, column = 1)

button1 = tk.Button(root, text = "路径选择", command = selectExcelFile).grid(row = 0, column = 2, padx = 10, pady = 5)

tk.Label(root,text = "工程路径:").grid(row = 1, column = 0)
tk.Entry(root, textvariable = projectFile).grid(row = 1, column = 1)
tk.Button(root, text = "路径选择", command = selectProjectFile).grid(row = 1, column = 2, padx = 10, pady = 5)

tk.Label(root,text = "ipa包输出路径:").grid(row = 2, column = 0)
tk.Entry(root, textvariable = outputPath).grid(row = 2, column = 1)
tk.Button(root, text = "路径选择", command = selectPath).grid(row = 2, column = 2, padx = 10, pady = 5)

# 获取推荐人 userid
tk.Button(root, text = "开始打包", command = lambda:packPkg(excelFile.get(), projectFile.get(), outputPath.get())).grid(row = 3, column = 0, pady = 10)

root.mainloop()
