#-*- coding:utf-8 -*-
#CREATER: ShenAo
import tkinter as tk
import base64

import Total_Seeting
import func_other
from func_ui import Selecter
from func_ui import Insert

class SettingPage:
    page_list = []
    def __init__(self, main_frame: tk.Frame) -> None:
        self.count = 0
        self.main_frame = main_frame
        self.Img = tk.PhotoImage(file='./res/show.png')
        self.left_bar = tk.Frame(self.main_frame, bg=Total_Seeting.Color1)
        self.left_bar.grid_propagate(False)
        self.left_bar.config(height=463, width=200)
        self.left_bar.grid(row=0, column=0, padx=0, pady=0)

        self.right_main = tk.Frame(self.main_frame, bg=Total_Seeting.Color0)
        
        self.right_main.grid(row=0, column=1, padx=0, pady=0)

        self.right_main.grid_rowconfigure(0, weight=1)
        self.right_main.grid_columnconfigure(0, weight=1)
        self.right_main.grid_propagate(False)

        self.Canves = tk.Canvas(self.right_main, bg=Total_Seeting.Color0, bd=-2)
        self.Canves.grid(row=0, column=0, sticky="news")
        #   orient:适配 vertical horizontal
        self.sidebar = tk.Scrollbar(self.right_main, command=self.Canves.yview,
                                    orient='vertical', bd=-2)
        self.Canves.config(yscrollcommand=self.sidebar.set)
        self.ImgFrame = tk.Frame(self.Canves, bg=Total_Seeting.Color0, bd=-2)
        self.ImgFrame.bind("<Enter>", lambda event: 
                            self.Canves.bind_all("<MouseWheel>", self.mouse_wheel))
        self.ImgFrame.grid(row=0, column=0, padx=0, pady=0)
        self.sidebar.grid(row=0, column=1,sticky='ns')
        self.Canves.create_window((0, 0), window=self.ImgFrame, anchor='nw')
        self.Canves.bind_all("<MouseWheel>", self.mouse_wheel)
        self.ImgFrame.update_idletasks()
        self.Canves.config(scrollregion=self.Canves.bbox("all"))
        self.right_main.grid(row=0, column=1, padx=0, pady=0)
        self.right_main.config(height=463, width=600)
        pass
    
    def common(self):
        self.main = tk.Frame(self.ImgFrame, bg=Total_Seeting.Color0)
        self.main.grid(row=0, column=0, padx=0, pady=0)
        labelINF = tk.Label(self.main, text='■ 下载路径', anchor="nw", compound='center', 
                            image=self.Img, relief='flat', width=565, height=20, bg=Total_Seeting.Color0,
                            fg='white').grid(row=0, column=0, padx=5)
        self.set_path_label = tk.Label(self.main, text=Total_Seeting.Path, anchor="nw", compound='left', 
                            image=self.Img, relief='flat', width=565, height=22, bg=Total_Seeting.Color3,
                            fg='white')
        self.set_path_label.grid(row=1, column=0, padx=5, pady=5)
        self.set_path_bt = tk.Button(self.main, text='浏览', bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    command = lambda: func_other.change_setting_downpath(self.set_path_label),
                                    bd=-1, height=25, width=565, image=self.Img)
        self.set_path_bt.grid(row=2, column=0, padx=5, pady=5)



        labelINF = tk.Label(self.main, text='', anchor="nw", compound='center', 
                            image=self.Img, relief='flat', width=565, height=20, bg=Total_Seeting.Color0,
                            fg='white').grid(row=3, column=0, padx=5)
        self.set_test_bt = tk.Button(self.main, text='测试网络', bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    command = lambda: func_other.network_test(),
                                    bd=-1, height=25, width=565, image=self.Img)
        self.set_test_bt.grid(row=4, column=0, padx=5, pady=5)
        self.set_reset_bt = tk.Button(self.main, text='恢复出厂设置', bg='red',
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    command = lambda: func_other.reset_all(),
                                    bd=-1, height=25, width=565, image=self.Img)
        self.set_reset_bt.grid(row=5, column=0, padx=5, pady=5)
        return self.main

    def download_engine(self):
        self.main = tk.Frame(self.ImgFrame, bg=Total_Seeting.Color0)
        self.main.grid(row=0, column=0, padx=0, pady=0)
        self.engine_selector = Selecter('请选择下载引擎', self.main, 565)
        tablet_enging = {
            'local': '内置',
            'IDM': 'IDM',
            'aria2c': 'Aria2c',
            'local_mulit': '多线程',
        }
        text_list = ['内置', '多线程', 'IDM', 'Aria2c']
        command_list = [
            lambda: func_other.change_down_engine('local'),
            lambda: func_other.change_down_engine('local_mulit'),
            lambda: func_other.change_down_engine('IDM'),
            lambda: func_other.change_down_engine('aria2c'),

        ]
        self.engine_selector.add_selection(text_list, command_list)
        self.engine_selector.select(tablet_enging.get(Total_Seeting.down_method))
        self.engine_selector.get().grid(row=0, column=0, padx=0, pady=10)

        self.thread_selector = Selecter('请选择下载线程数 - 在IDM下无效', self.main, 565)
        text_list = ['1', '2', '4', '8', '16', '32', '64']
        command_list = [
            lambda: func_other.change_down_thread(1),
            lambda: func_other.change_down_thread(2),
            lambda: func_other.change_down_thread(4),
            lambda: func_other.change_down_thread(8),
            lambda: func_other.change_down_thread(16),
            lambda: func_other.change_down_thread(32),
            lambda: func_other.change_down_thread(64),
        ]
        self.thread_selector.add_selection(text_list, command_list)
        self.thread_selector.select(str(Total_Seeting.down_thread))
        result = self.thread_selector.get().grid(row=1, column=0, padx=0, pady=10)

        self.RPCurl = Insert('Aria2c RPC地址', self.main, 565)
        self.RPCurl.add_insert(Total_Seeting.aria_RPC, func_other.save_PRC)
        self.RPCurl.get().grid(row=2, column=0, padx=0, pady=10)

        self.aria2c_selector = Selecter('Aria2C随软件启动', self.main, 565)
        text_list = ['不启动', '启动']
        command_list = [
            lambda: func_other.change_aria_start(False),
            lambda: func_other.change_aria_start(True),
        ]
        self.aria2c_selector.add_selection(text_list, command_list)
        if Total_Seeting.aria_start_with:
            self.aria2c_selector.select('启动')
        else:
            self.aria2c_selector.select('不启动')
        result = self.aria2c_selector.get().grid(row=3, column=0, padx=0, pady=5)

        labelINF = tk.Label(self.main, text='  ■ IDM程序路径', anchor="nw", compound='center', 
                            image=self.Img, relief='flat', width=565, height=20, bg=Total_Seeting.Color0,
                            fg='white').grid(row=4, column=0, padx=5)
        self.set_idmpath_label = tk.Label(self.main, text=Total_Seeting.idm_path, anchor="nw", compound='left', 
                            image=self.Img, relief='flat', width=545, height=22, bg=Total_Seeting.Color3,
                            fg='white')
        self.set_idmpath_label.grid(row=5, column=0, padx=5, pady=5)
        self.set_idmpath_bt = tk.Button(self.main, text='浏览', bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    command = lambda: func_other.change_setting_idmpath(self.set_path_label),
                                    bd=-1, height=25, width=545, image=self.Img)
        self.set_idmpath_bt.grid(row=6, column=0, padx=5, pady=5)
        return self.main

    def flash_link(self):
        self.main = tk.Frame(self.ImgFrame, bg=Total_Seeting.Color0)
        self.main.grid(row=0, column=0, padx=0, pady=0)
        self.RPCurl = Insert('加速链接地址', self.main, 565)
        self.RPCurl.add_insert(Total_Seeting.aria_RPC, func_other.save_PRC)
        self.RPCurl.get().grid(row=1, column=0, padx=0, pady=10)
        self.RPCurl = Insert('密码 (可选)', self.main, 565)
        self.RPCurl.add_insert(Total_Seeting.aria_RPC, func_other.save_PRC)
        self.RPCurl.get().grid(row=2, column=0, padx=0, pady=10)
        self.RPCurl = Insert('Token (可选)', self.main, 565)
        self.RPCurl.add_insert(Total_Seeting.aria_RPC, func_other.save_PRC)
        self.RPCurl.get().grid(row=3, column=0, padx=0, pady=10)
        labelINF = tk.Label(self.main, text='■ 什么是加速链接', anchor="w", compound='center', 
                            image=self.Img, relief='flat', height=20, width=363, bg=Total_Seeting.Color0,
                            fg='white').grid(row=4, column=0, padx=5)
        labelINF = tk.Label(self.main, text=Total_Seeting.version_rev + '|' + str(Total_Seeting.ver_num), anchor="w",
                            image=self.Img, relief='flat', width=363, height=20, bg=Total_Seeting.Color1,
                            compound='center', fg='white').grid(row=5, column=0, padx=5)
        return self.main

    def about_page(self):
        self.main = tk.Frame(self.ImgFrame, bg=Total_Seeting.Color0)
        self.main.grid(row=0, column=0, padx=0, pady=0)
        self.left_content = tk.Frame(self.main, bg=Total_Seeting.Color0)
        self.left_content.grid(row=0, column=0, padx=0, pady=0)
        self.Headphoto = tk.PhotoImage(data=bytes(base64.b64decode(Total_Seeting.headphoto, '-_')))
        self.headphoto_img = tk.Label(self.left_content, anchor="w", compound='center', width=200,
                            image=self.Headphoto, relief='flat', bg=Total_Seeting.Color0, fg='white')
        self.headphoto_img.grid(row=0, column=0, padx=0, pady=0)
        self.donate = tk.Button(self.left_content, text='赞助我', bg='gold',
                                    fg='black', compound='center', relief='flat',
                                    command = lambda: func_other.open_url('https://afdian.net/@BDNDM4'),
                                    bd=-1, height=25, width=195, image=self.Img)
        self.donate.grid(row=1, column=0, padx=0, pady=5)
        self.donate = tk.Button(self.left_content, text='加入TG频道', bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    command = lambda: func_other.open_url('https://t.me/BDNDM2022'),
                                    bd=-1, height=25, width=195, image=self.Img)
        self.donate.grid(row=2, column=0, padx=0, pady=5)
        #right
        self.content = tk.Frame(self.main, bg=Total_Seeting.Color0)
        self.content.grid(row=0, column=1, padx=0, pady=0)
        labelINF = tk.Label(self.content, text='■ 程序版本', anchor="w", compound='center', 
                            image=self.Img, relief='flat', height=20, width=363, bg=Total_Seeting.Color0,
                            fg='white').grid(row=0, column=0, padx=5)
        labelINF = tk.Label(self.content, text=Total_Seeting.version_rev + '|' + str(Total_Seeting.ver_num), anchor="w",
                            image=self.Img, relief='flat', width=363, height=20, bg=Total_Seeting.Color1,
                            compound='center', fg='white').grid(row=1, column=0, padx=5)
        labelINF = tk.Label(self.content, text='■ 更新日志', anchor="w", compound='left', 
                            image=self.Img, relief='flat', height=20, width=363, bg=Total_Seeting.Color0,
                            fg='white').grid(row=2, column=0, padx=5)
        labelINF = tk.Label(self.content, text=Total_Seeting.Update_text, anchor="w", justify='left',
                            image=self.Img, relief='flat', width=363, bg=Total_Seeting.Color1,
                            compound='center', fg='white').grid(row=3, column=0, padx=5)
        labelINF = tk.Label(self.content, text='■ 联系我', anchor="w", compound='left', 
                            image=self.Img, relief='flat', height=20, width=363, bg=Total_Seeting.Color0,
                            fg='white').grid(row=4, column=0, padx=5)
        labelINF = tk.Label(self.content, text='ntgtech20060605@gmail.com', anchor="w", justify='left',
                            image=self.Img, relief='flat', width=363, bg=Total_Seeting.Color1,
                            compound='center', fg='white').grid(row=5, column=0, padx=5)
        labelINF = tk.Label(self.content, text='Power by NTG 2022', anchor="w", compound='center', 
                            image=self.Img, relief='flat', height=20, width=363, bg=Total_Seeting.Color0,
                            fg='gray').grid(row=6, column=0, padx=5)
        return self.main

    def change(self, page: tk.Frame):
        for i in self.page_list:
            i.grid_forget()
        page.grid(row=0, column=0)
        self.ImgFrame.update_idletasks()
        self.Canves.config(scrollregion=self.Canves.bbox("all"))
    
    def bind_new(self, page: tk.Frame, text):
        self.count += 1
        self.page_list.append(page)
        self.set_reset_bt = tk.Button(self.left_bar, text=text, bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    command = lambda: self.change(page),
                                    bd=-1, height=30, width=185, image=self.Img)
        self.set_reset_bt.grid(row=self.count, column=0, padx=5, pady=5)

    def mouse_wheel(self, event):
        self.Canves.yview_scroll(int(-1*(event.delta/120)), "units")