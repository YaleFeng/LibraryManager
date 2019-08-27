import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import os
from datetime import datetime
from pandas import *
import numpy as np
import matplotlib.pyplot as plt

width = 800
height = 450
TotalNum = 7

class basedesk():
    def __init__(self,master):
        self.root = master
        self.root.config()
        # title
        self.root.title('Base page')
        # get the size of screen and take the window appears at the center of the screen
        self.screenwidth = root.winfo_screenwidth()  
        self.screenheight = root.winfo_screenheight()          
        self.size = '%dx%d+%d+%d' % (width, height, (self.screenwidth - width)/2, (self.screenheight - height)/2)  
        self.root.geometry(self.size)
        # set the maximum size and the minimum size
        self.root.maxsize(width * 2, height * 2)
        self.root.minsize(width, height) 

        init_face(self.root)        

columns = ("图书ID", "图书名称", "图书类别", "卖出时间", "买家姓名", "买家年龄", "所属箱")
class init_face():
    def __init__(self,master):

        self.master = master
        self.master.config(bg='white')
        self.select = None
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()        
        
        self.intermediate1 = tk.StringVar()
        self.intermediate1.set('')        
        
        # set the frame of the window      
        # list:
        self.treebox = ttk.Treeview(self.master, show = 'headings', columns = columns)
        self.ysb = ttk.Scrollbar(self.treebox, orient="vertical", command=self.treebox.yview)  #y滚动条
        self.xsb = ttk.Scrollbar(self.treebox, orient="horizontal",command=self.treebox.xview) #x滚动条
        self.treebox.configure(yscroll=self.ysb.set,xscroll=self.xsb.set) #y滚动条关联
        #self.treebox.bind("<<TreeviewSelect>>",self.gosel) #事件(选中)绑定     
        self.treebox.column("图书ID", width=50, anchor='center') # 表示列,不显示
        self.treebox.column("图书名称", width=100, anchor='center')
        self.treebox.column("图书类别", width=50, anchor='center')
        self.treebox.column("卖出时间", width=50, anchor='center')
        self.treebox.column("买家姓名", width=50, anchor='center')
        self.treebox.column("买家年龄", width=50, anchor='center')
        self.treebox.column("所属箱", width=50, anchor='center')
         
        self.treebox.heading("图书ID", text="图书ID") # 显示表头
        self.treebox.heading("图书名称", text="图书名称")
        self.treebox.heading("图书类别", text="图书类别")
        self.treebox.heading("卖出时间", text="卖出时间")
        self.treebox.heading("买家姓名", text="买家姓名")
        self.treebox.heading("买家年龄", text="买家年龄")
        self.treebox.heading("所属箱", text="所属箱")
        
        self.treebox.place(relx=0.0, rely=0.0, relwidth=0.8, relheight=1.0)
        self.ysb.pack(side = 'right', fill = 'y')
        self.xsb.pack(side = 'bottom', fill = 'x')
        self.show_list()
        self.treebox.bind('<ButtonRelease-1>', self.selectItem)
        
        # button:
        self.frame_btn = tk.Frame(self.master)
        self.frame_btn.place(relx=0.8, rely=0.0, relwidth=0.2, relheight=1.0)
        btn_add = tk.Button(self.frame_btn,text='添加新书',command=self.change_add, relief = 'sunken', activebackground='grey')
        #btn_add.grid(row=0, pady=10)
        btn_add.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.1)
        btn_edit = tk.Button(self.frame_btn,text='编辑状态',command=self.change_edit, relief = 'sunken', activebackground='grey')
        #btn_edit.grid(row=1, pady=10)
        btn_edit.place(relx = 0.1, rely = 0.3, relwidth = 0.8, relheight = 0.1)
        btn_stat = tk.Button(self.frame_btn,text='统计结果',command=self.change_stat, relief = 'sunken', activebackground='grey')
        #btn_stat.grid(row=2, pady=10)
        btn_stat.place(relx = 0.1, rely = 0.5, relwidth = 0.8, relheight = 0.1)
        btn_editBox = tk.Button(self.frame_btn,text='按箱操作',command=self.change_edit_box, relief = 'sunken', activebackground='grey')
        #btn_stat.grid(row=2, pady=10)
        btn_editBox.place(relx = 0.1, rely = 0.7, relwidth = 0.8, relheight = 0.1)     
        self.enter = tk.Entry(self.frame_btn, textvariable = self.intermediate1)
        self.enter.place(relx = 0.15, rely = 0.8, relwidth = 0.7, relheight = 0.08)        
    
    def show_list(self):
        cursor = self.c.execute("SELECT * from Library")
        array = [[],[],[],[],[],[],[]]
        for row in cursor:
            for i in range(TotalNum):
                array[i].append(str(row[i]))
            
        for i in range(len(array[0])): # 写入数据
            self.treebox.insert('', i, values=(array[0][i], array[1][i], array[2][i], array[3][i], array[4][i], array[5][i], array[6][i]))   

    # 点击新建列
    def change_add(self):       
        self.treebox.destroy()
        self.frame_btn.destroy()
        self.conn.close()    
        add_new_face(self.master)
        
    # 点击编辑列
    def change_edit(self):
        if self.select is not None:
            self.treebox.destroy()
            self.frame_btn.destroy()
            self.conn.close()    
            edit_face(self.master, self.select)
        else:
            tc=messagebox.showinfo(title='Error',message='未选定要更改项目')
        
    # 点击统计列
    def change_stat(self):       
        self.treebox.destroy()
        self.frame_btn.destroy()
        self.conn.close()    
        stat_face(self.master)    
        
        
    def change_edit_box(self):
        if self.intermediate1.get() is not '':
            query = "SELECT MAX(ID) FROM Library WHERE BOX = '%s';" %(self.intermediate1.get())
            cursor = self.c.execute(query) 
            for row in cursor:
                if row[0] == None:
                    tc=messagebox.showinfo(title='Error',message='选择箱不存在')
                else:
                    self.treebox.destroy()
                    self.frame_btn.destroy()
                    self.conn.close()    
                    edit_face_box(self.master, self.intermediate1.get())
        else:
            tc=messagebox.showinfo(title='Error',message='未指定选择箱')


    def selectItem(self, a):
        curItem = self.treebox.focus()
        self.select = self.treebox.item(curItem)['values'][0]

# 编辑页面
class edit_face():
    def __init__(self, master, ID):
        self.master = master
        self.master.config(bg='white')
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()      
        
        self.ID = ID
        self.intermediate1 = tk.StringVar()
        self.intermediate1.set('')
        self.intermediate2 = tk.StringVar()
        self.intermediate2.set('')
        self.intermediate3 = tk.StringVar()
        self.intermediate3.set('')
        self.intermediate4 = tk.StringVar()
        self.intermediate4.set('')
        self.intermediate5 = tk.StringVar()
        self.intermediate5.set('')
        self.intermediate6 = tk.StringVar()
        self.intermediate6.set('')
        self.intermediate7 = tk.StringVar()
        self.intermediate7.set('')
        
        self.face1 = tk.Frame(self.master)
        self.face1.place(relx = 0.0, rely = 0.0, relwidth = 1.0, relheight = 1.0)
        
        # label
        self.label1 = tk.Label(self.face1, text = '图书ID:')
        self.label1.place(relx = 0.2, rely = 0.1, relwidth = 0.2, relheight = 0.08)
        self.label2 = tk.Label(self.face1, text = '图书名称:')
        self.label2.place(relx = 0.2, rely = 0.2, relwidth = 0.2, relheight = 0.08)
        self.label3 = tk.Label(self.face1, text = '图书类别:')
        self.label3.place(relx = 0.2, rely = 0.3, relwidth = 0.2, relheight = 0.08)
        self.label4 = tk.Label(self.face1, text = '卖出时间:')
        self.label4.place(relx = 0.2, rely = 0.4, relwidth = 0.2, relheight = 0.08)
        self.label5 = tk.Label(self.face1, text = '买家姓名:')
        self.label5.place(relx = 0.2, rely = 0.5, relwidth = 0.2, relheight = 0.08)
        self.label6 = tk.Label(self.face1, text = '买家年龄:')
        self.label6.place(relx = 0.2, rely = 0.6, relwidth = 0.2, relheight = 0.08)
        self.label7 = tk.Label(self.face1, text = '所属箱:')
        self.label7.place(relx = 0.2, rely = 0.7, relwidth = 0.2, relheight = 0.08)        
        
        # input
        self.entry1 = tk.Entry(self.face1, textvariable = self.intermediate1, state = 'disable')
        self.entry1.place(relx = 0.6, rely = 0.1, relwidth = 0.2, relheight = 0.08)
        self.entry2 = tk.Entry(self.face1, textvariable = self.intermediate2)
        self.entry2.place(relx = 0.6, rely = 0.2, relwidth = 0.2, relheight = 0.08)
        self.entry3 = tk.Entry(self.face1, textvariable = self.intermediate3)
        self.entry3.place(relx = 0.6, rely = 0.3, relwidth = 0.2, relheight = 0.08)
        self.entry4 = tk.Entry(self.face1, textvariable = self.intermediate4)
        self.entry4.place(relx = 0.6, rely = 0.4, relwidth = 0.2, relheight = 0.08)
        self.entry5 = tk.Entry(self.face1, textvariable = self.intermediate5)
        self.entry5.place(relx = 0.6, rely = 0.5, relwidth = 0.2, relheight = 0.08)
        self.entry6 = tk.Entry(self.face1, textvariable = self.intermediate6)
        self.entry6.place(relx = 0.6, rely = 0.6, relwidth = 0.2, relheight = 0.08)     
        self.entry7 = tk.Entry(self.face1, textvariable = self.intermediate7)
        self.entry7.place(relx = 0.6, rely = 0.7, relwidth = 0.2, relheight = 0.08)          
        
        # 按钮
        self.btn_back = tk.Button(self.face1,text='确认',command=self.change, activebackground='grey')
        self.btn_back.place(relx = 0.3, rely = 0.8, relwidth = 0.1, relheight = 0.1)
        self.btn_back2 = tk.Button(self.face1,text='取消',command=self.back, activebackground='grey')
        self.btn_back2.place(relx = 0.6, rely = 0.8, relwidth = 0.1, relheight = 0.1)       
        self.show()
        
    def show(self):
        # 从数据库得到数据
        # 逐行添加到entry里面
        query = "SELECT * FROM Library WHERE ID = '%d';" %int(self.ID)
        cursor = self.c.execute(query) 
        #self.label1.text
        for row in cursor: 
            self.intermediate1.set(row[0])
            self.intermediate2.set(row[1])
            self.intermediate3.set(row[2])
            self.intermediate4.set(row[3])
            self.intermediate5.set(row[4])
            self.intermediate6.set(row[5])
            self.intermediate7.set(row[6])

    def back(self):
        self.face1.destroy()
        self.c.close()
        self.conn.close()        
        init_face(self.master)

    def change(self):
        # 输入年龄检测
        try:
            int(self.intermediate6.get())
        except ValueError:
            tc = messagebox.showinfo(title='Error',message='买家年龄应为数字')
        else:        
            # 输入日期检测
            try:
                date_time = datetime.strptime(self.intermediate4.get(),'%Y-%m-%d')
            except ValueError:
                tc = messagebox.showinfo(title='Error',message='时间格式不符')      
            else:
                
                query = "UPDATE Library SET NAME = '%s', TYPE = '%s', SALE_TIME = '%s', SALE_NAME = '%s', SALE_AGE = %d, BOX = '%s' WHERE ID = %d;" %(self.intermediate2.get(),
                                                                                                                                           self.intermediate3.get(), self.intermediate4.get(),
                                                                                                                                            self.intermediate5.get(), int(self.intermediate6.get()),
                                                                                                                                            self.intermediate7.get(), int(self.intermediate1.get()))
                self.c.execute(query)
                self.conn.commit()
        
                self.face1.destroy()
                self.c.close()
                self.conn.close()                
                init_face(self.master)
               
# 添加页面 
class add_new_face():
    def __init__(self, master):
        self.master = master
        self.master.config(bg='white')
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()      
        query = 'SELECT MAX(ID) FROM Library'
        cursor = self.c.execute(query) 

        self.intermediate1 = tk.StringVar()
        # if there is no book existed, add num 1
        for row in cursor: 
            if row[0] == None:
                self.intermediate1.set(1)
            else:
                self.num = int(row[0]) + 1             
                self.intermediate1.set(str(self.num))
        self.intermediate2 = tk.StringVar()
        self.intermediate2.set('')
        self.intermediate3 = tk.StringVar()
        self.intermediate3.set('')
        self.intermediate4 = tk.StringVar()
        self.intermediate4.set('')
        self.intermediate5 = tk.StringVar()
        self.intermediate5.set('')
        self.intermediate6 = tk.StringVar()
        self.intermediate6.set('')
        self.intermediate7 = tk.StringVar()
        self.intermediate7.set('')
        
        self.face1 = tk.Frame(self.master)
        self.face1.place(relx = 0.0, rely = 0.0, relwidth = 1.0, relheight = 1.0)
        
        # label
        self.label1 = tk.Label(self.face1, text = '图书ID:')
        self.label1.place(relx = 0.2, rely = 0.1, relwidth = 0.2, relheight = 0.08)
        self.label2 = tk.Label(self.face1, text = '图书名称:')
        self.label2.place(relx = 0.2, rely = 0.2, relwidth = 0.2, relheight = 0.08)
        self.label3 = tk.Label(self.face1, text = '图书类别:')
        self.label3.place(relx = 0.2, rely = 0.3, relwidth = 0.2, relheight = 0.08)
        self.label4 = tk.Label(self.face1, text = '卖出时间:')
        self.label4.place(relx = 0.2, rely = 0.4, relwidth = 0.2, relheight = 0.08)
        self.label5 = tk.Label(self.face1, text = '买家姓名:')
        self.label5.place(relx = 0.2, rely = 0.5, relwidth = 0.2, relheight = 0.08)
        self.label6 = tk.Label(self.face1, text = '买家年龄:')
        self.label6.place(relx = 0.2, rely = 0.6, relwidth = 0.2, relheight = 0.08)
        self.label7 = tk.Label(self.face1, text = '所属箱:')
        self.label7.place(relx = 0.2, rely = 0.7, relwidth = 0.2, relheight = 0.08)        
        
        # input
        self.entry1 = tk.Entry(self.face1, textvariable = self.intermediate1, state = 'disable')
        self.entry1.place(relx = 0.6, rely = 0.1, relwidth = 0.2, relheight = 0.08)
        self.entry2 = tk.Entry(self.face1, textvariable = self.intermediate2)
        self.entry2.place(relx = 0.6, rely = 0.2, relwidth = 0.2, relheight = 0.08)
        self.entry3 = tk.Entry(self.face1, textvariable = self.intermediate3)
        self.entry3.place(relx = 0.6, rely = 0.3, relwidth = 0.2, relheight = 0.08)
        self.entry4 = tk.Entry(self.face1, textvariable = self.intermediate4, state = 'disable')
        self.entry4.place(relx = 0.6, rely = 0.4, relwidth = 0.2, relheight = 0.08)
        self.entry5 = tk.Entry(self.face1, textvariable = self.intermediate5, state = 'disable')
        self.entry5.place(relx = 0.6, rely = 0.5, relwidth = 0.2, relheight = 0.08)
        self.entry6 = tk.Entry(self.face1, textvariable = self.intermediate6, state = 'disable')
        self.entry6.place(relx = 0.6, rely = 0.6, relwidth = 0.2, relheight = 0.08)     
        self.entry7 = tk.Entry(self.face1, textvariable = self.intermediate7)
        self.entry7.place(relx = 0.6, rely = 0.7, relwidth = 0.2, relheight = 0.08)          
        
        # 按钮
        self.btn_back = tk.Button(self.face1,text='确认',command=self.change, activebackground='grey')
        self.btn_back.place(relx = 0.3, rely = 0.8, relwidth = 0.1, relheight = 0.1)
        self.btn_back2 = tk.Button(self.face1,text='取消',command=self.back, activebackground='grey')
        self.btn_back2.place(relx = 0.6, rely = 0.8, relwidth = 0.1, relheight = 0.1)       

    def back(self):
        self.face1.destroy()
        self.c.close()
        self.conn.close()        
        init_face(self.master)

    def change(self):
        # 输入不为空
        if self.intermediate1.get() == '' or self.intermediate2.get() == '' or self.intermediate3.get() == '':
            tc = messagebox.showinfo(title='Error',message='请输入完整信息')
        else:   
            query = "INSERT INTO Library (ID, NAME, TYPE, BOX) VALUES (?, ?, ?, ?);"
            self.c.execute(query, [int(self.intermediate1.get()), self.intermediate2.get(), self.intermediate3.get(), self.intermediate7.get()])
            self.conn.commit()
        
            self.face1.destroy()
            self.c.close()
            self.conn.close()            
            init_face(self.master)
     
#统计页面       
class stat_face():
    def __init__(self, master):
        self.master = master
        self.master.config(bg='white')
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()      
            
        # list:
        self.treebox = ttk.Treeview(self.master, show = 'headings', columns = columns)
        self.ysb = ttk.Scrollbar(self.treebox, orient="vertical", command=self.treebox.yview)  #y滚动条
        self.xsb = ttk.Scrollbar(self.treebox, orient="horizontal",command=self.treebox.xview) #x滚动条
        self.treebox.configure(yscroll=self.ysb.set,xscroll=self.xsb.set) #y滚动条关联
        #self.treebox.bind("<<TreeviewSelect>>",self.gosel) #事件(选中)绑定     
        self.treebox.column("图书ID", width=50, anchor='center') # 表示列,不显示
        self.treebox.column("图书名称", width=100, anchor='center')
        self.treebox.column("图书类别", width=50, anchor='center')
        self.treebox.column("卖出时间", width=50, anchor='center')
        self.treebox.column("买家姓名", width=50, anchor='center')
        self.treebox.column("买家年龄", width=50, anchor='center')
        self.treebox.column("所属箱", width=50, anchor='center')
             
        self.treebox.heading("图书ID", text="图书ID") # 显示表头
        self.treebox.heading("图书名称", text="图书名称")
        self.treebox.heading("图书类别", text="图书类别")
        self.treebox.heading("卖出时间", text="卖出时间")
        self.treebox.heading("买家姓名", text="买家姓名")
        self.treebox.heading("买家年龄", text="买家年龄")
        self.treebox.heading("所属箱", text="所属箱")
            
        self.treebox.place(relx=0.0, rely=0.2, relwidth=1.0, relheight=0.8)
        self.ysb.pack(side = 'right', fill = 'y')
        self.xsb.pack(side = 'bottom', fill = 'x')
        self.show_list()
        
        # menu
        self.variable = tk.StringVar()
        self.variable.set('')
        
        self.face1 = tk.Frame(self.master)
        self.face1.place(relx = 0.0, rely = 0.0, relwidth = 1.0, relheight = 0.2)
        
        self.menu = tk.OptionMenu(self.face1, self.variable, '年龄分类', '类别分类', '时间分类')
        self.menu.place(relx = 0.2, rely = 0.2, relwidth = 0.15, relheight = 0.4)
        
        # label & Button
        self.label1 = tk.Label(self.face1, text = '请选择统计类别:')
        self.label1.place(relx = 0.05, rely = 0.2, relwidth = 0.15, relheight = 0.4)
        self.click = tk.Button(self.face1, text = '确认', command = self.change, activebackground='grey')
        self.click.place(relx = 0.75, rely = 0.2, relwidth = 0.15, relheight = 0.4)
        self.backB = tk.Button(self.face1, text = '返回', command = self.back, activebackground = 'grey')
        self.backB.place(relx = 0.0, rely = 0.0, relwidth = 0.1, relheight = 0.25)
        
        # Set Range
        self.lowRange = tk.StringVar()
        self.lowRange.set('')
        self.highRange = tk.StringVar()
        self.highRange.set('')        
        self.entryL = tk.Entry(self.face1, textvariable = self.lowRange)
        self.lineLabel = tk.Label(self.face1, text = '————')
        self.entryH = tk.Entry(self.face1, textvariable = self.highRange)
        self.entryL.place(relx = 0.4, rely = 0.2, relwidth = 0.1, relheight = 0.3)
        self.lineLabel.place(relx = 0.5, rely = 0.2, relwidth = 0.1, relheight = 0.3)
        self.entryH.place(relx = 0.6, rely = 0.2, relwidth = 0.1, relheight = 0.3)        
        
    def show_list(self):
        cursor = self.c.execute("SELECT * from Library")
        array = [[],[],[],[],[],[],[]]
        for row in cursor:
            for i in range(TotalNum):
                array[i].append(str(row[i]))
            
        for i in range(len(array[0])): # 写入数据
            self.treebox.insert('', i, values=(array[0][i], array[1][i], array[2][i], array[3][i], array[4][i], array[5][i], array[6]    [i]))   
            
            
    def back(self):
        self.treebox.destroy()
        self.face1.destroy()
        self.c.close()
        self.conn.close()
        init_face(self.master)

    def change(self):
        # 检查输入格式
        plt.rcParams['font.sans-serif']=['SimHei']
        if self.variable.get() == '年龄分类':
            if self.lowRange.get() == '' and self.highRange.get() == '':
                query = "SELECT SALE_AGE, COUNT(*) FROM Library where SALE_AGE GROUP BY SALE_AGE;"
                cursor = self.c.execute(query) 
                data = cursor.fetchall()
                label = []
                num = []
                for d in data:
                    label.append(d[0])
                    num.append(d[1])
                plt.pie(x = num, labels = label, autopct = '%.3f%%', pctdistance = 0.7, labeldistance = 1.1)
                plt.title("按所选年龄段分类")
                plt.show()
            else:
                try:
                    int(self.lowRange.get())
                    int(self.highRange.get())
                except ValueError:
                    tc = messagebox.showinfo(title='Error',message='年龄应为数字')
                else:
                    if int(self.lowRange.get()) < int(self.highRange.get()) and int(self.lowRange.get()) > 0:
                        query = "SELECT SALE_AGE, COUNT(*) FROM Library where SALE_AGE Between %d and %d GROUP BY SALE_AGE;" %(int(self.lowRange.get()), int(self.highRange.get()))
                        cursor = self.c.execute(query) 
                        data = cursor.fetchall()
                        label = []
                        num = []
                        for d in data:
                            label.append(d[0])
                            num.append(d[1])
                        plt.pie(x = num, labels = label, autopct = '%.3f%%', pctdistance = 0.7, labeldistance = 1.1)
                        plt.title("按所选年龄段分类")
                        plt.show()
                    
        elif self.variable.get() == '类别分类':
            query = "SELECT TYPE, COUNT(*) FROM Library GROUP BY TYPE;"
            cursor = self.c.execute(query) 
            data = cursor.fetchall()
            label = []
            num = []
            for d in data:
                label.append(d[0])
                num.append(d[1])
            plt.pie(x = num, labels = label, autopct = '%.3f%%', pctdistance = 0.7, labeldistance = 1.1)
            plt.title("按所选类别分类")
            plt.show()
            
        elif self.variable.get() == '时间分类':
            if self.lowRange == '' and self.highRange == '':
                query = "SELECT SALE_TIME, COUNT(*) FROM Library where SALE_TIME Between GROUP BY SALE_TIME;"
                cursor = self.c.execute(query) 
                data = cursor.fetchall()
                label = []
                num = []
                for d in data:
                    label.append(d[0])
                    num.append(d[1])
                plt.pie(x = num, labels = label, autopct = '%.3f%%', pctdistance = 0.7, labeldistance = 1.1)
                plt.title("按所选时间段分类")
                plt.show()
            else:
                try:
                    date_timeLow = datetime.strptime(self.lowRange.get(),'%Y-%m-%d')
                    date_timeHigh = datetime.strptime(self.highRange.get(),'%Y-%m-%d')
                except ValueError:
                    tc = messagebox.showinfo(title='Error',message='年份格式应为: YY-MM-DD')
                else:
                    query = "SELECT SALE_TIME, COUNT(*) FROM Library where SALE_TIME Between '%s' and '%s' GROUP BY SALE_TIME;" %(date_timeLow, date_timeHigh)
                    cursor = self.c.execute(query) 
                    data = cursor.fetchall()
                    label = []
                    num = []
                    for d in data:
                        label.append(d[0])
                        num.append(d[1])
                    plt.pie(x = num, labels = label, autopct = '%.3f%%', pctdistance = 0.7, labeldistance = 1.1)
                    plt.title("按所选时间段分类")
                    plt.show()
        else:
            tc = messagebox.showinfo(title='Error',message='请选择统计类型')


# 编辑页面
class edit_face_box():
    def __init__(self, master, box):
        self.master = master
        self.master.config(bg='white')
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()      
        
        self.box = box
        self.intermediate1 = tk.StringVar()
        self.intermediate1.set('')
        self.intermediate2 = tk.StringVar()
        self.intermediate2.set('')
        self.intermediate3 = tk.StringVar()
        self.intermediate3.set('')
        
        # list
        self.treebox = ttk.Treeview(self.master, show = 'headings', columns = columns)
        self.ysb = ttk.Scrollbar(self.treebox, orient="vertical", command=self.treebox.yview())  #y滚动条
        self.xsb = ttk.Scrollbar(self.treebox, orient="horizontal",command=self.treebox.xview()) #x滚动条
        self.treebox.configure(yscroll=self.ysb.set,xscroll=self.xsb.set) #y滚动条关联
        #self.treebox.bind("<<TreeviewSelect>>",self.gosel) #事件(选中)绑定     
        self.treebox.column("图书ID", width=50, anchor='center') # 表示列,不显示
        self.treebox.column("图书名称", width=100, anchor='center')
        self.treebox.column("图书类别", width=50, anchor='center')
        self.treebox.column("卖出时间", width=50, anchor='center')
        self.treebox.column("买家姓名", width=50, anchor='center')
        self.treebox.column("买家年龄", width=50, anchor='center')
        self.treebox.column("所属箱", width=50, anchor='center')
         
        self.treebox.heading("图书ID", text="图书ID") # 显示表头
        self.treebox.heading("图书名称", text="图书名称")
        self.treebox.heading("图书类别", text="图书类别")
        self.treebox.heading("卖出时间", text="卖出时间")
        self.treebox.heading("买家姓名", text="买家姓名")
        self.treebox.heading("买家年龄", text="买家年龄")
        self.treebox.heading("所属箱", text="所属箱")
        
        self.treebox.place(relx = 0.0, rely = 0.0, relwidth = 0.7, relheight = 1.0)    
        self.ysb.pack(side = 'right', fill = 'y')
        self.xsb.pack(side = 'bottom', fill = 'x')
        self.show_list()        
        
        self.face2 = tk.Frame(self.master)
        self.face2.place(relx = 0.7, rely = 0.0, relwidth = 0.3, relheight = 1.0)            
        
        # label
        self.label1 = tk.Label(self.face2, text = '卖出时间:')
        self.label1.place(relx = 0.1, rely = 0.2, relwidth = 0.4, relheight = 0.08)
        self.label2 = tk.Label(self.face2, text = '买家姓名:')
        self.label2.place(relx = 0.1, rely = 0.4, relwidth = 0.4, relheight = 0.08)
        self.label3 = tk.Label(self.face2, text = '买家年龄:')
        self.label3.place(relx = 0.1, rely = 0.6, relwidth = 0.4, relheight = 0.08)   
        
        # input
        self.entry1 = tk.Entry(self.face2, textvariable = self.intermediate1)
        self.entry1.place(relx = 0.5, rely = 0.2, relwidth = 0.4, relheight = 0.08)
        self.entry2 = tk.Entry(self.face2, textvariable = self.intermediate2)
        self.entry2.place(relx = 0.5, rely = 0.4, relwidth = 0.4, relheight = 0.08)
        self.entry3 = tk.Entry(self.face2, textvariable = self.intermediate3)
        self.entry3.place(relx = 0.5, rely = 0.6, relwidth = 0.4, relheight = 0.08)        
        
        # 按钮
        self.btn_back = tk.Button(self.face2,text='确认',command=self.change, activebackground='grey')
        self.btn_back.place(relx = 0.2, rely = 0.8, relwidth = 0.3, relheight = 0.1)
        self.btn_back2 = tk.Button(self.face2,text='取消',command=self.back, activebackground='grey')
        self.btn_back2.place(relx = 0.6, rely = 0.8, relwidth = 0.3, relheight = 0.1)       
        
    def show_list(self):
        # 从数据库得到数据
        # 逐行添加到entry里面
        query = "SELECT * FROM Library WHERE BOX = '%s';" %(self.box)
        cursor = self.c.execute(query) 
        array = [[],[],[],[],[],[],[]]
        for row in cursor:
            for i in range(TotalNum):
                array[i].append(str(row[i]))
            
        for i in range(len(array[0])): # 写入数据
            self.treebox.insert('', i, values=(array[0][i], array[1][i], array[2][i], array[3][i], array[4][i], array[5][i], array[6][i]))   

    def back(self):
        self.treebox.destroy()
        self.face2.destroy()
        self.c.close()
        self.conn.close()        
        init_face(self.master)

    def change(self):
        # 输入年龄检测
        try:
            int(self.intermediate3.get())
        except ValueError:
            tc = messagebox.showinfo(title='Error',message='买家年龄应为数字')
        else:        
            # 输入日期检测
            try:
                date_time = datetime.strptime(self.intermediate1.get(),'%Y-%m-%d')
            except ValueError:
                tc = messagebox.showinfo(title='Error',message='时间格式不符')      
            else:
                
                query = "UPDATE Library SET SALE_TIME = '%s', SALE_NAME = '%s', SALE_AGE = %d WHERE BOX = '%s';" %(self.intermediate1.get(),
                                                                                                                self.intermediate2.get(), int(self.intermediate3.get()),
                                                                                                                (self.box))
                self.c.execute(query)
                self.conn.commit()
        
                self.treebox.destroy()
                self.face2.destroy()
                self.c.close()
                self.conn.close()                
                init_face(self.master)

if __name__ == '__main__':    
    root = tk.Tk()
    basedesk(root)
    root.mainloop()







# create the database column



#cursor = c.execute("SELECT ID, NAME, TYPE from Library where ID = 1")

#print("writen successfully")
#for row in cursor:
#    print("ID = ",row[0])
#    print("book name = ",row[1])
#    print("book type = ",row[2])
#conn.close()
       
       
#self.c.execute('''CREATE TABLE Library
#       (ID INT PRIMARY KEY     NOT NULL,
#        BOX           CHAR(50),
#       NAME           TEXT    NOT NULL,
#      TYPE           CHAR(50)     NOT NULL,
#       SALE_TIME      DATE,
#       SALE_NAME      CHAR(50),
#       SALE_AGE       INT);''')             