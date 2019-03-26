#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 融托优选-自动打包界面

import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import RTAutoPackage


# 工程路径
def select_project_file():
    filename = askopenfilename(filetypes=[('PROJECT', '*.xcodeproj .xcworkspace'), ('All Files', '*')])
    project_file.set(filename)


# 判断是否选择了所有的路径
def judge_path(project_file_path):

    if project_file_path != '':
        print("configuration：", configuration.get())
        print("method：", method.get())
        RTAutoPackage.archive_project(project_file_path, configuration.get(), password_input.get(), method.get())
    else:
        messagebox.showinfo("温馨提示", "请选择工程路径！")


# 创建窗口
def create_window(application_name):
    root = tk.Tk()
    root.title(application_name)  # 父容器标题

    # 创建路径
    global project_file  # 文件路径
    # global output_path   # ipa包输出路径
    global password_input  # 开机密码
    global configuration  # 让用户选择 CONFIGURATION: Debug、Release
    global method  # 打包方法：ad-hoc、enterprise、app-store

    project_file = StringVar()
    password_input = StringVar()
    # output_path = StringVar()
    # 打包的模式：Debug、Release
    configuration = StringVar()
    configuration.set('Debug')  # 设置默认选中Debug选项
    # 打包的类型
    method = StringVar()
    method.set("ad-hoc")

    # 工程路径
    tk.Label(root, text="工程路径:").grid(row=0, column=0)
    tk.Entry(root, textvariable=project_file).grid(row=0, column=1)
    tk.Button(root, text="路径选择", command=select_project_file).grid(row=0, column=2, padx=10, pady=5)

    # 开机密码
    tk.Label(root, text="开机密码:").grid(row=1, column=0)
    tk.Entry(root, textvariable=password_input).grid(row=1, column=1)

    # ipa包输出路径
    tk.Label(root, text="输出路径:").grid(row=2, column=0)
    tk.Label(root, text="ipa包输出路径, 默认路径是-Desktop/RTYXipa").grid(row=2, column=1)
    # tk.Entry(root, textvariable=output_path).grid(row=1, column=1)
    # tk.Button(root, text="路径选择", command=select_path).grid(row=1, column=2, padx=10, pady=5)

    # 打包
    tk.Button(root, text="开始打包", command=lambda: judge_path(project_file.get())).grid(row=4, column=0, pady=10)
    # 让用户选择 CONFIGURATION - 打包的模式
    w = OptionMenu(root, configuration, 'Debug', 'Release').grid(row=4, column=1, pady=10)
    # 让用户选择 method - 打包的类型
    OptionMenu(root, method, 'ad-hoc', 'enterprise', 'app-store').grid(row=4, column=2, pady=10)

    root.mainloop()


# if __name__ == '__main__':
#     create_window("融托优选")

