#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 融托金融多个target打包-首界面


import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import RTJRAutoPackage


# 工程路径
def select_project_file():
    filename = askopenfilename(filetypes=[('PROJECT', '*.xcodeproj .xcworkspace'), ('All Files', '*')])
    project_file.set(filename)


# 判断是否选择了所有的路径
def judge_path(project_file_path):

    if project_file_path != '':
        print("configuration：", configuration.get())
        print("method：", method.get())
        print("scheme:", scheme_global.get())

        if menu_bind() == True:
            RTJRAutoPackage.package_rtjr(project_file_path, scheme_global.get(), configuration.get(), method.get())
        # RTAutoPackage.archive_project(project_file_path, configuration.get(), password_input.get(), method.get())
    else:
        messagebox.showinfo("温馨提示", "请选择工程路径！")


# OptionMenu按钮的点击
def menu_bind():
    if method.get() == "enterprise" and scheme_global.get() == "rongtuojinrong":
        messagebox.showinfo("温馨提示", "请正确选择\n enterprise对应的是企业版的scheme: rongtuojinrongQY，\n"
                                    "ad-hoc/app-store对应的scheme: rongtuojinrong")
        return False
    elif scheme_global.get() == "rongtuojinrongQY" and method.get() != "enterprise":
        messagebox.showinfo("温馨提示", "请正确选择\n enterprise对应的是企业版的scheme: rongtuojinrongQY，\n"
                                    "ad-hoc/app-store对应的scheme: rongtuojinrong")
        return False
    else:
        return True

    print("menu_bind ==== method：", method.get())
    print("menu_bind ==== scheme:", scheme_global.get())


# 创建窗口
def create_window(application_name):
    root = tk.Tk()
    root.title(application_name)  # 父容器标题

    # 创建路径
    global project_file  # 文件路径
    # global output_path   # ipa包输出路径
    global password_input  # 开机密码

    project_file = StringVar()
    password_input = StringVar()
    # output_path = StringVar()

    # 工程路径
    tk.Label(root, text="工程路径:").grid(row=0, column=0)
    tk.Entry(root, textvariable=project_file).grid(row=0, column=1)
    tk.Button(root, text="路径选择", command=select_project_file).grid(row=0, column=2, padx=10, pady=5)

    # ipa包输出路径
    tk.Label(root, text="输出路径:").grid(row=1, column=0)
    tk.Label(root, text="ipa包输出路径, 默认路径是-Desktop/RTJRipa").grid(row=1, column=1)

    tk.Label(root, text="参数设置:").grid(row=2, column=0)

    # 让用户选择 method - 打包的类型
    global method  # 打包方法：ad-hoc、enterprise、app-store
    method = StringVar()
    method.set("ad-hoc")
    option_method = OptionMenu(root, method, 'ad-hoc', 'enterprise', 'app-store').grid(row=2, column=1, pady=10)
    # option_method.bind('<Button-1>', menu_bind())

    # 全局的scheme
    global scheme_global
    scheme_global = StringVar()
    scheme_global.set("rongtuojinrong")
    # 让用户选择 scheme - 打包的target
    option_scheme = OptionMenu(root, scheme_global, 'rongtuojinrong', 'rongtuojinrongQY').grid(row=2, column=2, pady=10)
    # option_scheme.bind('<Button-1>', menu_bind())

    # 让用户选择 CONFIGURATION - 打包的模式
    global configuration  # 让用户选择 CONFIGURATION: Debug、Release
    # 打包的模式：Debug、Release
    configuration = StringVar()
    configuration.set('Debug')  # 设置默认选中Debug选项
    option_configuration = OptionMenu(root, configuration, 'Debug', 'Release')
    option_configuration.grid(row=2, column=3, pady=10)
    print("option_configuration:", option_configuration)
    # option_configuration.bind('<Button-1>', menu_bind())

    # 打包
    tk.Button(root, text="开始打包", command=lambda: judge_path(project_file.get())).grid(row=3, column=1, pady=10)

    # option_method.pack()
    # option_method.bind('<Button-1>', menu_bind())
    # option_configuration.bind('<Button-1>', menu_bind())
    # option_configuration.pack()
    # option_scheme.pack()
    # option_scheme.bind('<Button-1>', menu_bind())

    root.mainloop()


if __name__ == '__main__':
    create_window("融托金融")
