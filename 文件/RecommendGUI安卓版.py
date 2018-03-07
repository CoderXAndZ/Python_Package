#!C:\Python27\python.exe
# coding=utf-8
from Tkinter import *
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename
from PackPackage import packPkg

def selectPath():
    path_ = askdirectory()
    outputPath.set(path_)

def selectExcelFile():
    filename = askopenfilename(filetypes = [("excel files", "*.xls;*.xlsx")])
    excelFile.set(filename)

def selectApkFile():
    filename = askopenfilename(filetypes = [("apk files", "*.apk")])
    apkFile.set(filename)

root = Tk()
outputPath = StringVar()
excelFile = StringVar()
apkFile = StringVar()

Label(root,text = "推荐人excel表路径:").grid(row = 0, column = 0)
Entry(root, textvariable = excelFile).grid(row = 0, column = 1)
Button(root, text = "路径选择", command = selectExcelFile).grid(row = 0, column = 2, padx = 10, pady = 5)

Label(root,text = "apk包路径:").grid(row = 1, column = 0)
Entry(root, textvariable = apkFile).grid(row = 1, column = 1)
Button(root, text = "路径选择", command = selectApkFile).grid(row = 1, column = 2, padx = 10, pady = 5)

Label(root,text = "vip包输出路径:").grid(row = 2, column = 0)
Entry(root, textvariable = outputPath).grid(row = 2, column = 1)
Button(root, text = "路径选择", command = selectPath).grid(row = 2, column = 2, padx = 10, pady = 5)

Button(root, text = "开始打包", command = lambda:packPkg(excelFile.get(), apkFile.get(), outputPath.get())).grid(row = 3, column = 0, pady = 10)

root.mainloop()
