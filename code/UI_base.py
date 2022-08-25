#-*- coding:utf-8 -*-
#CREATER: ShenAo

import tkinter as tk
import os
import threading

import Total_Seeting
import func_other
import func_ui
import UI_pages_account
from UI_pages_setting import SettingPage
from UI_pages_down import DownPage

class MainWindow:
    def __init__(self) -> None:
        self.pages_list = []

        self.Name = 'BaiDu NetDisk Download Manager 4'

        #参数
        self.RootSize = '800x547'
        self.logo = './logo.ico'
        
        self.invisble = tk.Tk()
        self.invisble.withdraw()

        self.root = tk.Toplevel()
        self.root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
        self.Img =  tk.PhotoImage(file='./res/show.png')
        self.TopButtonImg =  tk.PhotoImage(file='./res/TopButton.png')
        self.ButtonLongImg = tk.PhotoImage(file='./res/BTlong.png')

        self.ReloadImg = tk.PhotoImage(file='./res/reload.png')
        self.BackImg = tk.PhotoImage(file='./res/back.png')
        self.HomeImg = tk.PhotoImage(file='./res/home.png')
        self.AllSelectImg = tk.PhotoImage(file='./res/allselect.png')
        
        self.TopHomeImg = tk.PhotoImage(file='./res/main_button/TopButton_home.png')
        self.TopUserImg = tk.PhotoImage(file='./res/main_button/TopButton_User.png')
        self.TopDownImg = tk.PhotoImage(file='./res/main_button/TopButton_download.png')
        self.TopMoreImg = tk.PhotoImage(file='./res/main_button/TopButton_more.png')
        self.TopSettingImg = tk.PhotoImage(file='./res/main_button/TopButton_setting.png')
        self.AnalyseImg = tk.PhotoImage(file='./res/main_button/analyse.png')
        
        self.LongFloder = tk.PhotoImage(file='./res/File_Long/floder.png')
        
        self.ImgFile_50px_exe = tk.PhotoImage(file='./res/50px/excProgram.png')
        self.ImgFile_50px_file = tk.PhotoImage(file='./res/50px/file.png')
        self.ImgFile_50px_iso = tk.PhotoImage(file='./res/50px/iso.png')
        self.ImgFile_50px_excel = tk.PhotoImage(file='./res/50px/Office_excel.png')
        self.ImgFile_50px_ppt = tk.PhotoImage(file='./res/50px/Office_powerpoint.png')
        self.ImgFile_50px_word = tk.PhotoImage(file='./res/50px/Office_word.png')
        self.ImgFile_50px_photo = tk.PhotoImage(file='./res/50px/photo.png')
        self.ImgFile_50px_txt = tk.PhotoImage(file='./res/50px/txt.png')
        self.ImgFile_50px_video = tk.PhotoImage(file='./res/50px/video.png')

        
        self.ImgFile_Short_zip = tk.PhotoImage(file='./res/File_Short/File_Zip.png')
        self.ImgFile_Short_excel = tk.PhotoImage(file='./res/File_Short/excel.png')
        self.ImgFile_Short_exe = tk.PhotoImage(file='./res/File_Short/exe.png')
        self.ImgFile_Short_file = tk.PhotoImage(file='./res/File_Short/file.png')
        self.ImgFile_Short_iso = tk.PhotoImage(file='./res/File_Short/iso.png')
        self.ImgFile_Short_music = tk.PhotoImage(file='./res/File_Short/music.png')
        self.ImgFile_Short_photo = tk.PhotoImage(file='./res/File_Short/photo.png')
        self.ImgFile_Short_ppt = tk.PhotoImage(file='./res/File_Short/ppt.png')
        self.ImgFile_Short_txt = tk.PhotoImage(file='./res/File_Short/txt.png')
        self.ImgFile_Short_video = tk.PhotoImage(file='./res/File_Short/video.png')
        self.ImgFile_Short_word = tk.PhotoImage(file='./res/File_Short/word.png')
        
        
        
        Total_Seeting.FileImgList = {
            '50px_exe': self.ImgFile_50px_exe,
            '50px_file': self.ImgFile_50px_file,
            '50px_iso': self.ImgFile_50px_iso,
            '50px_excel': self.ImgFile_50px_excel,
            '50px_ppt': self.ImgFile_50px_ppt,
            '50px_word': self.ImgFile_50px_word,
            '50px_photo': self.ImgFile_50px_photo,
            '50px_txt': self.ImgFile_50px_txt,
            '50px_video': self.ImgFile_50px_video,

            'Short_excel': self.ImgFile_Short_excel,
            'Short_exe': self.ImgFile_Short_exe,
            'Short_file': self.ImgFile_Short_file,
            'Short_iso': self.ImgFile_Short_iso,
            'Short_music': self.ImgFile_Short_music,
            'Short_photo': self.ImgFile_Short_photo,
            'Short_ppt': self.ImgFile_Short_ppt,
            'Short_txt': self.ImgFile_Short_txt,
            'Short_video': self.ImgFile_Short_video,
            'Short_word': self.ImgFile_Short_word,
            'Short_zip': self.ImgFile_Short_zip,
        }
        self.FileListRequireReload = False
        self.AccountBarLen = -1
        self.root.config(bg=Total_Seeting.Color0)
        self.root.geometry(self.RootSize)
        self.root.resizable(0,0)
        self.root.iconbitmap(self.logo)
        self.root.title(self.Name)
        pass
    
    def basic_part(self):
        #staus bar
        self.top_frame = tk.Frame(self.root, bg=Total_Seeting.Color3)
        self.top_frame.grid_propagate(False)
        self.top_frame.config(height=30, width=794)
        #self.top_frame.grid(row=0, column=0, padx=3, pady=3)

        #self.root.overrideredirect(True)

        self.name_label = tk.Label(self.top_frame, bg=Total_Seeting.Color3,
                                    fg=Total_Seeting.Fcolor, text=self.Name,
                                    height=25, font=('Arial', 11, "bold"),
                                    image=self.Img, compound='center', width=692)
        self.name_label.grid(row=0, column=0, padx=0, pady=0)
        self.mini_bt = tk.Button(self.top_frame, text='-',bg=Total_Seeting.Color1,
                                bd=-1, height=17, width=38, image=self.Img,
                                relief ='flat', compound ='center', fg=Total_Seeting.Fcolor,
                                command=lambda: self.minimize(), font=('Arial', 16, "bold"))
        self.mini_bt.grid(row=0, column=1, padx=5, pady=0)
        self.close_bt = tk.Button(self.top_frame, text='×',bg='#b55252',
                                bd=-1, height=17, width=38, image=self.Img,
                                relief ='flat', compound ='center', fg=Total_Seeting.Fcolor,
                                command=lambda: os._exit(0), font=('Arial', 16, "bold"))
        self.close_bt.grid(row=0, column=2, padx=0, pady=0)
        self.name_label.bind("<Map>",self.frame_mapped)
        staus_list=[self.top_frame, self.name_label]
        for sg in staus_list:
            sg.bind("<ButtonPress-1>", self.start_move)
            sg.bind("<ButtonRelease-1>", self.stop_move)
            sg.bind("<B1-Motion>", self.do_move)
        #top bar
        self.TopFunctionBar = tk.Frame(self.root, bg=Total_Seeting.Color0)
        self.TopFunctionBar.grid(row=1, column=0, padx=0, pady=0)
        self.MainPage = tk.Button(self.TopFunctionBar, text=Total_Seeting.lg_mainpage,bg=Total_Seeting.Color1,
                                bd=-1, height=30, width=150, image=self.TopHomeImg,
                                relief ='flat', compound ='center', fg=Total_Seeting.Fcolor,
                                font=('Arial', 11, "bold"))
        self.MyAccount = tk.Button(self.TopFunctionBar, text=Total_Seeting.lg_myaccount,bg=Total_Seeting.Color1,
                                    fg=Total_Seeting.Fcolor, compound='center',bd=-1, height=30,
                                    width=150, image=self.TopUserImg, relief='flat', 
                                    font=('Arial', 11, "bold"))
        self.Download = tk.Button(self.TopFunctionBar, text=Total_Seeting.lg_downtask,bg=Total_Seeting.Color1,
                                fg=Total_Seeting.Fcolor, compound='center', bd=-1, height=30,
                                width=150, image=self.TopDownImg, relief='flat', 
                                font=('Arial', 11, "bold"))
        self.More = tk.Button(self.TopFunctionBar, text=Total_Seeting.lg_more, bg=Total_Seeting.Color1,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=30, width=150, image=self.TopMoreImg,
                                font=('Arial', 11, "bold"))
        self.Setting = tk.Button(self.TopFunctionBar, text=Total_Seeting.lg_setting, bg=Total_Seeting.Color1,
                                fg=Total_Seeting.Fcolor, compound='center', font=('Arial', 11, "bold"),
                                bd=-1, height=30, width=150, image=self.TopSettingImg,
                                relief='flat')
        control_list = [self.MainPage, self.MyAccount, self.Download, self.More, self.Setting]
        for control in control_list:
            control.bind("<Enter>", lambda event, t=control: 
                        func_other.colorChange(t, Total_Seeting.Color1_Hold))
            control.bind("<Leave>", lambda event, t=control: 
                        func_other.colorChange(t, Total_Seeting.Color1))
        #按钮摆放
        self.MainPage.grid(row=0, column=0, padx=3, pady=3)
        self.MyAccount.grid(row=0, column=1, padx=3, pady=3)
        self.Download.grid(row=0, column=2, padx=3, pady=3)
        self.More.grid(row=0, column=3, padx=3, pady=3)
        self.Setting.grid(row=0, column=4, padx=3, pady=3)
        #main frame
        self.main_frame = tk.Frame(self.root, bg=Total_Seeting.Color0)
        self.main_frame.grid_propagate(False)
        self.main_frame.config(height=465, width=800)
        self.main_frame.grid(row=2, column=0, padx=0, pady=0)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def frame_mapped(self, e):
        return False
        self.root.update_idletasks()
        self.root.overrideredirect(True)
        self.root.state('normal')

    def minimize(self):
        return False
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state('iconic')

    def bind_change_page_command(self, part: tk.Button, page: tk.Frame):
        self.pages_list.append(page)
        part['command'] = lambda: self.change_page(page)
        part.update()
        return True

    def change_page(self, page):
        for part in self.pages_list:
            part.grid_forget()
        page.grid(row=0, column=0, padx=0, pady=0)
        return True

    def run(self):
        self.invisble.mainloop()


class ChildFrame:
    def __init__(self, main_wind: MainWindow) -> None:
        self.mian_frame = main_wind.main_frame
        self.pblc_res = main_wind
        self.warnImg = tk.PhotoImage(file='./res/warning.png')
        self.noticeImg = tk.PhotoImage(file='./res/notice.png')
        self.clockImg = tk.PhotoImage(file='./res/clock.png')
        pass

    def gen_main(self):
        """
        生成主页frame
        """
        self.main = tk.Frame(self.mian_frame, bg=Total_Seeting.Color0)
        self.main.grid_propagate(False)
        self.main.config(height=465, width=800)
        self.main.grid(row=0, column=0, padx=0, pady=0)
        self.bg=tk.Label(self.main, image=self.pblc_res.Img, bd=0, height=465, 
                            width=800, bg=Total_Seeting.Color0)
        self.bg.grid_propagate(False)
        self.bg.place(x=0, y=0)

        #self.clock_label.place(x=10, y=10)

        self.warn_label = tk.Label(self.main, text=Total_Seeting.lg_thispgstilltest,
                                    fg=Total_Seeting.Fcolor, compound='left', bg='orange',
                                    bd=-1, height=60, width=400, image=self.warnImg,
                                    relief='flat', anchor='w')
        self.warn_label.place(x=10, y=380)
        self.help_label = tk.Label(self.main, text=Total_Seeting.lg_gainhelp,
                                    fg=Total_Seeting.Fcolor, compound='left', bg='green',
                                    bd=-1, height=60, width=400, image=self.noticeImg,
                                    relief='flat', anchor='w')
        #self.help_label.place(x=10, y=380)
        return self.main

    def gen_account(self):
        """
        生成账号+分享链接所需的frame
        """
        #basic frame
        self.main = tk.Frame(self.mian_frame, bg=Total_Seeting.Color0)
        self.main.grid_propagate(False)
        self.main.config(height=465, width=800)
        self.main.grid(row=0, column=0, padx=0, pady=0)
        #select frame
        """生成账号界面顶部的账号栏"""
        self.TopBarFrame = tk.Frame(self.main, bg=Total_Seeting.Color0, bd=-2)
        self.TopBarFrame.grid_rowconfigure(0, weight=1)
        self.TopBarFrame.grid_columnconfigure(0, weight=1)
        self.TopBarFrame.grid_propagate(False)

        self.BarCanves = tk.Canvas(self.TopBarFrame, bg=Total_Seeting.Color0, bd=-2)
        self.BarCanves.grid(row=0, column=0, sticky="news")
        #   orient:适配 vertical horizontal
        self.sidebar = tk.Scrollbar(self.TopBarFrame, command=self.BarCanves.xview,
                                    orient='horizontal', bd=-2)
        self.BarCanves.config(xscrollcommand=self.sidebar.set)
        self.BarFrame = tk.Frame(self.BarCanves, bg=Total_Seeting.Color0, bd=-2)
        self.BarFrame.grid(row=0, column=0, padx=0, pady=0)

        self.sidebar.grid(row=1, column=0,sticky='ew')

        self.BarCanves.create_window((0, 0), window=self.BarFrame, anchor='nw')
        self.BarFrame.update_idletasks()

        self.TopBarFrame.config(height=40, width=800)
        self.BarCanves.config(scrollregion=self.BarCanves.bbox("all"))
        self.TopBarFrame.grid(row=0, column=0, padx=0, pady=0)
        #part frame
        self.part_main = tk.Frame(self.main, bg=Total_Seeting.Color0)
        self.part_main.grid_propagate(False)
        self.part_main.config(height=425, width=800)
        self.part_main.grid(row=1, column=0, padx=0, pady=0)
        return self.main

    def gen_more(self):
        #basic frame
        self.main = tk.Frame(self.mian_frame, bg=Total_Seeting.Color0)
        self.main.grid_propagate(False)
        self.main.config(height=463, width=800)
        self.name_label = tk.Label(self.main, bg=Total_Seeting.Color0,
                                    fg=Total_Seeting.Fcolor, text='啥也没有',
                                    height=2, font=('Arial', 11, "bold"),
                                    compound='center', width=90)
        self.name_label.grid(row=0, column=0, padx=0, pady=0)
        self.main.grid(row=0, column=0, padx=0, pady=0)

        return self.main

    def gen_download(self):
        #basic frame
        self.main = tk.Frame(self.mian_frame, bg=Total_Seeting.Color0)
        self.main.grid_propagate(False)
        self.main.config(height=463, width=800)
        self.main.grid(row=0, column=0, padx=0, pady=0)

        return self.main
    
    def gen_setting(self):
        #basic frame
        self.main = tk.Frame(self.mian_frame, bg=Total_Seeting.Color0)
        self.main.grid_propagate(False)
        self.main.config(height=463, width=800)
        self.main.grid(row=0, column=0, padx=0, pady=0)

        return self.main

def agree_policy():
    if os.path.exists('./data/policy.dat'):
        return True
    root = tk.Tk()
    root.config(bg=Total_Seeting.Color0)
    #root.geometry('400x270')
    #root.resizable(0,0)
    root.iconbitmap('./logo.ico')
    root.title('Policy')
    ploicy1 = tk.Button(root, text='《》',bg=Total_Seeting.Color1,
                                bd=-1, height=2, width=30, command=lambda: func_other.open_url(),
                                relief ='flat', compound ='center', fg=Total_Seeting.Fcolor,
                                font=('Arial', 11, "bold"))


    
Tlogin = threading.Thread(target=func_other.check_for_update)
Tlogin.start()
#generate main window, init basic frame
wind = MainWindow()
wind.basic_part()
pages = ChildFrame(wind)
main_page = pages.gen_main()
wind.bind_change_page_command(wind.MainPage, main_page)
wind.bind_change_page_command(wind.MyAccount, pages.gen_account())
wind.bind_change_page_command(wind.More, pages.gen_more())
down_frame = pages.gen_download()
wind.bind_change_page_command(wind.Download, down_frame)
#login
Tlogin = threading.Thread(target=UI_pages_account.login, args=(pages.BarFrame, pages.BarCanves, pages.part_main,
                                                                wind.root, Total_Seeting.FileImgList))
Tlogin.start()
#download page
page_down = DownPage(down_frame)
down_page, content_page = page_down.gen_down_page()
page_down.bind_command(page_down.button_download, down_page, content_page)
Tdownpage = threading.Thread(target=page_down.flash_down_page)
Tdownpage.start()
#seeting page
setting_frame = pages.gen_setting()
page_setting = SettingPage(setting_frame)
common_page = page_setting.common()
downengine_page = page_setting.download_engine()
about_page = page_setting.about_page()
page_setting.bind_new(common_page, Total_Seeting.lg_normalsetting)
page_setting.bind_new(downengine_page, Total_Seeting.lg_downenineselection)
page_setting.bind_new(about_page, '关于')
page_setting.change(common_page)
wind.bind_change_page_command(wind.Setting, setting_frame)
wind.change_page(main_page)
#task part
func_ui.main_frame = wind.root
func_ui.initialization()
Ttask = threading.Thread(target=func_ui.refresh)
Ttask.start()
#start aria2c
func_other.start_aria2c()
#func_ui.add_task('ok', 'none', 1)
wind.run()