#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# 融托优选打包界面

import tkinter as tk
import RTYXAutoPackageAndPost  # 融托优选的打包程序
from tkinter import messagebox


# 初始化页面
def setup_view(title_name):
    global root
    root = tk.Tk()  # 创建父容器GUI
    root.title(title_name)  # 父容器标题
    # root.geometry("320x80")  # 设置父容器窗口初始大小，如果没有这个设置，窗口会随着组件大小的变化而变化

    tk.Label(root, text="输入开机密码，授权访问钥匙串").grid(row=0, column=0)
    tk.Label(root, text="请输入测试人员邮箱,多个邮箱请使用英文逗号隔开").grid(row=1, column=0)

    # 融托优选
    tk.Button(root, text="开始打包", command=lambda: input_emails()).grid(row=2, column=0)

    root.mainloop()


#  选择app的打包程序
def input_emails():
    RTYXAutoPackageAndPost.post_to_fir_im('1935722630@qq.com')

    # password = input('输入开机密码，授权访问钥匙串：\n')
    # emails = input("请输入测试人员邮箱,多个邮箱请使用英文逗号隔开：\n")
    #
    # if len(emails) > 0:
    #     RTYXAutoPackageAndPost.archive_project(password, emails)
    # elif len(password) == 0:
    #     messagebox.showinfo("温馨提示", "请选择excel表格的路径！")

