#-*- coding:utf-8 -*-
#CREATER: ShenAo

import tkinter as tk
import time
import threading

import func_ui
import func_other
import CORE_download
import Total_Seeting

class DownPage:
    page_list = []
    def __init__(self, main_frame: tk.Frame) -> None:
        self.main_frame = main_frame
        self.Img = tk.PhotoImage(file='./res/show.png')
        self.head_section = tk.Frame(self.main_frame, bg=Total_Seeting.Color0)
        self.head_section.grid_propagate(False)
        self.head_section.config(height=25, width=800)
        self.head_section.grid(row=0, column=0, padx=0, pady=0)
        self.main = tk.Frame(self.main_frame, bg=Total_Seeting.Color1)
        self.main.grid_propagate(False)
        self.main.config(height=440, width=800)
        self.main.grid(row=1, column=0, padx=0, pady=0)

        self.button_download = tk.Button(self.head_section, text='下载任务', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color2,
                                bd=-1, height=25, width=253, image=self.Img, command=lambda: print('21'))
        self.button_upload = tk.Button(self.head_section, text='上传任务', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color2,
                                bd=-1, height=25, width=253, image=self.Img,
                                command = lambda: func_ui.showinfo('oh no', '暂未开放'))
        self.button_history = tk.Button(self.head_section, text='下载历史', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color2,
                                bd=-1, height=25, width=253, image=self.Img,
                                command = lambda: func_ui.showinfo('oh no', '暂未开放'))
        self.button_download.grid(row=0, column=0, padx=5, pady=0)
        self.button_upload.grid(row=0, column=1, padx=5, pady=0)
        self.button_history.grid(row=0, column=2, padx=5, pady=0)
        pass
    
    def change_page(self, page, size_page=False):
        for i in DownPage.page_list:
            i.grid_forget()
        if size_page:
            size_page.grid_propagate(False)
            size_page.config(height=423, width=800)
            size_page.grid(row=1, column=0, padx=0, pady=0)
        page.grid_propagate(False)
        page.config(height=443, width=800)
        page.grid(row=1, column=0, padx=0, pady=0)

    def bind_command(self, abutton, page, size_page=False):
        abutton['command'] = lambda: self.change_page(page, size_page)

    def gen_down_page(self):
        self.down_page = tk.Frame(self.main_frame, bg=Total_Seeting.Color1, bd=-2)
        self.total_func_frame = tk.Frame(self.down_page, bg=Total_Seeting.Color1, bd=-2, height=20, width=800)
        self.total_func_frame.grid_propagate(False)
        self.tf_start = tk.Button(self.total_func_frame, text='全部开始', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg='green',
                                bd=-1, height=20, width=100, image=self.Img,
                                command = lambda: CORE_download.start_all())
        self.tf_start.grid(row=0, column=0, padx=5)

        self.tf_start = tk.Button(self.total_func_frame, text='全部暂停', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg='orange',
                                bd=-1, height=20, width=100, image=self.Img,
                                command = lambda: CORE_download.pause_all())
        self.tf_start.grid(row=0, column=1, padx=5)

        self.tf_start = tk.Button(self.total_func_frame, text='全部取消', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg='red',
                                bd=-1, height=20, width=100, image=self.Img,
                                command = lambda: CORE_download.delete_all())
        self.tf_start.grid(row=0, column=2, padx=5)

        self.tf_start = tk.Button(self.total_func_frame, text='打开文件夹', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.ColorSpecial,
                                bd=-1, height=20, width=100, image=self.Img,
                                command = lambda: func_other.open_download_dir())
        self.tf_start.grid(row=0, column=3, padx=5)
        self.total_func_frame.grid(row=0, column=0)
        self.down_page.grid(row=1, column=0, padx=0, pady=0)
        self.TopFrame = tk.Frame(self.down_page, bg=Total_Seeting.Color0, bd=-2)
        DownPage.page_list.append(self.TopFrame)
        self.TopFrame.grid_rowconfigure(0, weight=1)
        self.TopFrame.grid_columnconfigure(0, weight=1)
        self.TopFrame.grid_propagate(False)

        self.Canves = tk.Canvas(self.TopFrame, bg=Total_Seeting.Color1, bd=-2)
        self.Canves.grid(row=0, column=0, sticky="news")
        #   orient:适配 vertical horizontal
        self.sidebar = tk.Scrollbar(self.TopFrame, command=self.Canves.yview,
                                    orient='vertical', bd=-2)
        self.Canves.config(yscrollcommand=self.sidebar.set)
        self.ImgFrame = tk.Frame(self.Canves, bg=Total_Seeting.Color1, bd=-2)
        self.ImgFrame.bind("<Enter>", lambda event: 
                            self.Canves.bind_all("<MouseWheel>", self.mouse_wheel))
        self.ImgFrame.grid(row=0, column=0, padx=0, pady=0)
        self.sidebar.grid(row=0, column=1,sticky='ns')
        self.Canves.create_window((0, 0), window=self.ImgFrame, anchor='nw')
        self.Canves.bind_all("<MouseWheel>", self.mouse_wheel)
        self.ImgFrame.update_idletasks()
        self.TopFrame.config(height=423, width=800)
        self.Canves.config(scrollregion=self.Canves.bbox("all"))
        self.TopFrame.grid(row=1, column=0, padx=0, pady=0)
        return self.down_page, self.TopFrame
    
    def mouse_wheel(self, event):
        self.Canves.yview_scroll(int(-1*(event.delta/120)), "units")

    def thread_deltsk(self, command):
        Tthr = threading.Thread(target=command)
        Tthr.start()

    def thread_pausetsk(self, command, t1, t2):
        Tthr = threading.Thread(target=command, args=(t1, t2))
        Tthr.start()

    def flash_down_page(self):
        self.controlList = []
        self.takeplace = tk.Label(self.ImgFrame, image=self.Img, bg=Total_Seeting.Color1, width=780)
        self.takeplace.grid(row=2048, column=0, padx=0, pady=0)
        while True:
            time.sleep(0.3)
            self.count = 1
            if len(CORE_download.get_all()) < len(self.controlList):
                for i in range(len(self.controlList) - len(CORE_download.get_all())):
                    self.controlList[-1]['Frame'].destroy()
                    self.controlList.remove(self.controlList[-1])
            for DownSatus in CORE_download.get_all():
                name = DownSatus['Name']
                progress = DownSatus['Percent']
                status = {
                    'Ready': '就绪',
                    'Deleted': '已删除',
                    'Pause': '已暂停',
                    'Download': '正在下载',
                    'Done': '下载完成',
                    'Pauseing': '正在暂停',
                    'Deleting': '正在删除',
                    'Starting': '正在启动',
                }
                if DownSatus['Satus'] == 'Done':
                    continue
                status = status.get(DownSatus['Satus'], '无法识别' + str(DownSatus['Satus']))
                download = DownSatus['download']
                total = DownSatus['total']
                speed = DownSatus['speed']
                inf_text=(name + '\n状态:' + status + '\t总大小:' + total + '\t已下载:' + download + 
                            '\t速度:' + str(speed) + '\t进度:' + progress)

                progress_width=DownSatus['Progress'] * 760
                ext = DownSatus['ext']
                if self.count <= len(self.controlList) and self.controlList != []:
                    
                    if DownSatus['Pause']:
                        text='▷'
                    else:
                        text='||'
                    #从已有的列表中取出控件
                    DownTSK_Inf = self.controlList[self.count - 1]['InfLabel']
                    DownTSK_Img = self.controlList[self.count - 1]['ImgLabel']
                    progressBar = self.controlList[self.count - 1]['progressBar']
                    BTpause = self.controlList[self.count - 1]['BTpause']
                    BTdel = self.controlList[self.count - 1]['BTdel']
                    #重置内容
                    BTdel['command'] = lambda t=DownSatus['Self']: self.thread_deltsk(t.delete_task)
                    BTpause['text'] = text
                    BTpause['command'] = (lambda t1=BTpause, t2=DownSatus['Self']: 
                                        self.thread_pausetsk(func_other.change_pause_shart, t1, t2))
                    DownTSK_Img['image'] = func_other.select_ext(Total_Seeting.FileImgList, ext)['50px']
                    DownTSK_Inf['text'] = inf_text
                    progressBar['width'] = progress_width
                    #更新控件
                    if DownSatus['Satus'] == 'Done':
                        BTdel.grid_forget()
                        BTpause.grid_forget()
                    else:
                        BTpause.grid(row=0, column=2, padx=0, pady=0)
                        BTdel.grid(row=0, column=3, padx=5, pady=0)
                        BTdel.update()
                        BTpause.update()
                    DownTSK_Img.update()
                    DownTSK_Inf.update()
                    progressBar.update()
                    
                    self.count += 1
                else:
                    if DownSatus['Pause']:
                        text='▷'
                    else:
                        text='||'
                    #外层frame
                    self.OutsideDownTSK = tk.Frame(self.ImgFrame,
                                                bg=Total_Seeting.Color0, bd=-2)
                    self.inf_and_func_frame = tk.Frame(self.OutsideDownTSK,
                                                    bg=Total_Seeting.Color0, bd=-2)
                    #图片
                    self.FileIcon = tk.Label(self.inf_and_func_frame, bg=Total_Seeting.Color0, bd=-2,
                                            image=func_other.select_ext(Total_Seeting.FileImgList, ext)['50px'],
                                            height=50, width=50)
                    self.DownTSK_Inf = tk.Label(self.inf_and_func_frame, bg=Total_Seeting.Color0, bd=-2,
                                                fg=Total_Seeting.Fcolor, text=inf_text, image=self.Img,
                                                compound='center', height=40, width=610)
                    
                    self.PauseButton = tk.Button(self.inf_and_func_frame, text=text, bg=Total_Seeting.Color0,
                                                fg=Total_Seeting.Fcolor, compound='center', relief='flat', 
                                                bd=-1, height=40, width=40, image=self.Img)
                    self.PauseButton['command'] = (lambda t1 = self.PauseButton, t2=DownSatus['Self']: 
                                                    self.thread_pausetsk(func_other.change_pause_shart, t1, t2))
                    self.DeleteButton = tk.Button(self.inf_and_func_frame, text='×', bg=Total_Seeting.Color0,
                                                command = lambda t = DownSatus['Self']: self.thread_deltsk(t.delete_task),
                                                bd=-1, height=40, width=40, image=self.Img, relief='flat',
                                                fg=Total_Seeting.Fcolor, compound='center')
                    self.progressBar = tk.Label(self.OutsideDownTSK, bg=Total_Seeting.Color2,
                                                image=self.Img, width=progress_width,
                                                height=2, compound='top', text=' ')
                    
                    self.inf_and_func_frame.grid(row=0, column=0, padx=0, pady=0, sticky='w')
                    self.FileIcon.grid(row=0, column=0, padx=0, pady=0, sticky='w')
                    self.DownTSK_Inf.grid(row=0, column=1, padx=0, pady=0, sticky='w')
                    if DownSatus['Satus'] != 'Done':
                        self.PauseButton.grid(row=0, column=2, padx=0, pady=0, sticky='w')
                        self.DeleteButton.grid(row=0, column=3, padx=5, pady=0, sticky='w')
                    self.OutsideDownTSK.grid(row=self.count, column=0, padx=0, pady=5)
                    self.progressBar.grid(row=1, column=0, padx=0, pady=0, sticky='w')

                    lists = {
                        'Frame': self.OutsideDownTSK,
                        'ImgLabel': self.FileIcon,
                        'InfLabel': self.DownTSK_Inf,
                        'BTpause': self.PauseButton,
                        'BTdel': self.DeleteButton,
                        'progressBar': self.progressBar,
                    }
                    self.controlList.append(lists)
                    self.count += 1
            height_takeplace = 479 - (self.count * 60)
            if height_takeplace < 0:
                height_takeplace = 0
            self.takeplace['height'] = height_takeplace
            self.takeplace.update()
            self.ImgFrame.update_idletasks()
            self.Canves.config(scrollregion=self.Canves.bbox("all"))

#    def gen_basic_part(self):
#        
#
#
#def start(main_frame):
#    page_down = DownPage(main_frame)
#    page_down.gen_basic_part()
#        