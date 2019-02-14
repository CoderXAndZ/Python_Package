#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# Home 首页

import tkinter as tk
import RecommendGUI  # 融托金融打包程序
import RTYXHomePage  # 融托优选首页面


# 初始化页面
def setup_view():
    global root
    root = tk.Tk()  # 创建父容器GUI
    root.title("请选择要打包的工程")  # 父容器标题
    root.geometry("320x80")  # 设置父容器窗口初始大小，如果没有这个设置，窗口会随着组件大小的变化而变化

    # 融托金融
    tk.Button(root, text="融托金融", command=lambda: choose_application(0)).grid(row=0, column=0, padx=10, pady=5)
    # 融米小管家
    tk.Button(root, text="融米小管家", command=lambda: choose_application(1)).grid(row=0, column=1, padx=10, pady=5)
    # 融托优选
    tk.Button(root, text="融托优选", command=lambda: choose_application(2)).grid(row=0, column=2, padx=10, pady=5)

    root.mainloop()


#  选择app的打包程序
def choose_application(types):
    if types == 0:
        print("融托金融")
        root.destroy()  # 关闭窗口

        RecommendGUI.create_window()  # 打开融托金融的打包程序
    elif types == 1:
        print("融米小管家")
    else:
        print("融托优选")
        root.destroy()
        RTYXHomePage.setup_view("融托优选")


if __name__ == '__main__':
    setup_view()
