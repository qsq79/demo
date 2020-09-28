# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter as tk
import tkinter.messagebox as msg
import pymysql
import os
import user
import manage

BACK_PATH="resources"+os.sep+"resources.jpg"

def exit1():
    root.destroy()
    user.frame()

def exit2():
    root.destroy()
    manage.frame()
    
def exit_login():
    root.destroy()
    frame()
    
def frame():
    global root
    root = tk.Tk()
    root.title('CUMT图书系统')
    #photo=tk.PhotoImage(file = "C:/Users/quan/Desktop/python++/项目经历/图书管理系统/resources.jpg")
    root.geometry("700x260")
    #theLabel = tk.Label(root,image = photo,compound = tk.CENTER,fg = "white").grid(row=0,column=0)
    labe1 = tk.Label(root, text="欢迎来到CUMT图书系统，请选择用户类型：", font=36).grid(row=0, column=1)
    tk.Button(root, text='普通用户',width=10,height=2, command=exit1).grid(row=1, column=1)
    tk.Button(root, text='管理员',width=10,height=2, command=exit2).grid(row=2, column=1)
    tk.Button(root, text='退出',width=10,height=2,command=exit_login).grid(row=8, column=2)
    root.mainloop()


if __name__ == '__main__':
    frame()