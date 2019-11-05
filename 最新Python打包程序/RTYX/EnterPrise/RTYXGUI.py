#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# FileName:RecommendGUI.py

import tkinter
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from RTYX.EnterPrise.RTYXCreatePhoneList import *
from tkinter import messagebox


# 选择推荐人表格的路径
def selectExcelFile():
    filename = askopenfilename(filetypes=[('Excel', '*.xls *.xlsx'), ('All Files', '*')])
    excel_file_global.set(filename)


# 工程路径
def selectProjectFile():
    filename = askopenfilename(filetypes=[('PROJECT', '*.xcodeproj .xcworkspace'), ('All Files', '*')])
    project_file_global.set(filename)


# 选择推荐人包的路径 ==> 可以不选，如果不选择路径，默认在桌面生成一个"生成的ipa包"存放ipa包
def selectPath():
    path_ = askdirectory()
    if path_ != '':
        output_path_global.set(path_)
    else:
        output_path_global.set("未选中路径")


# registerPhone.plist路径
def selectInfoPlistPath():
    plistPath = askopenfilename(filetypes=[('INFOPLIST', '*.plist'), ('All Files', '*')])
    info_plist_path_global.set(plistPath)


# 判断是否选择了所有的路径
def judgePath(excel_file, projectFile, outputPath, infoPlistPath):
    if excel_file != '' and projectFile != '' and outputPath != '' and infoPlistPath != '':
        packPkg(excel_file, projectFile, outputPath, infoPlistPath)
    elif excel_file == '':
        messagebox.showinfo("温馨提示", "请选择excel表格的路径！")
    elif projectFile == '':
        messagebox.showinfo("温馨提示", "请选择工程.xcodeproj/.xcworkspace路径！")
    elif infoPlistPath == '':
        messagebox.showinfo("温馨提示", "请选择registerPhone.plist路径！")
    else:
        packPkg(excel_file, projectFile, outputPath, infoPlistPath)


# 创建窗口
def create_window():
    root = tkinter.Tk()
    root.title("融托优选")  # 父容器标题
    global excel_file_global  # excelFile
    global project_file_global  # projectFile
    global output_path_global  # outputPath
    global info_plist_path_global  # infoPlistPath
    excel_file_global = StringVar()
    project_file_global = StringVar()
    output_path_global = StringVar()
    info_plist_path_global = StringVar()

    # 推荐人excel表路径
    label1 = ttk.Label(root, text="推荐人excel表路径:").grid(row=0, column=0)
    ttk.Entry(root, textvariable=excel_file_global).grid(row=0, column=1)

    button1 = ttk.Button(root, text="路径选择", command=selectExcelFile).grid(row=0, column=2, padx=10, pady=5)

    # 工程路径
    ttk.Label(root, text="工程路径:").grid(row=1, column=0)
    ttk.Entry(root, textvariable=project_file_global).grid(row=1, column=1)
    ttk.Button(root, text="路径选择", command=selectProjectFile).grid(row=1, column=2, padx=10, pady=5)

    # ipa包输出路径
    ttk.Label(root, text="ipa包输出路径:").grid(row=2, column=0)
    ttk.Entry(root, textvariable=output_path_global).grid(row=2, column=1)
    ttk.Button(root, text="路径选择", command=selectPath).grid(row=2, column=2, padx=10, pady=5)

    # info.plist路径
    ttk.Label(root, text="registerPhone.plist路径:").grid(row=3, column=0)
    ttk.Entry(root, textvariable=info_plist_path_global).grid(row=3, column=1)
    ttk.Button(root, text="路径选择", command=selectInfoPlistPath).grid(row=3, column=2, padx=10, pady=5)

    # 修改推荐人列表的plist, 获取推荐人userid并打包
    ttk.Button(root, text="开始打包", command=lambda: judgePath(excel_file_global.get(), project_file_global.get(), output_path_global.get(),
                                                           info_plist_path_global.get())).grid(row=4, column=0, pady=10)
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


# if __name__ == '__main__':
#     create_window()
