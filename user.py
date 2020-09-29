# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 16:33:41 2020

@author: quan
"""

import tkinter as tk
import tkinter.messagebox as msg
import pymysql
import os
import login

BACK_PATH="resources"+os.sep+"background.gif"

def check_book():
    db = pymysql.connect("localhost", "root", "root", "library")
    cursor = db.cursor() #创建一个游标对象,python里的sql语句都要通过cursor来执行
    a = input_book.get()
    sql = "SELECT * FROM book WHERE bname = '%s'" % (a)
    cursor.execute(sql) #执行sql语句
    results = cursor.fetchone() 
    if results:
        root3 = tk.Tk()
        root3.title('查询到的书')
        val = "您要查询的书号为：%s" % (results[0])
        print2 = tk.Label(root3, text=val)
        print2.grid(row=1, column=0, padx=10, pady=5)
        val = "您要查询的书的作者为：%s" % (results[1])
        print3 = tk.Label(root3, text=val)
        print3.grid(row=2, column=0, padx=10, pady=5)
        val = "您要查询的书的剩余库存为：%s" % (results[2])
        print4 = tk.Label(root3, text=val)
        print4.grid(row=3, column=0, padx=10, pady=5)
        val = "您要查询的书名为：%s" % (results[3])
        print5 = tk.Label(root3, text=val)
        print5.grid(row=4, column=0, padx=10, pady=5)
        val = "您要查询的书的出版日期为：%s" % (results[4])
        print6 = tk.Label(root3, text=val)
        print6.grid(row=5, column=0, padx=10, pady=5)
    else:
        msg._show(title='错误', message='没有查到您要查询的记录')
    db.close()

def borrow_end():
    db = pymysql.connect("localhost", "root", "root", "library")
    cursor = db.cursor()
    name = input8.get()
    #name = "Java"
    sql = "SELECT bid,num FROM book WHERE bname='%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchone()  #返回单个的元组，也就是一条记录(row)，如果没有结果 则返回 None
                                    #fetchall()
                                 #row_2 = cursor.fetchmany(3)  获取前三行数据，元组包含元组
    sql = "SELECT lid, rid FROM borrow order by lid desc"
    cursor.execute(sql)
    l = cursor.fetchone()
    
    if results:
       if results[1] > 0:
           if l is None:
               sql = "INSERT INTO borrow(lid, rid, bid, btime) VALUES(%s, %s, %s, CURDATE())" % (1, id, results[0])
           else:
               lid = l[0]+1
               sql = "INSERT INTO borrow(lid, rid, bid, btime) VALUES(%s, %s, %s, CURDATE())" % (lid, id, results[0])
           #cursor.execute(sql)
           try:
               #sql = "INSERT INTO borrow(lid, rid, bid, btime) VALUES(%s, %s, CURDATE())" % (1, id, results[0])
               cursor.execute(sql)
               db.commit()
               msg._show(title="成功",message="借阅成功！")
           except:
               msg._show(title="系统故障",message="借阅失败！")
       else:           
           msg._show(title="库存量不足",message="对不起，您要借阅的图书库存不足！")
    else:
         msg._show(title="失败",message="没有找到您要借的书！")
    db.close()

def return_end():
    db = pymysql.connect("localhost", "root", "root", "library")
    cursor = db.cursor()
    name = input9.get()
    sql = "SELECT bid FROM book WHERE bname = '%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchone()
    
    sql = "SELECT lid FROM borrow WHERE bid='%s' AND rid='%s' and rtime is null" % (results[0], id)
    #    = "SELECT lid FROM borrow WHERE bid=2 AND rid = 123 and rtime is null;"
    cursor.execute(sql)
    result = cursor.fetchone()
    sql = "UPDATE borrow SET rtime = CURDATE() WHERE lid= %s"%(result[0])
    try:
        cursor.execute(sql)
        db.commit()
        msg._show(title='成功',message='还书成功')
    except:
        msg._show(title='系统故障',message='还书失败')
    db.close()

def donate_end():
    db = pymysql.connect("localhost", "root", "root", "library")
    cursor = db.cursor()
    name = input10.get()
    amount = input11.get()
    write = input12.get()
    tim= input13.get()
    sql = "SELECT num FROM book WHERE bname='%s'" % (name)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
        sql = "UPDATE book SET num=num+%s WHERE bname='%s'" % (amount, name)
        try:
            cursor.execute(sql)
            db.commit()
            msg._show(title="成功",message="捐书成功！谢谢您")
        except:
            msg._show(title="系统故障",message="捐书失败")
            db.rollback()
    else:
        sql = "INSERT INTO book(writer,num,bname,ptime) VALUES ('%s',%s,'%s','%s')" % ( write, amount, name, tim)
        try:
            cursor.execute(sql)
            db.commit()
            msg._show(title="成功", message="捐书成功！谢谢您")
        except:
            msg._show(title="错误", message="输入信息有误")
            db.rollback()
    db.close()

def book_select():
    v1=tk.StringVar()
    global root2
    root2=tk.Tk()
    root2.title("查询图书")
    global input_book
    labe1 = tk.Label(root2, text="请输入您要查询的图书名：", font=36).grid(row=0, column=0)
    input_book = tk.Entry(root2,textvariable=v1)
    input_book.grid(row=0,column=1)
    tk.Button(root2, text='确认', width=10, command=check_book).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=1, column=1, sticky=tk.E, padx=10, pady=5)

def book_borrow():
    db = pymysql.connect("localhost", "root", "root", "library")
    cursor = db.cursor()
    sql = "SELECT bleft FROM reader WHERE rid = %s" % (id)
    cursor.execute(sql)
    result = cursor.fetchone()
    v_borrow=tk.StringVar()
    if result[0] == 0:
        msg._show(title="错误",message="你已达最大借阅量，借阅失败")
    global root2
    root2 = tk.Tk()
    root2 .title("借阅")
    global input8
    labe1 = tk.Label(root2, text="请输入您要借阅的图书名：", font=36).grid(row=0, column=0)
    input8 = tk.Entry(root2, textvariable=v_borrow)
    input8.grid(row=1,column=0)
    tk.Button(root2, text='确认', width=10, command=borrow_end).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)
    db.close()

def return_book():
    global root2
    root2 = tk.Tk()
    root2.title("还书")
    v1=tk.StringVar()
    global input9
    labe1 = tk.Label(root2, text="请输入您要还的图书名：", font=36).grid(row=0, column=0)
    input9 = tk.Entry(root2, textvariable=v1)
    input9.grid(row=1, column=0)
    tk.Button(root2, text='确认', width=10, command=return_end).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)

def donate_book():
    global root2
    root2 = tk.Tk()
    root2.title("捐书")
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()
    global input10,input11,input12,input13
    labe1 = tk.Label(root2, text="请输入您要捐赠的图书名：", font=36).grid(row=0, column=0)
    labe12 = tk.Label(root2, text="请输入您要捐赠的图书的数量：", font=36).grid(row=1, column=0)
    labe13 = tk.Label(root2, text="请输入您要捐赠的作者：", font=36).grid(row=2, column=0)
    labe4 = tk.Label(root2, text="请输入您要捐赠的图书的出版时间：", font=36).grid(row=3, column=0)
    input10 = tk.Entry(root2, textvariable=v1)
    input10.grid(row=0, column=1)
    input11 = tk.Entry(root2, textvariable=v2)
    input11.grid(row=1, column=1)
    input12 = tk.Entry(root2, textvariable=v3)
    input12.grid(row=2, column=1)
    input13 = tk.Entry(root2, textvariable=v4)
    input13.grid(row=3, column=1)
    tk.Button(root2, text='确认', width=10, command=donate_end).grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=4, column=1, sticky=tk.E, padx=10, pady=5)


def success_tip():
    root.destroy()
    root1.destroy()
    global rootx
    rootx = tk.Tk()
    rootx.title('CUMT图书用户系统')
    labe1 = tk.Label(rootx,text="欢迎来到CUMT图书管理系统，请选择您要进行的操作：", font=36).grid(row=0, column=0)
    tk.Button(rootx, text='查询图书',  width=50,height=2, command=book_select).grid(row=1, column=0)
    tk.Button(rootx, text='借阅图书',  width=50,height=2, command=book_borrow).grid(row=2, column=0)
    tk.Button(rootx, text='归还图书',  width=50,height=2, command=return_book).grid(row=3,  column=0)
    tk.Button(rootx, text='捐赠图书',  width=50,height=2, command=donate_book).grid(row=4, column=0)
    tk.Button(rootx, text='退出', width=50,height=2,command=exit_loginx).grid(row=5,column=0)
    rootx.mainloop()

def exit_login2():
    root1.destroy()

def exit_loginx():
    rootx.destroy()
    frame()

def login_check():
    db = pymysql.connect("localhost", "root", "root", "library")
    cursor = db.cursor()
    passward=input2.get()
    global id
    id = input_id.get()
    sql = "SELECT rpassward FROM rpass WHERE rid='%s'" % (id)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results:
            if passward == results[0]:
                success_tip()
            else:
               msg._show(title='错误！',message='账号密码输入错误！')
    else:
        msg._show(title='错误！',message='您输入的用户不存在！')
    db.close()

def auto_login():
    global root1
    root1 = tk.Tk()
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    root1.title("登入")
    labe1=tk.Label(root1,text="学号：",font=36).grid(row=0, column=0)
    label2=tk.Label(root1,text="密码：",font=36).grid(row=1,column=0)
    global input_id,input2
    input_id = tk.Entry(root1, textvariable=v1)
    input_id.grid(row=0, column=1, padx=10, pady=5)
    input2 = tk.Entry(root1, textvariable=v2, show='*')
    input2.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root1, text='登录', width=10, command=login_check).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root1, text='退出', width=10, command=exit_login2).grid(row=3, column=1, sticky=tk.E, padx=10, pady=5)

def exit_login():
    root.destroy()
    login.frame()

def exit_login3():
    root2.destroy()

def resiger_end():
    db = pymysql.connect("localhost", "root", "root", "library")
    cursor = db.cursor()
    rid = input1.get()
    name = input2.get()
    passward = input3.get()
    sex = input4.get()
    clas = input5.get()
    sql = "INSERT INTO reader VALUES(%s,'%s','%s','%s',10)" % (rid, name, sex, clas)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        msg._show(title='错误', message='注册失败！')
    sql = "INSERT INTO rpass VALUES(%s,'%s')" % (rid, passward)
    try:
        cursor.execute(sql)
        db.commit()
        msg._show(title='成功', message='注册成功！')
    except:
        msg._show(title='错误', message='注册失败！')
        db.rollback()
    db.close()

def resiger():
    global  root2
    root2 = tk.Tk()
    root2.title("注册")
    labe1  = tk.Label(root2, text="学号：", font=36).grid(row=0,column=0)
    label2 = tk.Label(root2, text="姓名：", font=36).grid(row=1,column=0)
    label3 = tk.Label(root2, text="密码：", font=36).grid(row=2,column=0)
    label4 = tk.Label(root2,text="性别：",font=36).grid(row=3,column=0)
    label5 = tk.Label(root2,text="班级：",font=36).grid(row=4,column=0)
    v1 = tk.StringVar()
    v2 = tk.StringVar()
    v3 = tk.StringVar()
    v4 = tk.StringVar()
    v5 = tk.StringVar()
    global input1,input2,input3,input4,input5
    input1 = tk.Entry(root2, textvariable=v1)
    input1.grid(row=0, column=1, padx=10, pady=5)
    input2 = tk.Entry(root2, textvariable=v2)
    input2.grid(row=1, column=1, padx=10, pady=5)
    input3 = tk.Entry(root2, textvariable=v3, show='*')
    input3.grid(row=2, column=1, padx=10, pady=5)
    input4 = tk.Entry(root2, textvariable=v4)
    input4.grid(row=3, column=1, padx=10, pady=5)
    input5 = tk.Entry(root2, textvariable=v5,)
    input5.grid(row=4, column=1, padx=10, pady=5)
    tk.Button(root2, text='确认', width=10, command=resiger_end).grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
    tk.Button(root2, text='取消', width=10, command=exit_login3).grid(row=5, column=1, sticky=tk.E, padx=10, pady=5)

def frame():
    global root
    root = tk.Tk()
    root.title('CUMT图书用户系统登录')
    root.geometry("280x310")
   # photo=tk.PhotoImage(file=BACK_PATH)
    #theLabel = tk.Label(root,image = photo,compound = tk.CENTER,fg = "white").grid(row=0,column=0)
    tk.Button(root, text='登入', width=10,height=2, command=auto_login).grid(row=1, column=0,)
    tk.Button(root, text='注册', width=10,height=2, command=resiger).grid(row=2, column=0)
    tk.Button(root, text='退出',width=10,height=2,command=exit_login).grid(row=3, column=0)
    root.mainloop()