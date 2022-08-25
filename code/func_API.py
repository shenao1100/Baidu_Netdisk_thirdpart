#-*- coding:utf-8 -*-
#CREATER: ShenAo

import os
from tkinter import filedialog
import tkinter as tk
import threading
import pyperclip
import random

import func_other
import Total_Seeting
from CORE_GetInfo import BaiDuCloud
import func_ui
class APIgetPath:
    Running_Tasks = {}

    def __init__(self, root: tk.Tk, User: BaiDuCloud, command, **kwarg):
        self.command = command
        self.kwarg = kwarg
        self.User = User
        self.root = root
        #resource
        self.ReloadImg = tk.PhotoImage(file='./res/reload.png')
        self.BackImg = tk.PhotoImage(file='./res/back.png')
        self.HomeImg = tk.PhotoImage(file='./res/home.png')
        self.AllSelectImg = tk.PhotoImage(file='./res/allselect.png')
        self.Img = tk.PhotoImage(file='./res/show.png')
        self.Floder = tk.PhotoImage(file='./res/File_Short/Floder.png')
        #Creat a window
        self.choose = tk.Toplevel(master=self.root, bg=Total_Seeting.Color0)
        self.choose.title('请选择存放到的路径')
        self.choose.iconbitmap('./logo.ico')
        self.choose.resizable(0,0)
        self.choose.geometry('580x410')
        self.choose.protocol("WM_DELETE_WINDOW", lambda: self.choose.destroy())
        self.FileFrame = False
        self.count = 0
        #main
        self.main_frame = tk.Frame(self.choose, bg=Total_Seeting.Color0, bd=-2)
        self.main_frame.config(height=345, width=580)
        self.main_frame.grid_propagate(False)
        self.main_frame.grid(row=1, column=0, padx=0, pady=0)
        #topbar
        self.Topbar_frame = tk.Frame(self.choose, bg=Total_Seeting.Color1, bd=-2)
        self.Topbar_frame.config(height=30, width=580)
        self.Topbar_frame.grid_propagate(False)
        self.Topbar_frame.grid(row=0, column=0, padx=0, pady=0)

        self.back_bt = tk.Button(self.Topbar_frame, text=' ', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color2,
                                bd=-1, height=20, width=20, image=self.BackImg)
        self.back_bt.grid(row=0, column=0, padx=3, pady=3)
        self.path_label = tk.Label(self.Topbar_frame, text='', relief='flat',
                                fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color1_Hold,
                                bd=-1, height=20, width=537, image=self.Img)
        self.path_label.grid(row=0, column=1, padx=3, pady=3)

    def end_win(self, command, **Arg):
        #self.window.clear_all(self.window.show_account)
        self.choose.destroy()
        result = command(**Arg, ToPath=self.User.get_temp_path())
        if result:
            if result['FailOrNot']:
                ntc_id = func_ui.add_task('正在操作', 'percent', 0)
                self.User.gui_refresh(result['result']['data'], result['result']['task_id'], ntc_id)
        #self.showlist_class.ProcessFinishAndBack(command, self.User, 
        #                        self.User.get_temp_path(), **kwarg)

    def show_get(self, path, is_add, Filelist):
        #Basic Frame
        if not is_add:
            if self.FileFrame:
                self.FileFrame.destroy()
            self.FileFrame = tk.Frame(self.main_frame, bg=Total_Seeting.Color0, bd=-2)
            self.FileFrame.grid_rowconfigure(0, weight=1)
            self.FileFrame.grid_columnconfigure(0, weight=1)
            self.FileFrame.grid_propagate(False)
            self.FileCanves = tk.Canvas(self.FileFrame, bg=Total_Seeting.Color0, bd=-2, relief='flat')
            self.FileCanves.grid(row=0, column=0, sticky="news")
            self.Filesidebar = tk.Scrollbar(self.FileFrame, command=self.FileCanves.yview,
                                            orient='vertical', bd=-2)
            self.FileCanves.config(yscrollcommand=self.Filesidebar.set)
            self.packFrame = tk.Frame(self.FileCanves, bg=Total_Seeting.Color0, bd=-2)
        self.path_label['text']=path
        self.path_label.update()
        #reload setting

        if not is_add:
            self.count = 0
        #get items
        if not Filelist:
            Filelist = self.User.get_file_list(path, True)

        temp_file_list = []
        self.temp_count = 0
        if self.count + 50 > len(Filelist['result']['Dir']):
            max_temp_count = len(Filelist['result']['Dir'])
        else:
            max_temp_count = self.count + 50
        for i in Filelist['result']['Dir']:
            self.temp_count += 1
            if self.temp_count > self.count and self.temp_count <= max_temp_count:
                temp_file_list.append(i)
        #pack items
        for i in temp_file_list:
            show_name = i['show_name']
            path_open = i['path']
            Time = i['time']
            self.count += 1
            self.OpenBt = tk.Label(self.packFrame, text=show_name + '   ' + Time,
                                fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.Color0_5,
                                bd=-1, height=35, width=560, image=self.Floder, 
                                relief='flat', anchor='w')
            self.OpenBt.bind("<Button-1>", lambda event, t1=path_open: 
                            self.show_get(t1, False, False))
            self.OpenBt.bind("<Enter>", lambda event, t1=self.OpenBt, t2=Total_Seeting.Color2: 
                            func_other.colorChange(t1, t2))
            self.OpenBt.bind("<Leave>", lambda event, t1=self.OpenBt, t2=Total_Seeting.Color0_5:
                            func_other.colorChange(t1, t2))
            self.OpenBt.grid(row=self.count, column=0, padx=3, pady=3)
        #more_button
        if self.count < len(Filelist['result']['Dir']):
            self.more_button = tk.Label(self.packFrame, text='<加载更多>',
                                    fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=20, width=560, image=self.Img, 
                                    relief='flat')
            self.more_button.bind("<Button-1>", lambda event, t1=path, t2=Filelist: 
                            self.show_get(t1, True, t2))
            self.more_button.bind("<Enter>", lambda event, t1=self.more_button, t2=Total_Seeting.Color2: 
                            func_other.colorChange(t1, t2))
            self.more_button.bind("<Leave>", lambda event, t1=self.more_button, t2=Total_Seeting.Color0_5:
                                func_other.colorChange(t1, t2))
            self.more_button.grid(row=self.count + 1, column=0, padx=3, pady=3)

        self.packFrame.grid(row=0, column=0, padx=0, pady=0)
        self.Filesidebar.grid(row=0, column=1,sticky='ns')
        self.FileCanves.create_window((-5, -5), window=self.packFrame, anchor='nw')
        self.FileCanves.bind_all("<MouseWheel>", self.mouse_wheel_down)
        self.packFrame.update_idletasks()
        self.FileFrame.config(height=345, width=580)
        self.FileCanves.config(scrollregion=self.FileCanves.bbox("all"))
        self.FileFrame.grid(row=1, column=0, padx=0, pady=0)
        #continue button
        self.continue_bt = tk.Button(self.choose, text='选择这个文件夹 >',
                                command=lambda: self.end_win(self.command, **self.kwarg), relief='flat',
                                fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.Color2,
                                bd=-1, height=20, width=465, image=self.Img, anchor='w')
        self.continue_bt.grid(row=2, column=0, padx=3, pady=3)

        self.packFrame.bind("<Enter>", lambda event: 
                            self.FileCanves.bind_all("<MouseWheel>", self.mouse_wheel_down))

        self.refresh_backbt()

    def refresh_backbt(self):
        if self.User.get_temp_path() != '/':
            path = self.User.get_temp_path()[:(-1 * (len(self.User.get_temp_path().split('/')[-1]) + 1))]
            if path == '':
                path = '/'
            self.back_bt['command'] = lambda: self.show_get(path, False, False)
        self.back_bt.update()

    def mouse_wheel_down(self, event):
        self.FileCanves.yview_scroll(int(-1*(event.delta/120)), "units")


class SelectUser:
    def __init__(self, root, method, data) -> None:
        self.root = root
        self.method = method
        self.data = data
        self.Img = tk.PhotoImage(file='./res/show.png')
        pass
    
    def select_to_save(self, User: BaiDuCloud):
        self.AskNme_select_share.destroy()
        Tdown = threading.Thread(target=self.select_to_save_real, args=(User, ))
        Tdown.start()

    def select_to_save_real(self, User: BaiDuCloud):
        surl = self.data['surl']
        pwd = self.data['pwd']
        datas = self.data['datas']
        start_path = self.data['start_path']
        for i in range(5):
            s_id = User.share_basic_inf(surl, pwd)
            if s_id:
                break
        if not s_id:
            func_ui.showerror('', '获取信息时出错, 请稍后再试')
            return False
        result = APIgetPath(self.root, User, User.share_save_loop_thread, 
                            s_id=s_id, datas=datas, start_path=start_path)
        result.show_get('/', False, False)
        pass

    def select_to_down_real(self, User: BaiDuCloud):
        surl = self.data['surl']
        pwd = self.data['pwd']
        start_len = self.data['path_len']
        for i in range(5):
            s_id = User.share_basic_inf(surl, pwd)
            if not s_id:
                continue
            else:
                break
        if not s_id:
            func_ui.showerror('', '获取失败，请重试')
            return False
        randsk = User.randsk[s_id]
        share_uk = User.share_uk[s_id]
        share_id = User.share_id[s_id]
        sign = User.share_sign[s_id]
        uk = User.uk[s_id]
        logid = User.Logid[s_id]
        timestamp = User.time_stamp[s_id]
        ntc_id = func_ui.add_task('正在下载', 'cycle', -1)
        for sg_fl in self.data['File']:
            md5 = sg_fl['md5']
            fs_id = sg_fl['fs_id']
            path = sg_fl['path'][start_len:]
            func_ui.manage_task(ntc_id, '正在建立下载文件 - ' + path, 'cycle', -1)
            User.get_share_download_link(md5, share_uk, fs_id, sign, logid, share_id, randsk, uk, timestamp, path)
        for sg_dir in self.data['Dir']:
            start_path = sg_dir['path']
            func_ui.manage_task(ntc_id, '正在解析文件夹 - ' + start_path, 'cycle', -1)
            User.get_share_download_link_loop(start_path, False, s_id, start_len)
        func_ui.delete_task(ntc_id)
        return True

    def share_save_real(self, User: BaiDuCloud):
        surl = self.data['surl']
        pwd = self.data['pwd']
        fs_id = self.data['fs_id']
        s_id = User.share_basic_inf(surl, pwd)
        randsk = User.randsk[s_id]
        share_uk = User.share_uk[s_id]
        share_id = User.share_id[s_id]
        logid = User.Logid[s_id]
        result = APIgetPath(self.root, User, User.api_save, 
                            fs_id=fs_id, Randsk=randsk, Share_Id=share_id, 
                            Share_Uk=share_uk, Logid=logid, Surl=surl)
        result.show_get('/', False, False)
        pass

    def share_save(self, User: BaiDuCloud):
        self.AskNme_select_share.destroy()
        Tdown = threading.Thread(target=self.share_save_real, args=(User, ))
        Tdown.start()
    
    def select_to_down(self, User: BaiDuCloud):
        self.AskNme_select_share.destroy()
        Tdown = threading.Thread(target=self.select_to_down_real, args=(User, ))
        Tdown.start()



    def show(self):
        if len(Total_Seeting.User_loop) == 1:
            func_ui.showinfo('', '请先登录账号')
            return True
        if len(Total_Seeting.User_loop) == 1:
            command = {
                'share_to_save': self.share_save,
                'select_to_down': self.select_to_down,
                'select_to_save': self.select_to_save,
            }.get(self.method)
            command(Total_Seeting.User_loop[0])
        self.AskNme_select_share = tk.Toplevel(master=self.root, bg=Total_Seeting.Color0)
        self.AskNme_select_share.title('请选择')
        self.AskNme_select_share.iconbitmap('./logo.ico')
        self.AskNme_select_share.resizable(0,0)
        labelINF = tk.Label(self.AskNme_select_share, text='■ 您要使用哪个用户进行操作？',
                            anchor="nw", compound='left', image=self.Img, relief='flat',
                            width=210, height=20, bg=Total_Seeting.Color0, fg='white'
                            ).grid(row=0, column=0, padx=5)
        count = 1
        for user in Total_Seeting.User_loop:
            command = {
                'share_to_save': self.share_save,
                'select_to_down': self.select_to_down,
                'select_to_save': self.select_to_save,
            }.get(self.method)

            self.Ctne = tk.Button(self.AskNme_select_share, text=user.Name, bg=Total_Seeting.Color2,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                command=lambda t1=user: command(t1), 
                                bd=-1, height=25, width=200, image=self.Img)

            self.Ctne.grid(row=count, column=0, padx=5, pady=5)
            count += 1
        return True
    
class TopLevels:
    def __init__(self, main_window: tk.Tk, User: BaiDuCloud) -> None:
        """
        需要窗口的功能，包括
        重命名
        获取分享链接
        """
        self.main_window = main_window
        self.User = User
        self.Img =  tk.PhotoImage(file='./res/show.png')
        self.ImgFile_paste = tk.PhotoImage(file='./res/paste.png')
        self.AskPwd = False
        self.AskNme_rename = False
        self.AskPwd_eve_link = False
        self.AskNme_cdir = False
        self.Share_save = False
        pass
    

    def multiple_select_share(self, User: BaiDuCloud):
        """多选分享"""
        if User.SelectedList_File == [] and User.SelectedList_Dir == []:
            func_ui.showwarning('警告', '未选择任何文件/文件夹')
            return False
        FileList = []
        nameList = []
        for i in User.SelectedList_Dir:
            FileList.append(i['fs_id'])
            nameList.append(i['server_filename'])
        for i in User.SelectedList_File:
            FileList.append(i['fs_id'])
            nameList.append(i['name'])
        self.AskNme_select_share = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.AskNme_select_share.title('方式')
        self.AskNme_select_share.iconbitmap('./logo.ico')
        self.AskNme_select_share.resizable(0,0)
        labelINF = tk.Label(self.AskNme_select_share, text='■ 请选择一个方式\n您可以选择将所选文件分享为一个链接\n或将所选的每一个文件分享为链接',
                            anchor="nw", compound='left', image=self.Img, relief='flat',
                            width=210, height=60, bg=Total_Seeting.Color0, fg='white'
                            ).grid(row=0, column=0, padx=5)
        self.Ctne = tk.Button(self.AskNme_select_share, text='分享为一个链接', bg=Total_Seeting.Color2,
                            fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                            command=lambda: self.ask_for_pwd(FileList), 
                            bd=-1, height=30, width=200, image=self.Img)
        self.Ctne.grid(row=1, column=0, padx=5, pady=5)
        self.Ctne = tk.Button(self.AskNme_select_share, text='将选中的文件依次获取链接', bg=Total_Seeting.Color2,
                            fg=Total_Seeting.Fcolor, compound='center', command=lambda t1=User, 
                            t2=FileList, t3=nameList: self.eve_one_link_UI(t1, t2, t3), 
                            bd=-1, height=30, width=200, image=self.Img, relief='flat')
        self.Ctne.grid(row=2, column=0, padx=5, pady=5)

    def eve_one_link_UI(self, User, fs_id_List, name_list):
        if self.AskPwd_eve_link:
            self.AskPwd_eve_link.destroy()
        self.AskPwd_eve_link = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.AskPwd_eve_link.title('提取码')
        self.AskPwd_eve_link.iconbitmap('./logo.ico')
        self.AskPwd_eve_link.resizable(0,0)
        labelINF = tk.Label(self.AskPwd_eve_link, text='■ 这些链接的提取码', anchor="nw", compound='left', 
                            image=self.Img, relief='flat', width=200, height=20, bg=Total_Seeting.Color0,
                            fg='white').grid(row=0, column=0, padx=5)
        AskEntry = tk.Entry(self.AskPwd_eve_link)
        AskEntry.insert(0, str(random.randint(1000, 9999)))
        AskEntry.grid(row=1, column=0, padx=5, pady=5)
        self.CopyPWD = tk.Button(self.AskPwd_eve_link, text='获取',bg=Total_Seeting.Color2,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                command=lambda: self.eve_one_link(User, fs_id_List, name_list, AskEntry.get()), 
                                bd=-1, height=30, width=200, image=self.Img)
        self.CopyPWD.grid(row=5, column=0, padx=5, pady=5)
        return True

    def eve_one_link(self, User: BaiDuCloud, fs_id_List, name_list, pwd):
        Tget = threading.Thread(target=self.eve_one_link_thread, args= (User, fs_id_List, name_list, pwd))
        Tget.start()

    def eve_one_link_thread(self, User: BaiDuCloud, fs_id_List, name_list, pwd):
        self.AskPwd_eve_link.destroy()
        self.AskPwd_eve_link = False
        result_str = '================================'
        ntc_id = func_ui.add_task('正在获取链接...', 'cycle', -1)
        for fs_id, name in zip(fs_id_List, name_list):
            result = User.get_share_link(fs_id, pwd)
            func_ui.manage_task(ntc_id, '正在获取链接: ' + name, False, False)
            if result['FailOrNot']:
                result_str += ('\n' + name + '\n链接:https://pan.baidu.com/s/' + result['result'] +
                                '\n提取码:' + pwd + '\n================================')
            else:
                func_ui.showerror('错误', '获取分享链接时出错' + result['ErrorMessage'])
        func_ui.delete_task(ntc_id)
        self.show_copy_message('获取完成', result_str)

    def show_copy_message(self, title, Str):
        window = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        window.title(title)
        window.iconbitmap('./logo.ico')
        window.resizable(0,0)
        labelINF = tk.Label(window, text='■ 请复制', compound='center', image=self.Img,
                            relief='flat', width=350, height=20, bg=Total_Seeting.Color0, fg='white'
                            ).grid(row=0, column=0, padx=5)
        Copy = tk.Button(window, text='全部复制', bg=Total_Seeting.Color2, bd=-1, height=30,
                        fg=Total_Seeting.Fcolor, compound='center', command=lambda t1=Str: 
                        pyperclip.copy(t1), width=500, image=self.Img, relief='flat')
        Copy.grid(row=1, column=0, padx=5, pady=5)
        labelINF = tk.Label(window, text=Str, compound='center', image=self.Img, relief='flat',
                        width=490, bg=Total_Seeting.Color0_5, fg='white').grid(row=2, column=0, padx=5)
        return True

    def multiple_select_rename(self, User: BaiDuCloud):
        if User.SelectedList_File == [] and User.SelectedList_Dir == []:
            func_ui.showwarning('警告', '未选择任何文件/文件夹')
            return False
        if User.SelectedList_File != [] and User.SelectedList_Dir != []:
            func_ui.showwarning('警告', '批量重命名暂不支持文件夹和文件一同选择')
            return False    
        pathList = []
        OriginalFilename = []
        for i in User.SelectedList_Dir:
            pathList.append(i['path'])
            OriginalFilename.append(i['server_filename'])
        for i in User.SelectedList_File:
            pathList.append(i['path'])
            OriginalFilename.append(i['name'])
        self.ask_for_rename_multiple(pathList, OriginalFilename)


    def ask_for_rename_multiple(self, pathList, OriginalFilename):
        """询问多文件重命名时的文件名"""
        if self.AskNme_rename:
            self.AskNme_rename.destroy()
        self.AskNme_rename = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.AskNme_rename.title('文件名')
        self.AskNme_rename.iconbitmap('./logo.ico')
        self.AskNme_rename.resizable(0,0)
        tips_str='■ 请文件名\n可以使用 [origin] 代替文件原本名称(无后缀)\n   [number] 代替序号\n     [ext] 代替后缀名'
        labelINF = tk.Label(self.AskNme_rename, text=tips_str, anchor="nw", compound='left',
                            image=self.Img, relief='flat', width=250, height=80,
                            bg=Total_Seeting.Color0, fg='white').grid(row=0, column=0, padx=5)
        AskEntry = tk.Entry(self.AskNme_rename, width=35)
        self.Ctne = tk.Button(self.AskNme_rename, text='开始重命名',bg=Total_Seeting.Color2,
                            fg=Total_Seeting.Fcolor, compound='center',
                            command=lambda t2=pathList:
                            self.rename_thread(t2, func_other.process_input_rename(OriginalFilename, AskEntry.get())['list']), 
                            bd=-1, height=30, width=250, image=self.Img, relief='flat')
        self.looklike = tk.Button(self.AskNme_rename, text='我的文件名会长啥样？',bg=Total_Seeting.Color2,
                            fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                            command=lambda :func_ui.showinfo('预览',
                            func_other.process_input_rename(OriginalFilename, AskEntry.get())['str']),
                            bd=-1, height=30, width=250, image=self.Img)
        AskEntry.insert(0, '[number][origin][ext]')
        AskEntry.grid(row=1, column=0, padx=5, pady=5)
        self.Ctne.grid(row=2, column=0, padx=5, pady=5)
        self.looklike.grid(row=3, column=0, padx=5, pady=5)
        return True

    def show_downlink(self, link):
        self.Share=tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.Share.title('下载链接')
        self.Share.iconbitmap('./logo.ico')
        self.Share.resizable(0,0)

        labelINF = tk.Label(self.Share, text='■ 链接', anchor="nw", compound='left',
                            image=self.Img, relief='flat', width=500, height=20,
                            bg=Total_Seeting.Color0, fg='white').grid(row=0, column=0, padx=5)
        labelINF = tk.Label(self.Share, text=link, anchor="nw", compound='left', 
                            image=self.Img, relief='flat', width=500, bg=Total_Seeting.Color1,
                            fg='white').grid(row=1, column=0, padx=5)
        self.CopyLNK = tk.Button(self.Share, text='复制链接', bg=Total_Seeting.Color2,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                command=lambda t1=link: pyperclip.copy(t1), 
                                bd=-1, height=30, width=500, image=self.Img)
        self.CopyLNK.grid(row=2, column=0, padx=5, pady=5)

    def show_share_link(self, fs_id, pwd):
        if len(pwd) != 4:
            func_ui.showwarning('警告', '提取码仅能为4位数')
        result = self.User.get_share_link(fs_id, pwd)
        if result['FailOrNot']:
            surl = 'https://pan.baidu.com/s/' + result['result']
        else:
            return False
        """用于显示分享链接和密码
        配备复制按钮"""
        self.Share = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.Share.title('分享链接及提取码')
        self.Share.iconbitmap('./logo.ico')
        self.Share.resizable(0,0)

        labelINF = tk.Label(self.Share, text='■ 分享链接', anchor="nw", compound='left',
                            image=self.Img, relief='flat', width=500, height=20,
                            bg=Total_Seeting.Color0, fg='white').grid(row=0, column=0, padx=5)
        labelINF = tk.Label(self.Share, text=surl, anchor="nw", compound='left', 
                            image=self.Img, relief='flat', width=500, bg=Total_Seeting.Color1,
                            fg='white').grid(row=1, column=0, padx=5)
        self.CopyLNK = tk.Button(self.Share, text='复制链接', bg=Total_Seeting.Color2,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                command=lambda t1=surl: pyperclip.copy(t1), 
                                bd=-1, height=30, width=500, image=self.Img)
        labelINF = tk.Label(self.Share, text='■ 提取码', anchor="nw", compound='left',
                            image=self.Img, relief='flat', width=500, height=20,
                            bg=Total_Seeting.Color0, fg='white').grid(row=3, column=0, padx=5)
        labelINF = tk.Label(self.Share, text=pwd, anchor="nw", compound='left', 
                            image=self.Img, relief='flat', width=500, bg=Total_Seeting.Color1,
                            fg='white').grid(row=4, column=0, padx=5)
        self.CopyPWD = tk.Button(self.Share, text='复制密码', bg=Total_Seeting.Color2,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                command=lambda t1=pwd:pyperclip.copy(t1), 
                                bd=-1, height=30, width=500, image=self.Img)
        self.CopyLNK.grid(row=2, column=0, padx=5, pady=5)
        self.CopyPWD.grid(row=5, column=0, padx=5, pady=5)
        return True

    def get_share_link_thread(self, fs_id, pwd):
        self.AskPwd.destroy()
        self.AskPwd = False
        Tsl = threading.Thread(target=self.show_share_link, args=(fs_id, pwd))
        Tsl.start()

    def ask_for_pwd(self, fs_id):
        if self.AskPwd:
            self.AskPwd.destroy()
        self.AskPwd = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.AskPwd.title('提取码')
        self.AskPwd.iconbitmap('./logo.ico')
        self.AskPwd.resizable(0,0)
        labelINF = tk.Label(self.AskPwd, text='■ 提取码', anchor="nw", compound='left',
                        image=self.Img, relief='flat', width=200, height=20, 
                        bg=Total_Seeting.Color0, fg='white').grid(row=0, column=0, padx=5)
        AskEntry = tk.Entry(self.AskPwd)
        AskEntry.insert(0, str(random.randint(1000, 9999)))
        AskEntry.grid(row=1, column=0, padx=5, pady=5)
        self.CopyPWD = tk.Button(self.AskPwd, text='获取', bg=Total_Seeting.Color2,
                command=lambda t1=self.User, t2=fs_id: self.get_share_link_thread(fs_id, AskEntry.get()), 
                bd=-1, height=30, width=200, image=self.Img, relief='flat', 
                fg=Total_Seeting.Fcolor, compound='center')
        self.CopyPWD.grid(row=5, column=0, padx=5, pady=5)
        return True

    #           rename

    def ask_for_rename(self, User: BaiDuCloud, name, path):
        """单文件重命名"""
        if self.AskNme_rename:
            self.AskNme_rename.destroy()
        self.AskNme_rename = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.AskNme_rename.title('文件名')
        self.AskNme_rename.iconbitmap('./logo.ico')
        self.AskNme_rename.resizable(0,0)
        labelINF = tk.Label(self.AskNme_rename, text='■ 请输入名称', anchor="nw",
                            compound='left', image=self.Img, relief='flat', 
                            width=200, height=20, bg=Total_Seeting.Color0, fg='white'
                            ).grid(row=0, column=0, padx=5)
        AskEntry = tk.Entry(self.AskNme_rename, width=28)
        self.Ctne = tk.Button(self.AskNme_rename, text='重命名',bg=Total_Seeting.Color2,
                fg=Total_Seeting.Fcolor, compound='center', bd=-1, height=30, 
                width=200, image=self.Img, relief='flat',
                command=lambda t3=path: self.rename_thread(t3, AskEntry.get()))
        AskEntry.insert(0, name)
        AskEntry.grid(row=1, column=0, padx=5, pady=5)
        self.Ctne.grid(row=2, column=0, padx=5, pady=5)
    
    def rename(self, path, name):
        if type(path) == str:
            path = [path]
            name = [name]
        self.AskNme_rename.destroy()
        self.AskNme_rename = False
        result = self.User.re_name(path, name)
        if result['FailOrNot']:
            ntc_id = func_ui.add_task('正在重命名', 'percent', 0)
            self.User.gui_refresh(result['result']['data'], result['result']['task_id'], ntc_id)

    def rename_thread(self, path, name):
        Trf = threading.Thread(target=self.rename, args=(path, name))
        Trf.start()

    def ask_for_name_rename(self, name, path):
        """单文件重命名"""
        if self.AskNme_rename:
            self.AskNme_rename.destroy()
        self.AskNme_rename = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.AskNme_rename.title('文件名')
        self.AskNme_rename.iconbitmap('./logo.ico')
        self.AskNme_rename.resizable(0,0)
        labelINF = tk.Label(self.AskNme_rename, text='■ 请输入名称', anchor="nw",
                            compound='left', image=self.Img, relief='flat', 
                            width=200, height=20, bg=Total_Seeting.Color0, fg='white'
                            ).grid(row=0, column=0, padx=5)
        AskEntry = tk.Entry(self.AskNme_rename, width=28)
        self.Ctne = tk.Button(self.AskNme_rename, text='重命名',bg=Total_Seeting.Color2,
                fg=Total_Seeting.Fcolor, compound='center', bd=-1, height=30, 
                width=200, image=self.Img, relief='flat',
                command=lambda t3=path:self.rename_thread(t3, AskEntry.get()))
        AskEntry.insert(0, name)
        AskEntry.grid(row=1, column=0, padx=5, pady=5)
        self.Ctne.grid(row=2, column=0, padx=5, pady=5)

    def creat_dir(self, User: BaiDuCloud, path):
        self.AskNme_cdir.destroy()
        self.AskNme_cdir = False
        User.creat_dir(path)
        User.gui_refresh(False, False, False)

    def creat_dir_thread(self, User: BaiDuCloud, path):
        Tcd = threading.Thread(target=self.creat_dir, args=(User, path))
        Tcd.start()

    def creat_dir_UI(self, User: BaiDuCloud):
        """用于显示新建文件夹控件"""
        if self.AskNme_cdir:
            self.AskNme_cdir.destroy()
        self.AskNme_cdir = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.AskNme_cdir.title('文件名')
        self.AskNme_cdir.iconbitmap('./logo.ico')
        self.AskNme_cdir.resizable(0,0)
        labelINF = tk.Label(self.AskNme_cdir, text='■ 请输入新建文件夹的名称', anchor="nw",
                            compound='left', image=self.Img, relief='flat', 
                            width=200, height=20, bg=Total_Seeting.Color0, fg='white'
                            ).grid(row=0, column=0, padx=5)
        #self.AskNme_cdir.bind_all("<Return>", lambda event, t1=User:self.ext_and_exit_cdir(t1, AskEntry.get()))
        AskEntry = tk.Entry(self.AskNme_cdir, width=28)
        self.Ctne = tk.Button(self.AskNme_cdir, text='建立',bg=Total_Seeting.Color2,
                fg=Total_Seeting.Fcolor, compound='center', bd=-1, height=30, 
                width=200, image=self.Img, relief='flat',
                command=lambda t1=User:self.creat_dir_thread(t1, User.get_temp_path() + '/' + AskEntry.get()))
        AskEntry.grid(row=1, column=0, padx=5, pady=5)
        self.Ctne.grid(row=2, column=0, padx=5, pady=5)
        return True

    def save_files(self, User: BaiDuCloud, surl, pwd):
        self.Share_save.destroy()
        self.Share_save = False
        api_select = APIgetPath(self.main_window, User, User.share_start_save, surl=surl, pwd=pwd)
        api_select.show_get('/', False, False)

    def save_files_thread(self, User: BaiDuCloud, surl, pwd):
        Tsf = threading.Thread(target=self.save_files, args=(User, surl, pwd))
        Tsf.start()

    def save_file_UI(self, User):
        """保存的ui"""
        if self.Share_save:
            self.Share_save.destroy()
        self.Share_save = tk.Toplevel(master=self.main_window, bg=Total_Seeting.Color0)
        self.Share_save.title('分享链接及提取码')
        self.Share_save.iconbitmap('./logo.ico')
        self.Share_save.resizable(0,0)
        labelINF = tk.Label(self.Share_save, text='■ 分享链接', anchor="nw", compound='left',
                            image=self.Img, relief='flat', width=500, height=20,
                            bg=Total_Seeting.Color0, fg='white').grid(row=0, column=0, padx=5)
        lnk_frame = tk.Frame(self.Share_save, bg=Total_Seeting.Color0)
        EntryShareLink = tk.Entry(lnk_frame, width=67)
        EntryShareLink.grid(row=0, column=0, padx=5, pady=5)
        self.p_lnk = tk.Button(lnk_frame,bg=Total_Seeting.Color2, command=lambda: func_other.paste(EntryShareLink),
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=20, width=20, image=self.ImgFile_paste)
        self.p_lnk.grid(row=0, column=1, padx=5, pady=0)
        lnk_frame.grid(row=1, column=0, padx=5, pady=5)

        labelINF = tk.Label(self.Share_save, text='■ 提取码', anchor="nw", compound='left',
                            image=self.Img, relief='flat', width=500, height=20,
                            bg=Total_Seeting.Color0, fg='white').grid(row=2, column=0, padx=5)
        
        pwd_frame = tk.Frame(self.Share_save, bg=Total_Seeting.Color0)
        EntryPwd=tk.Entry(pwd_frame, width=67)
        EntryPwd.grid(row=0, column=0, padx=5, pady=5)
        self.p_pwd = tk.Button(pwd_frame,bg=Total_Seeting.Color2, command=lambda: func_other.paste(EntryPwd),
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=20, width=20, image=self.ImgFile_paste)
        self.p_pwd.grid(row=0, column=1, padx=5, pady=0)
        pwd_frame.grid(row=3, column=0, padx=5, pady=5)

        self.CopyPWD = tk.Button(self.Share_save, text='开始保存', bg=Total_Seeting.Color2,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                command=lambda: self.save_files_thread(User, EntryShareLink.get(), EntryPwd.get()),
                                bd=-1, height=30, width=500, image=self.Img)
        self.CopyPWD.grid(row=4, column=0, padx=5, pady=5)
        return True

    #upload file
    def upload(event, User: BaiDuCloud):
        target_path = User.get_temp_path()
        file_path = filedialog.askopenfilename(title=u'选择文件')
        User.upload_file_thread(target_path, file_path.split('/')[-1], file_path)