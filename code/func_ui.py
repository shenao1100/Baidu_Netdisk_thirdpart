import tkinter as tk
import time

import Total_Seeting


class Selecter:
    def __init__(self, title, root, x) -> None:
        self.Img = tk.PhotoImage(file='./res/show.png')
        self.count = 0
        self.part_list = []

        self.button_x = 40
        self.button_y = 20
        self.width=x
        self.pack_len = int(self.width / (self.button_x + 3))

        self.main = tk.Frame(root, bg=Total_Seeting.Color0, width=x)
        self.main.grid_propagate(False)
        labelINF = tk.Label(self.main, text='■ ' + title, anchor="nw", compound='center', 
                            image=self.Img, relief='flat', bg=Total_Seeting.Color0,
                            fg='white', width=x).grid(row=0, column=0, padx=5)
        self.bt_main = tk.Frame(self.main, bg=Total_Seeting.Color0)
        self.bt_main.grid(row=1, column=0, padx=5, sticky='w')
        pass

    def do_command(self, command, part):
        for i in self.part_list:
            i['bg'] = Total_Seeting.Color1
        part['bg'] = Total_Seeting.ColorSpecial
        command()

    def add_selection(self, text_list, command_list):
        self.text_list = text_list
        for text, command in zip(text_list, command_list):
            self.count += 1
            self.bt = tk.Button(self.bt_main, text=text, bg=Total_Seeting.Color1,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=self.button_y, 
                                width=self.button_x, image=self.Img)
            self.bt['command'] = lambda t1=command, t2=self.bt: self.do_command(t1, t2)
            self.part_list.append(self.bt)
            self.bt.grid(row=int(self.count / self.pack_len), 
                        column=self.count - (int(self.count / self.pack_len) * self.pack_len), 
                        padx=3, pady=3)
        if int(self.count / self.pack_len) >= 1:
            self.bt_main['height'] = 25 * int(self.count / self.pack_len)
            self.main['height'] = 25 * int(self.count / self.pack_len) + 25
        else:
            self.bt_main['height'] = 25
            self.main['height'] = 50

    def select(self, text):
        count = -1
        for i in self.text_list:
            count += 1
            if i == text:
                break
        self.part_list[count]['bg'] = Total_Seeting.ColorSpecial
        
    def get(self):
        return self.main

class Insert:
    def __init__(self, title, root, x) -> None:
        self.width=x
        self.Img = tk.PhotoImage(file='./res/show.png')
        self.main = tk.Frame(root, bg=Total_Seeting.Color0, width=x, height=50)
        self.main.grid_propagate(False)
        labelINF = tk.Label(self.main, text='■ ' + title, anchor="nw", compound='center', 
                            image=self.Img, relief='flat', bg=Total_Seeting.Color0,
                            fg='white', width=x).grid(row=0, column=0, padx=5)
        self.bt_main = tk.Frame(self.main, bg=Total_Seeting.Color0)
        self.bt_main.grid(row=1, column=0, padx=5, sticky='w')
        pass

    def add_insert(self, text, command):
        self.entry=tk.Entry(self.bt_main, relief='flat', width=int(self.width / 7) - 7)
        self.entry.grid(row=0, column=0, padx=5, sticky='w')
        self.ok_bt = tk.Button(self.bt_main, text='√', bg=Total_Seeting.ColorSpecial,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                command=lambda: command(self.entry.get()),
                                bd=-1, height=20, width=30, image=self.Img)
        self.entry.insert(0, text)
        self.ok_bt.grid(row=0, column=1, padx=5, sticky='w')
        return True

    def get(self):
        return self.main


main_frame = None
tasks_loop = []

#ui part
def initialization():
    global main, mainImg
    mainImg = tk.PhotoImage(file='./res/task.png')
    main = tk.Label(main_frame, text='Here\'s your task!',
                    fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.ColorSpecial,
                    bd=-1, height=40, width=800, image=mainImg, font=(12, ),
                    relief='flat', anchor='w')
    main.grid(row=1024, column=0, padx=0, pady=0)
    pass

def refresh():
    while True:
        if not len(tasks_loop) == 0:
            t_count = 0
            for i in tasks_loop:
                t_count += 1
                if i['inf']['method'] == 'percent':
                    main['text'] = '[' + str(t_count) + '/' + str(len(tasks_loop)) + ']  ' + str(i['inf']['per']) + '% | ' + i['inf']['title']
                else:
                    main['text'] = '[' + str(t_count) + '/' + str(len(tasks_loop)) + ']  ' + i['inf']['title']
                time.sleep(2)
        else:
            time.sleep(0.2)
            main['text'] = '还没有任务欸 (〜￣△￣)〜'

#control part
def add_task(title, method, percent):
    #标题，进度条样式样式，百分比
    count_id = len(tasks_loop) + 1
    tasks_loop.append(
        {
            'id': count_id,
            'inf': {
                'title': title,
                'method': method,
                'per': percent,
            }
        }
    )
    return count_id

def manage_task(count_id, title, method, percent):
    for i in tasks_loop:
        if i['id'] == count_id:
            if title:
                i['inf']['title'] = title
            if method:  
                i['inf']['method'] = method
            if percent:
                i['inf']['per'] = percent
            break
    return True

def delete_task(count_id):
    for i in tasks_loop:
        if i['id'] == count_id:
            tasks_loop.remove(i)
            break
    return True

noticeImg = False
errorImg = False
warnImg = False
notice = False
def showinfo(title, content):
    global noticeImg, notice
    if not noticeImg:
        noticeImg = tk.PhotoImage(file='./res/info.png')
    if notice:
        notice.place_forget()
    notice = tk.Label(main_frame, text=content + '  \n\n[点此关闭]',
            fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.ColorSpecial,
            bd=-1, image=noticeImg, relief='flat', anchor='w')
    notice.place(x=5, y=5)
    notice.bind("<Button-1>", lambda event, t1=notice: 
                            t1.place_forget())

def showerror(title, content):
    global errorImg, notice
    if not errorImg:
        errorImg = tk.PhotoImage(file='./res/error.png')
    if notice:
        notice.place_forget()
    notice = tk.Label(main_frame, text=content + '  \n\n[点此关闭]',
            fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.ColorSpecial,
            bd=-1, image=errorImg, relief='flat', anchor='w')
    notice.place(x=5, y=5)
    notice.bind("<Button-1>", lambda event, t1=notice: 
                            t1.place_forget())

def showwarning(title, content):
    global warnImg, notice
    if not warnImg:
        warnImg = tk.PhotoImage(file='./res/warning.png')
    if notice:
        notice.place_forget()
    notice = tk.Label(main_frame, text=content + '  \n\n[点此关闭]',
            fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.ColorSpecial,
            bd=-1, image=warnImg, relief='flat', anchor='w')
            
    notice.place(x=5, y=5)
    notice.bind("<Button-1>", lambda event, t1=notice: 
                            t1.place_forget())