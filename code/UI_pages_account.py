#-*- coding:utf-8 -*-
#CREATER: ShenAo
import os
import tkinter as tk
import threading
from subprocess import call
from tkinter.messagebox import showinfo
from PIL import Image,ImageTk
from io import BytesIO

import func_ui
import Total_Seeting
import func_other
import func_adapt
from CORE_GetInfo import BaiDuCloud
from func_API import SelectUser, TopLevels
import NTG_base


class AccountPages:
    created_len = 0
    pages_list = []

    def __init__(self, account_select_frame: tk.Frame, BarCanves, part_frame: tk.Frame, window, ext_img) -> None:
        self.mother_window = window
        self.account_select_frame = account_select_frame
        self.BarCanves = BarCanves
        self.part_frame = part_frame
        self.ext_img_list = ext_img
        self.share_path_root = ''

        self.AccountImg = tk.PhotoImage(file='./res/Account.png')

        self.LeftMoveImg = tk.PhotoImage(file='./res/main_button/BTlong_move.png')
        self.LeftDelImg = tk.PhotoImage(file='./res/main_button/BTlong_DEL.png')
        self.LeftRenameImg = tk.PhotoImage(file='./res/main_button/BTlong_rename.png')
        self.LeftDownloadImg = tk.PhotoImage(file='./res/main_button/BTlong_download.png')
        self.LeftShareImg = tk.PhotoImage(file='./res/main_button/BTlong_share.png')
        self.SaveImg = tk.PhotoImage(file='./res/main_button/BTlong_save.png')

        self.selectImg = tk.PhotoImage(file='./res/select.png')
        self.NotslectImg = tk.PhotoImage(file='./res/not_select.png')
        self.MoreImg = tk.PhotoImage(file='./res/more.png')
        self.DownloadImg = tk.PhotoImage(file='./res/download.png')
        self.ShareImg = tk.PhotoImage(file='./res/share.png')
        self.orderImg = tk.PhotoImage(file='./res/order.png')
        self.addImg = tk.PhotoImage(file='./res/adddir.png')
        self.cookieImg = tk.PhotoImage(file='./res/cookie.png')

        self.ReloadImg = tk.PhotoImage(file='./res/reload.png')
        self.BackImg = tk.PhotoImage(file='./res/back.png')
        self.HomeImg = tk.PhotoImage(file='./res/home.png')
        self.AllSelectImg = tk.PhotoImage(file='./res/allselect.png')
        self.Img = tk.PhotoImage(file='./res/show.png')

        self.Floder = tk.PhotoImage(file='./res/File_Short/Floder.png')


        self.AddAccount = tk.PhotoImage(file='./res/main_button/add.png')
        self.Share_60px = tk.PhotoImage(file='./res/main_button/share.png')
        self.add_20px = tk.PhotoImage(file='./res/20px/add.png')
        self.share_20px = tk.PhotoImage(file='./res/20px/share.png')
        self.save_30px = tk.PhotoImage(file='./res/save_30px.png')
        self.down_30px = tk.PhotoImage(file='./res/down.png')
        self.ImgFile_paste = tk.PhotoImage(file='./res/paste.png')
        self.AddAccountButton = tk.Button(account_select_frame, text='+', bg=Total_Seeting.Color2,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=21, width=21, image=self.Img,
                                        command = lambda: self.add_new())
        self.AddAccountButton.grid(row=0, column=1024, padx=1, pady=0)
        self.Addtakeplace = tk.Label(account_select_frame, text='', bg=Total_Seeting.Color0,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=21, width=800, image=self.Img)
        self.Addtakeplace.grid(row=0, column=1025, padx=0, pady=0)
        self.control_list = []
        self.ActivateFrame = False
        self.more_button = False
        pass
    
    def change_page(self, page_show):
        for page_sg in AccountPages.pages_list:
            if page_sg == page_show:
                page_show.grid(row=0, column=0, padx=0, pady=0)
            else:
                page_sg.grid_forget()
        
    
    def close_page(self, page, select_button, delete_button, account_frame, bt_type):
        AccountPages.pages_list.remove(page)
        page.destroy()
        select_button.destroy()
        delete_button.destroy()
        account_frame.destroy()
        if bt_type['type'] == 'user':
            func_other.delete_cookie(bt_type['cookie'])
        return True

    def change_image(self, bt, url, User: BaiDuCloud):
        #while True:
        #    try:
        img_data = NTG_base.get(url, '', '', '')['content']
        photo = Image.open(BytesIO(img_data))  #括号里为需要显示在图形化界面里的图片

        photo = photo.resize((20,20))  #规定图片大小
        self.head_img = ImageTk.PhotoImage(photo)
        bt['image'] = self.head_img
        bt.bind("<Button-3>", func=lambda event: showinfo(
            'info',
            '！账号信息，请勿截图给任何人！' +'\n\n' +
            'Cookie: ' + str(User.Cookie) +'\n' +
            'Name: ' + str(User.Name) + '\n' +
            'Sign:' + str(User.sign) + '\n' +
            'Sign3:' + str(User.sign3) + '\n' +
            'ShareSign:' + str(User.share_sign) + '\n' +
            'Randsk:' + str(User.randsk) + '\n' +
            'needpr:' + str(User.needpr) + '\n' +
            'randsk:' + str(User.randsk) + '\n' +
            'uk:' + str(User.uk) + '\n' +
            'share_uk:' + str(User.share_uk) + '\n' +
            'share_id:' + str(User.share_id) + '\n' +
            'Logid:' + str(User.Logid) + '\n' +
            'surl:' + str(User.surl) + '\n' +
            'pwd:' + str(User.pwd) + '\n' +
            'time_stamp:' + str(User.time_stamp) + '\n' +
            'time:' + str(User.time) + '\n' +
            'share_sign:' + str(User.share_sign) + '\n'
        ))
        return True
            #except:
            #    continue

    def gen_new_sector(self, bt_name, pages, bt_type):
        AccountPages.created_len += 1
        self.change_page(pages)
        account_frame = tk.Frame(self.account_select_frame, bg=Total_Seeting.Color2)
        AccountButton = tk.Button(account_frame, text=bt_name, bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='left', relief='flat',
                                    command = lambda t1=pages: self.change_page(t1), anchor='w',
                                    bd=-1, height=21, width=150, image=self.Img)
        AccountDelete = tk.Button(account_frame, text='×', bg=Total_Seeting.ColorAccount,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=21, width=21, image=self.Img)
        AccountDelete['command'] = lambda t1=account_frame, t2=pages, t3=AccountButton, t4=AccountDelete, t5=bt_type: self.close_page(t2, t3, t4, t1, t5)
        AccountButton.grid(row=0, column=0, padx=0, pady=0)
        AccountDelete.grid(row=0, column=1, padx=0, pady=0)
        account_frame.grid(row=0, column=AccountPages.created_len, padx=1, pady=0)
        self.account_select_frame.update_idletasks()
        self.BarCanves.config(scrollregion=self.BarCanves.bbox("all"))

        if bt_type['type'] == 'user':
            Tlogin = threading.Thread(target=self.change_image, args= (AccountButton, bt_type['image'], bt_type['user']))
            Tlogin.start()
        else:
            image_list = {
                'new_page': self.add_20px,
                'share': self.share_20px,
            }
            AccountButton['image'] = image_list.get(bt_type['type'])

    def gen_add_page(self):
        #main
        self.FrameMain = tk.Frame(self.part_frame, bg=Total_Seeting.Color0)
        AccountPages.pages_list.append(self.FrameMain)
        self.FrameMain.config(height=425, width=800)
        self.FrameMain.grid_propagate(False)
        #main function
        
        self.FrameMain.grid(row=0, column=0, padx=0, pady=0)
        pass

    #
    #               function---account
    #

    def account_bind_button(self, toplevel_func: TopLevels, User: BaiDuCloud):
        self.CopyCookie.bind("<Button-1>", lambda event, t1=User: 
                                func_adapt.copy_cookie(t1))
        self.MitiMove['command'] = lambda: func_adapt.multiple_select_move(toplevel_func.main_window, User)
        self.MitiDelete['command'] = lambda: func_adapt.multiple_select_del(User)
        self.MitiRename['command'] = lambda: toplevel_func.multiple_select_rename(User)
        self.MitiDownload['command'] = lambda: func_adapt.thread_mutiselect_down(User)
        self.MitiShare['command'] = lambda: toplevel_func.multiple_select_share(User)
        self.MitiSave['command'] = lambda: toplevel_func.save_file_UI(User)
        self.ChangeOrder.bind("<Button-1>", func=func_adapt.MenuAdaptor(func_adapt.order_menu, 
                                            root=toplevel_func.main_window, User=User))

    def share_refresh_buttons(self, User: BaiDuCloud, s_id, start_path):
        self.MultSaveBt.bind("<Button-1>", lambda event: self.mulit_save(User, s_id, start_path))
        self.MultDownBt.bind("<Button-1>", lambda event: func_adapt.select_user_to_down_mix(self.mother_window, User.surl[s_id - 1], User.pwd[s_id], 
                                                                start_path, dir_list=User.SelectedList_Dir, file_list=User.SelectedList_File))

    #def mulit_down(self, User: BaiDuCloud):


    def mulit_save(self, User: BaiDuCloud, s_id, start_path):
        datas = {
            'surl': User.surl[s_id - 1],
            'pwd': User.pwd[s_id],
            'start_path': start_path,
            'datas': {
                'File': User.SelectedList_File,
                'Dir': User.SelectedList_Dir,
            }
        }
        user_selector = SelectUser(self.mother_window, 'select_to_save', datas)
        user_selector.show()
    
    def share_change(self, User: BaiDuCloud, path, count, s_id):
        thread_share = threading.Thread(target=self.share_change_func, args=(User, path, count, s_id))
        thread_share.start()
    
    def share_change_func(self, User: BaiDuCloud, path, count, s_id):
        orig_path = path
        #refresh select button list
        if count == 0:
            self.select_button_list = []
        if self.share_path_root == path:
            path = '/'
        #refresh path
        if path == '/':
            text_path = '分享链接根目录'
        else:
            text_path = path
        self.PathLabel['text'] = text_path

        #get file item list
        if path == User.get_temp_path():
            item_list = User.get_temp()['result']
        else:
            item_list = User.share_get_list(False, path, s_id)
        if path == '/':
            if item_list['Dir'] != []:
                self.share_path_root = NTG_base.get_back_path(item_list['Dir'][0]['path'])
            elif item_list['File'] != []:
                self.share_path_root = NTG_base.get_back_path(item_list['File'][0]['path'])
            path_rep = len(self.share_path_root)
        else:
            path_rep = len(path)
        
        #clear last frame
        if count == 0 and self.ActivateFrame:
            self.control_list = []
            self.ActivateFrame.destroy()
            self.continer_frame = tk.Frame(self.ImgFrame, bg=Total_Seeting.Color0)
            self.ActivateFrame = self.continer_frame
        else:
            if not self.ActivateFrame:
                self.continer_frame = tk.Frame(self.ImgFrame, bg=Total_Seeting.Color0)
                self.ActivateFrame = self.continer_frame
            else:
                self.continer_frame = self.ActivateFrame
        if self.more_button:
            self.more_button.destroy()
        #refresh button
        self.share_refresh_buttons(User, s_id, path_rep)
        #pack items
        self.continer_frame.grid(row=0, column=0, padx=0, pady=0)
        this_time_count = 0
        count_from_start = 0
        count_dir = -1
        count_file = -1

        share_uk = User.share_uk[s_id]

        logid = User.Logid[s_id]
        share_id = User.share_id[s_id]
        randsk = User.randsk[s_id]
        timestamp = User.time_stamp
        surl = User.surl[s_id - 1]
        pwd = User.pwd[s_id]
        for sg_dir in item_list['Dir']:
            if this_time_count >= Total_Seeting.list_show_len:
                break
            count_dir += 1
            count_from_start += 1
            if count_from_start > count:
                
                this_time_count += 1
                #pack
                self.OutsideFrame = tk.Frame(self.continer_frame, bg=Total_Seeting.Color0_5)
                self.OutsideFrame.grid_propagate(False)
                self.OutsideFrame.config(height=35, width=770)
                name = sg_dir['name']
                path = sg_dir['path']
                Time = sg_dir['time']
                show_name = sg_dir['name']
                fs_id = sg_dir['fs_id']
                if sg_dir['select']:
                    select_images = self.selectImg
                else:
                    select_images = self.NotslectImg
                
                self.SelectBt = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=35, width=35, image=select_images)
                self.select_button_list.append(self.SelectBt)
                self.OpenBt = tk.Label(self.OutsideFrame, text=show_name + '   ' + Time,
                                        fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.Color0_5,
                                        bd=-1, height=35, width=660, image=self.Floder,
                                        relief='flat', anchor='w')
                self.Download = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=35, width=35, image=self.DownloadImg)
                self.Save = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=35, width=35, image=self.save_30px)
                Time = sg_dir['time']
                fs_id = sg_dir['fs_id']
                self.OpenBt.bind("<Button-1>", lambda event, t1=path, t2=self.SelectBt: 
                                self.share_change(User, t1, 0, s_id))
                self.SelectBt.bind("<Button-1>", lambda event, t1=count_dir, t2=self.SelectBt: 
                                func_adapt.change_select(User, False, t1, t2, self.selectImg, self.NotslectImg))
                self.Download.bind("<Button-1>", lambda event, t2=sg_dir:
                                func_adapt.select_user_to_down_mix(self.mother_window, surl, pwd, path_rep, dir_list=[t2]))
                self.Save.bind("<Button-1>", lambda event, t1=User, t2=path, 
                                t3='', t4=share_uk, t5=fs_id, t6='', t7=logid, t8=share_id, 
                                t9=randsk, t10=sg_dir['save_path']:
                                func_adapt.select_user_to_save(self.mother_window, t3, t4, t5, t6,
                                                                t7, t8, t9, timestamp, surl, pwd, t10))
                control_list = [self.SelectBt, self.OpenBt, self.Download, self.Save]
                for control in control_list:
                    control.bind("<Enter>", lambda event, t1=control, t2=Total_Seeting.Color2: 
                                func_other.colorChange(t1, t2))
                    control.bind("<Leave>", lambda event, t1=control, t2=Total_Seeting.Color0_5: 
                                func_other.colorChange(t1, t2))
                self.SelectBt.grid(row=0, column=0, padx=0, pady=0)
                self.OpenBt.grid(row=0, column=1, padx=0, pady=0)
                self.Download.grid(row=0, column=2, padx=0, pady=0)
                self.Save.grid(row=0, column=3, padx=0, pady=0)
                self.OutsideFrame.grid(row=count_from_start, column=0, padx=3, pady=3)
        
        for sg_fl in item_list['File']:
            if this_time_count >= Total_Seeting.list_show_len:
                break
            count_file += 1
            count_from_start += 1
            
            if count_from_start > count:
                this_time_count += 1
                #pack
                self.OutsideFrame = tk.Frame(self.continer_frame, bg=Total_Seeting.Color0_5)
                self.OutsideFrame.grid_propagate(False)
                self.OutsideFrame.config(height=35, width=770)
                name = sg_fl['name']
                show_name = sg_fl['name']
                path = sg_fl['path']
                path_down = Total_Seeting.Path + '/' + show_name
                Time = sg_fl['time']
                fs_id = sg_fl['fs_id']
                ext = sg_fl['category']
                md5 = sg_fl['md5']
                if sg_fl['select']:
                    select_images = self.selectImg
                else:
                    select_images = self.NotslectImg
                FileImg = func_other.select_ext(self.ext_img_list, ext)['Short']
                self.SelectBt = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=35, width=35, image=select_images)
                self.select_button_list.append(self.SelectBt)
                self.OpenBt = tk.Label(self.OutsideFrame, text=show_name + '   ' + Time,
                                    fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=35, width=660, image=FileImg, 
                                    relief='flat', anchor='w')
                self.Download = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=35, width=35, image=self.DownloadImg)
                self.Save = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=35, width=35, image=self.save_30px)

                self.SelectBt.bind("<Button-1>", lambda event, t1=count_file, t2=self.SelectBt: 
                                func_adapt.change_select(User, True, t1, t2, self.selectImg, self.NotslectImg))
                
                self.Download.bind("<Button-1>", lambda event, t1=User, t2=sg_fl: 
                                func_adapt.select_user_to_down_mix(self.mother_window, surl, pwd, path_rep, file_list=[t2]))
                self.Save.bind("<Button-1>", lambda event, t1=User, t2=path, 
                                t3=md5, t4=share_uk, t5=fs_id, t6='', t7=logid, t8=share_id, 
                                t9=randsk, t10=sg_fl['save_path']:
                                func_adapt.select_user_to_save(self.mother_window, t3, t4, t5, t6,
                                                                t7, t8, t9, timestamp, surl, pwd, t10))

                control_list = [self.SelectBt, self.OpenBt, self.Download, self.Save]
                for control in control_list:
                    control.bind("<Enter>", lambda event, t1=control, t2=Total_Seeting.Color2: 
                                func_other.colorChange(t1, t2))
                    control.bind("<Leave>", lambda event, t1=control, t2=Total_Seeting.Color0_5: 
                                func_other.colorChange(t1, t2))
                self.SelectBt.grid(row=0, column=0, padx=0, pady=0)
                self.OpenBt.grid(row=0, column=1, padx=0, pady=0)
                self.Download.grid(row=0, column=2, padx=0, pady=0)
                self.Save.grid(row=0, column=3, padx=0, pady=0)
                self.OutsideFrame.grid(row=count_from_start, column=0, padx=3, pady=3)

        if count_from_start < len(item_list['File']) + len(item_list['Dir']):
            self.more_button = tk.Label(self.continer_frame, text=Total_Seeting.lg_loadmore,
                                    fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=20, width=560, image=self.Img, 
                                    relief='flat')
            self.more_button.bind("<Button-1>", lambda event, t1=path: 
                            self.share_change(User, orig_path, count_from_start, s_id))
            self.more_button.bind("<Enter>", lambda event, t1=self.more_button, t2=Total_Seeting.Color2: 
                            func_other.colorChange(t1, t2))
            self.more_button.bind("<Leave>", lambda event, t1=self.more_button, t2=Total_Seeting.Color0_5:
                                func_other.colorChange(t1, t2))
            self.more_button.grid(row=count_from_start + 1, column=0, padx=3, pady=3)

        self.Canves.bind_all("<MouseWheel>", self.mouse_wheel)
        self.ImgFrame.update_idletasks()
        self.TopFrame.config(height=370, width=800)
        self.Canves.config(scrollregion=self.Canves.bbox("all"))

        #refresh path label and function button
        self.reloadBt['command'] = lambda t1=orig_path: self.share_change(User, t1, 0, s_id)
        self.Back['command'] = lambda t1=orig_path: self.share_change(User, NTG_base.get_back_path(t1), 0, s_id)
        self.AllSelect['command'] = lambda: func_adapt.change_all_select(User, self.select_button_list, self.selectImg, self.NotslectImg)
        self.Home['command'] = lambda: self.share_change(User, '/', 0, s_id)
        refresh_list = [self.AllSelect, self.Home, self.reloadBt, self.Back]
        for i in refresh_list:
            i.update()
        #update info
        #self.TotalInfoLabel['text'] = (Total_Seeting.lg_total + str(len(item_list['result']['FileList']) + len(item_list['result']['DirList'])) + 
        #                            Total_Seeting.lg_nowshow + str(count_from_start) + Total_Seeting.lg_selection)
        pass
    
    def account_change(self, User: BaiDuCloud, path, count, is_refresh, toplevel_func: TopLevels):
        thread_account = threading.Thread(target=self.account_change_func, args=(User, path, count, is_refresh, toplevel_func))
        thread_account.start()

    def account_change_func(self, User: BaiDuCloud, path, count, is_refresh, toplevel_func: TopLevels):
        User.set_gui_refresh(lambda t1=path: self.account_change(User, t1, 0, True, toplevel_func))
        self.CreatDir.bind("<Button-1>", func_adapt.MenuAdaptor(
            func_adapt.upload_menu, root=toplevel_func.main_window, User=User, toplevel_func=toplevel_func))
        orig_path = path
        #refresh select button list
        if count == 0:
            self.select_button_list = []

        #refresh path
        self.PathLabel['text'] = path
        self.PathLabel.update()

        #get file item list
        
        if path == User.get_temp_path() and is_refresh == False:
            item_list = User.get_temp()
        else:
            item_list = User.get_file_list(path, True)
        #clear last frame
        if (count == 0 or is_refresh == True) and self.ActivateFrame:
            self.control_list = []
            self.ActivateFrame.destroy()
            self.continer_frame = tk.Frame(self.ImgFrame, bg=Total_Seeting.Color0)
            self.ActivateFrame = self.continer_frame
        else:
            if not self.ActivateFrame:
                self.continer_frame = tk.Frame(self.ImgFrame, bg=Total_Seeting.Color0)
                self.ActivateFrame = self.continer_frame
            else:
                self.continer_frame = self.ActivateFrame
        if self.more_button:
            self.more_button.destroy()
        #pack items
        self.continer_frame.grid(row=0, column=0, padx=0, pady=0)
        this_time_count = 0
        count_from_start = 0
        count_dir = -1
        count_file = -1
        if item_list['result']['Dir'] == [] and item_list['result']['File'] == []:
            self.none = tk.Label(self.continer_frame, text='空空如也，这里什么也没有', bg=Total_Seeting.Color0,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=35, width=625, image=self.Img)
            self.none.grid(row=0, column=0, padx=0, pady=0)
        for sg_dir in item_list['result']['Dir']:
            if this_time_count >= Total_Seeting.list_show_len:
                break
            count_dir += 1
            count_from_start += 1
            if count_from_start > count:
                
                this_time_count += 1
                #pack
                self.OutsideFrame = tk.Frame(self.continer_frame, bg=Total_Seeting.Color0_5)
                self.OutsideFrame.grid_propagate(False)
                self.OutsideFrame.config(height=35, width=625)
                name = sg_dir['server_filename']
                path = sg_dir['path']
                Time = sg_dir['time']
                show_name = sg_dir['server_filename']
                fs_id = sg_dir['fs_id']
                if sg_dir['select']:
                    select_images = self.selectImg
                else:
                    select_images = self.NotslectImg
                
                self.SelectBt = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=35, width=35, image=select_images)
                self.select_button_list.append(self.SelectBt)
                self.OpenBt = tk.Label(self.OutsideFrame, text=show_name,
                                        fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.Color0_5,
                                        bd=-1, height=35, width=355, image=self.Floder,
                                        relief='flat', anchor='w')
                self.InfoBt = tk.Label(self.OutsideFrame, text=Time,
                                    fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=35, width=120, image=self.Img, font=('', 8),
                                    relief='flat', anchor='w')
                self.Download = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=35, width=35, image=self.DownloadImg)
                self.Share = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=35, width=35, image=self.ShareImg)
                self.More = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=35, width=35, image=self.MoreImg)
                self.OpenBt.bind("<Button-1>", lambda event, t1=path, t2=self.SelectBt: 
                                self.account_change(User, t1, 0, False, toplevel_func))
                self.InfoBt.bind("<Button-1>", lambda event, t1=path, t2=self.SelectBt: 
                                self.account_change(User, t1, 0, False, toplevel_func))
                self.SelectBt.bind("<Button-1>", lambda event, t1=count_dir, t2=self.SelectBt: 
                                func_adapt.change_select(User, False, t1, t2, self.selectImg, self.NotslectImg))
                self.Download.bind("<Button-1>", lambda event, t1=User, t2=path:
                                func_adapt.start_path_download(t1, t2))
                self.Share.bind("<Button-1>", lambda event, t1=User, t2=fs_id:
                                toplevel_func.ask_for_pwd(t2))
                self.More.bind("<Button-1>", func=func_adapt.MenuAdaptor(func_adapt.menu, User=User, 
                                inf=sg_dir, isfile=False, func_toplevel=toplevel_func))

                control_list = [self.SelectBt, [self.OpenBt, self.InfoBt], self.Download, self.Share, self.More]
                for control in control_list:
                    if type(control) == list:
                        for i in control:
                            i.bind("<Enter>", lambda event, t1=control, t2=Total_Seeting.Color2: 
                                        func_other.colorChange(t1, t2))
                            i.bind("<Leave>", lambda event, t1=control, t2=Total_Seeting.Color0_5: 
                                        func_other.colorChange(t1, t2))
                    else:
                        control.bind("<Enter>", lambda event, t1=control, t2=Total_Seeting.Color2: 
                                    func_other.colorChange(t1, t2))
                        control.bind("<Leave>", lambda event, t1=control, t2=Total_Seeting.Color0_5: 
                                    func_other.colorChange(t1, t2))
                self.SelectBt.grid(row=0, column=0, padx=0, pady=0)
                self.OpenBt.grid(row=0, column=1, padx=0, pady=0)
                self.InfoBt.grid(row=0, column=2, padx=0, pady=0)
                self.Download.grid(row=0, column=3, padx=0, pady=0)
                self.Share.grid(row=0, column=4, padx=0, pady=0)
                self.More.grid(row=0, column=5, padx=0, pady=0)
                self.OutsideFrame.grid(row=count_from_start, column=0, padx=3, pady=3)
                
        for sg_fl in item_list['result']['File']:
            if this_time_count >= Total_Seeting.list_show_len:
                break
            count_file += 1
            count_from_start += 1
            
            if count_from_start > count:
                this_time_count += 1
                #pack
                self.OutsideFrame = tk.Frame(self.continer_frame, bg=Total_Seeting.Color0_5)
                self.OutsideFrame.grid_propagate(False)
                self.OutsideFrame.config(height=35, width=625)
                name = sg_fl['name']
                show_name = sg_fl['name']
                path = sg_fl['path']
                Time = sg_fl['time']
                fs_id = sg_fl['fs_id']
                ext = sg_fl['category']
                if sg_fl['select']:
                    select_images = self.selectImg
                else:
                    select_images = self.NotslectImg
                FileImg = func_other.select_ext(self.ext_img_list, ext)['Short']
                self.SelectBt = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                        fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                        bd=-1, height=35, width=35, image=select_images)
                self.select_button_list.append(self.SelectBt)
                self.OpenBt = tk.Label(self.OutsideFrame, text=show_name,
                                    fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=35, width=355, image=FileImg, 
                                    relief='flat', anchor='w')
                self.InfoBt = tk.Label(self.OutsideFrame, text=Time + '\n' + NTG_base.size(sg_fl['size']),
                                    fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=35, width=120, image=self.Img, font=('', 8),
                                    relief='flat', anchor='w')
                self.Download = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=35, width=35, image=self.DownloadImg)
                self.Share = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=35, width=35, image=self.ShareImg)
                self.More = tk.Label(self.OutsideFrame, text=' ', bg=Total_Seeting.Color0_5,
                                    fg =Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=35, width=35, image=self.MoreImg)

                self.SelectBt.bind("<Button-1>", lambda event, t1=count_file, t2=self.SelectBt: 
                                func_adapt.change_select(User, True, t1, t2, self.selectImg, self.NotslectImg))
                
                self.Download.bind("<Button-1>", lambda event, t1=User, t2=path:
                                func_adapt.start_single_file_download(t1, t2))
                self.Share.bind("<Button-1>", lambda event, t1=User, t2=fs_id:
                                toplevel_func.ask_for_pwd(t2))
                
                self.More.bind("<Button-1>", func=func_adapt.MenuAdaptor(func_adapt.menu, User=User, 
                                inf=sg_fl, isfile=True, func_toplevel=toplevel_func))

                control_list = [self.SelectBt, [self.OpenBt, self.InfoBt], self.Download, self.Share, self.More]
                for control in control_list:
                    if type(control) == list:
                        for i in control:
                            i.bind("<Enter>", lambda event, t1=control, t2=Total_Seeting.Color2: 
                                        func_other.colorChange(t1, t2))
                            i.bind("<Leave>", lambda event, t1=control, t2=Total_Seeting.Color0_5: 
                                        func_other.colorChange(t1, t2))
                    else:
                        control.bind("<Enter>", lambda event, t1=control, t2=Total_Seeting.Color2: 
                                    func_other.colorChange(t1, t2))
                        control.bind("<Leave>", lambda event, t1=control, t2=Total_Seeting.Color0_5: 
                                    func_other.colorChange(t1, t2))
                self.SelectBt.grid(row=0, column=0, padx=0, pady=0)
                self.OpenBt.grid(row=0, column=1, padx=0, pady=0)
                self.InfoBt.grid(row=0, column=2, padx=0, pady=0)
                self.Download.grid(row=0, column=3, padx=0, pady=0)
                self.Share.grid(row=0, column=4, padx=0, pady=0)
                self.More.grid(row=0, column=5, padx=0, pady=0)
                self.OutsideFrame.grid(row=count_from_start, column=0, padx=3, pady=3)

        if count_from_start < len(item_list['result']['File']) + len(item_list['result']['Dir']):
            self.more_button = tk.Label(self.continer_frame, text=Total_Seeting.lg_loadmore,
                                    fg=Total_Seeting.Fcolor, compound='center', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=20, width=615, image=self.Img, 
                                    relief='flat')
            self.more_button.bind("<Button-1>", lambda event, t1=path: 
                            self.account_change(User, orig_path, count_from_start, False, toplevel_func))
            self.more_button.bind("<Enter>", lambda event, t1=self.more_button, t2=Total_Seeting.Color2: 
                            func_other.colorChange(t1, t2))
            self.more_button.bind("<Leave>", lambda event, t1=self.more_button, t2=Total_Seeting.Color0_5:
                                func_other.colorChange(t1, t2))
            self.more_button.grid(row=count_from_start + 1, column=0, padx=3, pady=3)

        self.Canves.bind_all("<MouseWheel>", self.mouse_wheel)
        self.ImgFrame.update_idletasks()
        self.TopFrame.config(height=400, width=650)
        self.Canves.config(scrollregion=self.Canves.bbox("all"))

        #refresh path label and function button
        self.reloadBt['command'] = lambda t1 = orig_path: self.account_change(User, t1, 0, True, toplevel_func)
        self.Back['command'] = lambda t1 = orig_path: self.account_change(User, NTG_base.get_back_path(t1), 0, False, toplevel_func)
        self.AllSelect['command'] = lambda: func_adapt.change_all_select(User, self.select_button_list, self.selectImg, self.NotslectImg)
        self.Home['command'] = lambda: self.account_change(User, '/', 0, True, toplevel_func)
        refresh_list = [self.AllSelect, self.Home, self.reloadBt, self.Back]
        for i in refresh_list:
            i.update()
        #update info
        Tinfo = threading.Thread(target=self.change_personal_inf, args= (User, ))
        Tinfo.start()
        self.TotalInfoLabel['text'] = (Total_Seeting.lg_total + str(len(item_list['result']['File']) + len(item_list['result']['Dir'])) + 
                                    Total_Seeting.lg_nowshow + str(count_from_start) + Total_Seeting.lg_selection)
        pass
    
    def change_personal_inf(self, User: BaiDuCloud):
        User.get_storage()
        used = NTG_base.size(User.Storage_Used)
        total = NTG_base.size(User.Storage_Total)
        self.UserInfoLabel['text'] = User.Name + '\n' + used + '/' + total
        self.UserInfoLabel.update()

    def gen_share_frame(self):
        #main
        self.FrameMain = tk.Frame(self.part_frame, bg=Total_Seeting.Color0)
        AccountPages.pages_list.append(self.FrameMain)
        """主frame"""
        self.MyAccountFrame = tk.Frame(self.FrameMain, bg=Total_Seeting.Color0)
        self.MyAccountFrame.grid(row=0, column=1, padx=0, pady=0)
        self.InfoBar = tk.Frame(self.MyAccountFrame, bg=Total_Seeting.Color1, bd=-2)
        #全选
        self.AllSelect = tk.Button(self.InfoBar, text=' ', bg=Total_Seeting.Color1,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat', 
                                bd=-1, height=21, width=23, image=self.AllSelectImg)
        #返回按钮
        self.Back = tk.Button(self.InfoBar, text=' ', bg=Total_Seeting.Color1,
                            fg=Total_Seeting.Fcolor, compound='center', relief='flat', 
                            bd=-1, height=21, width=23, image=self.BackImg)
        #路径label
        self.PathLabel = tk.Label(self.InfoBar, text='正在处理...', bg=Total_Seeting.Color0_5,
                                fg=Total_Seeting.Fcolor, compound='left', relief='flat', 
                                bd=-1, height=20, width=683, image=self.Img)
        #主页按钮
        self.Home = tk.Button(self.InfoBar, text=' ', bg=Total_Seeting.Color1,
                            fg=Total_Seeting.Fcolor, compound='center', relief='flat', 
                            bd=-1, height=21, width=23, image=self.HomeImg)
        #刷新按钮
        self.reloadBt = tk.Button(self.InfoBar, text=' ', bg=Total_Seeting.Color1,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=21, width=23, image=self.ReloadImg)
        
        self.AllSelect.grid(row=0, column=0, padx=0, pady=0)
        self.Back.grid(row=0, column=1, padx=0, pady=0)
        self.PathLabel.grid(row=0, column=2, padx=0, pady=0)
        self.Home.grid(row=0, column=3, padx=0, pady=0)
        self.reloadBt.grid(row=0, column=4, padx=0, pady=0)

        self.InfoBar.grid(row=0, column=0, padx=0, pady=0, sticky='n')
        self.InfoBar.grid_propagate(False)
        self.InfoBar.config(height=25, width=800)

        self.TopFrame = tk.Frame(self.MyAccountFrame, bg=Total_Seeting.Color0, bd=-2)
        self.TopFrame.grid_rowconfigure(0, weight=1)
        self.TopFrame.grid_columnconfigure(0, weight=1)
        self.TopFrame.grid_propagate(False)

        self.Canves = tk.Canvas(self.TopFrame, bg=Total_Seeting.Color0, bd=-2)
        self.Canves.grid(row=0, column=0, sticky="news")
        #   orient:适配 vertical horizontal
        self.sidebar = tk.Scrollbar(self.TopFrame, command=self.Canves.yview,
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
        self.TopFrame.config(height=370, width=800)
        self.Canves.config(scrollregion=self.Canves.bbox("all"))
        self.TopFrame.grid(row=1, column=0, padx=0, pady=0)

        self.CmdBar = tk.Frame(self.MyAccountFrame, bg=Total_Seeting.Color1, bd=-2)
        self.CmdBar.grid(row=2, column=0, padx=0, pady=0, sticky='n')
        self.CmdBar.grid_propagate(False)
        self.CmdBar.config(height=30, width=800)
        self.MultSaveBt = tk.Label(self.CmdBar, text='多选保存',
                                    fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=30, width=100, image=self.save_30px, 
                                    relief='flat', anchor='w')
        self.MultSaveBt.grid(row=0, column=0, padx=0, pady=0)
        self.MultDownBt = tk.Label(self.CmdBar, text='多选下载',
                                    fg=Total_Seeting.Fcolor, compound='left', bg=Total_Seeting.Color0_5,
                                    bd=-1, height=30, width=100, image=self.down_30px, 
                                    relief='flat', anchor='w')
        self.MultDownBt.grid(row=0, column=1, padx=3, pady=0)
        for i in [self.MultSaveBt, self.MultDownBt]:
            i.bind("<Enter>", lambda event, t1 = i, t2 = Total_Seeting.Color2: 
                func_other.colorChange(t1, t2))
            i.bind("<Leave>", lambda event, t1 = i, t2 = Total_Seeting.Color0_5: 
                func_other.colorChange(t1, t2))
        return self.FrameMain

    def gen_account_frame(self):
        #main
        self.FrameMain = tk.Frame(self.part_frame, bg=Total_Seeting.Color0)
        AccountPages.pages_list.append(self.FrameMain)
        #生成账号Frame的左侧边栏
        self.LeftSideBar = tk.Frame(self.FrameMain, bg=Total_Seeting.Color1)

        self.UserInfoLabel = tk.Label(self.LeftSideBar, bg=Total_Seeting.Color1, fg=Total_Seeting.Fcolor,
                                    height=2)
        self.UserInfoLabel.grid(row=1024, column=0, padx=0, pady=0)
        self.TotalInfoLabel = tk.Label(self.LeftSideBar, bg=Total_Seeting.Color3, fg=Total_Seeting.Fcolor,
                                        width=19, height=1)
        self.TotalInfoLabel.grid(row=1025, column=0, padx=0, pady=0)
        self.MitiMove = tk.Button(self.LeftSideBar, text=Total_Seeting.lg_groupmove, bg=Total_Seeting.Color2,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=40, width=140, image=self.LeftMoveImg,
                                font = ('Arial', 11))
        self.MitiDelete = tk.Button(self.LeftSideBar, text=Total_Seeting.lg_groupdelete, bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=40, width=140, image=self.LeftDelImg,
                                font = ('Arial', 11))
        self.MitiRename = tk.Button(self.LeftSideBar, text=Total_Seeting.lg_grouprename, bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=40, width=140, image=self.LeftRenameImg,
                                font = ('Arial', 11))
        self.MitiDownload = tk.Button(self.LeftSideBar, text=Total_Seeting.lg_groupdown, bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=40, width=140, image=self.LeftDownloadImg,
                                font = ('Arial', 11))
        self.MitiShare = tk.Button(self.LeftSideBar, text=Total_Seeting.lg_groupshare, bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=40, width=140, image=self.LeftShareImg,
                                font = ('Arial', 11))
        self.MitiSave = tk.Button(self.LeftSideBar, text=Total_Seeting.lg_groupsave, bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=40, width=140, image=self.SaveImg,
                                font = ('Arial', 11))
        self.func_frame = tk.Frame(self.LeftSideBar, bg=Total_Seeting.Color1)
        self.ChangeOrder = tk.Label(self.func_frame, text=' ', bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=40, width=40, image=self.orderImg)
        self.CreatDir = tk.Label(self.func_frame, text=' ', bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=40, width=40, image=self.addImg)
        self.CopyCookie = tk.Label(self.func_frame, text=' ', bg=Total_Seeting.Color2,
                                    fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                    bd=-1, height=40, width=40, image=self.cookieImg)
        control_list = [self.MitiMove, self.MitiDelete, self.MitiRename,
                        self.MitiDownload, self.MitiShare, self.ChangeOrder,
                        self.MitiSave, self.CreatDir, self.CopyCookie]
        for control in control_list:
            control.bind("<Enter>", lambda event, t = control: 
                        func_other.colorChange(t, Total_Seeting.Color3))
            control.bind("<Leave>", lambda event, t = control: 
                        func_other.colorChange(t, Total_Seeting.Color2))

        

        self.MitiMove.grid(row=0, column=0, padx=3, pady=3)
        self.MitiDelete.grid(row=1, column=0, padx=3, pady=3)
        self.MitiRename.grid(row=2, column=0, padx=3, pady=3)
        self.MitiDownload.grid(row=3, column=0, padx=3, pady=3)
        self.MitiShare.grid(row=4, column=0, padx=3, pady=3)
        self.MitiSave.grid(row=5, column=0, padx=3, pady=3)
        self.func_frame.grid(row=6, column=0, padx=0, pady=0, sticky='nw')
        self.ChangeOrder.grid(row=0, column=0, padx=3, pady=3)
        self.CreatDir.grid(row=0, column=1, padx=3, pady=3)
        self.CopyCookie.grid(row=0, column=2, padx=3, pady=3)

        self.LeftSideBar.grid_propagate(False)
        self.LeftSideBar.config(height=423, width=150)
        
        self.LeftSideBar.grid(row=0, column=0, padx=0, pady=0)
        """主frame"""
        self.MyAccountFrame = tk.Frame(self.FrameMain, bg=Total_Seeting.Color0)
        self.MyAccountFrame.grid(row=0, column=1, padx=0, pady=0)
        self.InfoBar = tk.Frame(self.MyAccountFrame, bg=Total_Seeting.Color1, bd=-2)
        #全选
        self.AllSelect = tk.Button(self.InfoBar, text=' ', bg=Total_Seeting.Color1,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat', 
                                bd=-1, height=21, width=23, image=self.AllSelectImg)
        #返回按钮
        self.Back = tk.Button(self.InfoBar, text=' ', bg=Total_Seeting.Color1,
                            fg=Total_Seeting.Fcolor, compound='center', relief='flat', 
                            bd=-1, height=21, width=23, image=self.BackImg)
        #路径label
        self.PathLabel = tk.Label(self.InfoBar, text='/', bg=Total_Seeting.Color0_5,
                                fg=Total_Seeting.Fcolor, compound='left', relief='flat', 
                                bd=-1, height=20, width=543, image=self.Img)
        #主页按钮
        self.Home = tk.Button(self.InfoBar, text=' ', bg=Total_Seeting.Color1,
                            fg=Total_Seeting.Fcolor, compound='center', relief='flat', 
                            bd=-1, height=21, width=23, image=self.HomeImg)
        #刷新按钮
        self.reloadBt = tk.Button(self.InfoBar, text=' ', bg=Total_Seeting.Color1,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=21, width=23, image=self.ReloadImg)
        
        self.AllSelect.grid(row=0, column=0, padx=0, pady=0)
        self.Back.grid(row=0, column=1, padx=0, pady=0)
        self.PathLabel.grid(row=0, column=2, padx=0, pady=0)
        self.Home.grid(row=0, column=3, padx=0, pady=0)
        self.reloadBt.grid(row=0, column=4, padx=0, pady=0)

        self.InfoBar.grid(row=0, column=0, padx=0, pady=0, sticky='n')
        self.InfoBar.config(height=21, width=650)

        self.TopFrame = tk.Frame(self.MyAccountFrame, bg=Total_Seeting.Color0, bd=-2)
        self.TopFrame.grid_rowconfigure(0, weight=1)
        self.TopFrame.grid_columnconfigure(0, weight=1)
        self.TopFrame.grid_propagate(False)

        self.Canves = tk.Canvas(self.TopFrame, bg=Total_Seeting.Color0, bd=-2)
        self.Canves.grid(row=0, column=0, sticky="news")
        #   orient:适配 vertical horizontal
        self.sidebar = tk.Scrollbar(self.TopFrame, command=self.Canves.yview,
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
        self.TopFrame.config(height=400, width=650)
        self.Canves.config(scrollregion=self.Canves.bbox("all"))
        self.TopFrame.grid(row=1, column=0, padx=0, pady=0)
        return self.FrameMain

    def gen_main_page(self):
        main_frame = tk.Frame(self.part_frame, bg=Total_Seeting.Color0)
        AccountPages.pages_list.append(main_frame)
        login = tk.Label(main_frame, text='登录', bg=Total_Seeting.Color0_5,
                                fg=Total_Seeting.Fcolor, compound='top', relief='flat', 
                                bd=-1, height=200, width=120, image=self.AddAccount,
                                font = (24, ))
        login.bind("<Button-1>", lambda event: self.login_thread())
        login.grid(row=0, column=0, padx=5, pady=5)

        share = tk.Label(main_frame, text='分享链接', bg=Total_Seeting.Color0_5,
                                fg=Total_Seeting.Fcolor, compound='top', relief='flat', 
                                bd=-1, height=200, width=120, image=self.Share_60px,
                                font = (24, ))
        share.bind("<Button-1>", lambda event: self.save_file_UI())
        share.grid(row=0, column=1, padx=5, pady=5)
        return main_frame

    def login_thread(self):
        Tlogin = threading.Thread(target=self.login)
        Tlogin.start()
    
    def save_file_UI(self):
        """保存的ui"""
        self.Share_save = tk.Toplevel(master=self.mother_window, bg=Total_Seeting.Color0)
        self.Share_save.title('分享链接及提取码')
        self.Share_save.iconbitmap('./logo.ico')
        self.Share_save.resizable(0,0)
        

        labelINF = tk.Label(self.Share_save, text='■ 分享链接', anchor="nw", compound='left',
                            image=self.Img, relief='flat', width=500, height=20,
                            bg=Total_Seeting.Color0, fg='white').grid(row=0, column=0, padx=5)
        
        lnk_frame = tk.Frame(self.Share_save, bg=Total_Seeting.Color0)
        EntryShareLink = tk.Entry(lnk_frame, width=67)
        EntryShareLink.grid(row=0, column=0, padx=5, pady=5)
        self.p_lnk = tk.Button(lnk_frame, bg=Total_Seeting.Color2, command=lambda: func_other.paste(EntryShareLink),
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=20, width=20, image=self.ImgFile_paste)
        self.p_lnk.grid(row=0, column=1, padx=5, pady=0)
        lnk_frame.grid(row=1, column=0, padx=5, pady=5)

        labelINF = tk.Label(self.Share_save, text='■ 提取码', anchor="nw", compound='left',
                            image=self.Img, relief='flat', width=500, height=20,
                            bg=Total_Seeting.Color0, fg='white').grid(row=2, column=0, padx=5)
        
        pwd_frame = tk.Frame(self.Share_save, bg=Total_Seeting.Color0)
        EntryPwd = tk.Entry(pwd_frame, width=67)
        EntryPwd.grid(row=0, column=0, padx=5, pady=5)
        self.p_pwd = tk.Button(pwd_frame, bg=Total_Seeting.Color2, command=lambda: func_other.paste(EntryPwd),
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                bd=-1, height=20, width=20, image=self.ImgFile_paste)
        self.p_pwd.grid(row=0, column=1, padx=5, pady=0)
        pwd_frame.grid(row=3, column=0, padx=5, pady=5)


        self.CopyPWD = tk.Button(self.Share_save, text='解析', bg=Total_Seeting.Color2,
                                fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                                command = lambda: self.start_share(EntryShareLink.get(), EntryPwd.get()),
                                bd=-1, height=30, width=500, image=self.Img)
        self.CopyPWD.grid(row=4, column=0, padx=5, pady=5)
        return True

    def start_share(self, surl, pwd):
        Tshare = threading.Thread(target=self.start_share_thread, args= (surl, pwd))
        Tshare.start()

    def start_share_thread(self, surl, pwd):
        self.Share_save.destroy()
        Users = BaiDuCloud('')
        
        pages_user = AccountPages(self.account_select_frame, self.BarCanves, self.part_frame, 
                                        self.mother_window, self.ext_img_list)
        Share_frame = pages_user.gen_share_frame()
        type_inf = {
            'type': 'share',
        }
        pages_user.gen_new_sector('分享链接', Share_frame, type_inf)
        s_id = Users.share_basic_inf(surl, pwd)
        if s_id:
            pages_user.share_change(Users, '/', 0, s_id)
        else:
            func_ui.showwarning('', '解析失败\n请检查提取码或链接是否存在!')


    def login(self):
        cookie = Start_Browser()
        if cookie:
            Users = BaiDuCloud(cookie)
            Total_Seeting.User_loop.append(Users)
            GetBasic = Users.start_get_basic_inf()
            if GetBasic['FailOrNot']:
                toplevel_func = TopLevels(self.mother_window, Users)
                pages_user = AccountPages(self.account_select_frame, self.BarCanves, self.part_frame, 
                                        self.mother_window, self.ext_img_list)
                User_frame = pages_user.gen_account_frame()
                type_inf = {
                    'type': 'user',
                    'image': GetBasic['result']['Photo'],
                    'cookie': cookie,
                    'user': Users,
                }
                pages_user.gen_new_sector(Users.Name, User_frame, type_inf)
                pages_user.account_bind_button(toplevel_func, Users)
                pages_user.account_change(Users, '/', 0, False, toplevel_func)
            else:
                func_ui.showerror('错误', GetBasic['ErrorMessage'])
            return True

    def add_new(self):
        page = self.gen_main_page()
        type_inf = {
            'type': 'new_page',
        }
        self.gen_new_sector('新建标签页', page, type_inf)

    def mouse_wheel(self, event):
        self.Canves.yview_scroll(int(-1*(event.delta/120)), "units")

def delete_cookie(cookie):
    Total_Seeting.Cookie_Loop.remove(cookie)
    NTG_base.write_file('./data/cookieTotal.dat', str(Total_Seeting.Cookie_Loop))

def Start_Browser():
    #自己写浏览器用pyqt太大了
    #用MBPython吧，官方文档是错的
    #干脆直接用以前的成品算了
    if os.path.exists('./data/data/cookie.dat'):
        os.remove('./data/data/cookie.dat')
    call('./data/cookie.exe')
    if os.path.exists('./data/data/cookie.dat'):
        result = NTG_base.read_file('./data/data/cookie.dat')
        Total_Seeting.Cookie_Loop.append(result)
        NTG_base.write_file('./data/cookieTotal.dat', str(Total_Seeting.Cookie_Loop))
        os.remove('./data/data/cookie.dat')
        
        return result
    else:
        return False

def login(account_select_frame: tk.Frame, BarCanves, part_frame: tk.Frame, window, ext_img):
    if func_other.Boot_CheckCookieLoop():
        #如果有cookie
        #获取基准
        for i in func_other.Boot_CheckCookieLoop():
            Users = BaiDuCloud(i)
            Total_Seeting.User_loop.append(Users)
            GetBasic = Users.start_get_basic_inf()
            if GetBasic['FailOrNot']:
                toplevel_func = TopLevels(window, Users)
                pages_user = AccountPages(account_select_frame, BarCanves, part_frame, window, ext_img)
                User_frame = pages_user.gen_account_frame()
                type_inf = {
                    'type': 'user',
                    'image': GetBasic['result']['Photo'],
                    'cookie': i,
                    'user': Users
                }
                pages_user.gen_new_sector(Users.Name, User_frame, type_inf)
                pages_user.account_bind_button(toplevel_func, Users)
                pages_user.account_change(Users, '/', 0, False, toplevel_func)
            else:
                func_ui.showerror('错误', GetBasic['ErrorMessage'])
                #is_del = messagebox.askyesno('询问', '登入一个账号的时候遇到了一些错误\n这可能是信息过期导致的，是否删除此账号？')
                #if is_del:
                #    func_other.delete_cookie(i)
                #    func_ui.showinfo('提示', '删除完成')
    else:
        pages_user = AccountPages(account_select_frame, BarCanves, part_frame, window, ext_img)