#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# Home 首页

# import tkinter as ttk
from tkinter import ttk
import tkinter.messagebox
# from tkinter import messagebox
from RTJR.Enterprise import RecommendGUI
from RTYX import RTAutoPackageGUI
from RTJR import RTJRGUI
import RTYX.EnterPrise.RTYXGUI as RTYXGUI

root = tkinter.Tk()  # 创建父容器GUI

# 初始化页面
def setup_view():
    root.title("请选择要打包的工程")  # 父容器标题
    root.geometry("320x120")  # 设置父容器窗口初始大小，如果没有这个设置，窗口会随着组件大小的变化而变化

    # 融托金融
    ttk.Button(root, text="融托金融", command=lambda: choose_application(0)).grid(row=0, column=0, padx=10, pady=5)
    ttk.Button(root, text="融托金融批量打包", command=lambda: choose_application(1)).grid(row=0, column=1, padx=10, pady=5)

    # 融托优选
    ttk.Button(root, text="融托优选", command=lambda: choose_application(2)).grid(row=2, column=0, padx=10, pady=5)
    ttk.Button(root, text="融托优选批量打包", command=lambda: choose_application(3)).grid(row=2, column=1, padx=10, pady=5)

    # 融米小管家
    ttk.Button(root, text="融米小管家", command=lambda: choose_application(4)).grid(row=3, column=0, padx=10, pady=5)

    root.mainloop()


#  选择app的打包程序
def choose_application(types):
    root.destroy()  # 关闭窗口

    if types == 0:  # 测试版本打包
        print("融托金融")

        RTJRGUI.create_window("融托金融")  # 打开融托金融的打包程序
    elif types == 1:  # 融托金融批量打包

        RecommendGUI.create_window()
    elif types == 2:  # 融托优选 测试版打包
        print("融托优选")

        RTAutoPackageGUI.create_window("融托优选")
    elif types == 3:  # 融托优选 批量打包程序

        RTYXGUI.create_window()
    else:   # 融米小管家打包

        tkinter.messagebox.showinfo("温馨提示", "暂未开发，敬请期待")
        print("融米小管家")


if __name__ == '__main__':
    setup_view()