#-*- coding:utf-8 -*-
#CREATER: ShenAo

import tkinter as tk
import os
import threading
import pyperclip

from CORE_GetInfo import BaiDuCloud
from func_API import APIgetPath, TopLevels, SelectUser
import NTG_base
import CORE_download
import Total_Seeting
import func_ui

def change_select(User: BaiDuCloud, isFile, count, part, img_s, img_ns):
    res = User.change_select(isFile, count, None)
    if res:
        part['image'] = img_s
    else:
        part['image'] = img_ns
    part.update()
    return True

def change_all_select(User: BaiDuCloud, list_controls, img_s, img_ns):
    selected_count = len(User.SelectedList_Dir) + len(User.SelectedList_File)
    total_count = len(User.get_temp()['result']['Dir']) + len(User.get_temp()['result']['File'])
    if selected_count >= int(total_count / 2):
        #清空
        for i in list_controls:
            i['image'] = img_ns
            i.update()
        User.change_select(None, None, False)
    else:
        for i in list_controls:
            i['image'] = img_s
            i.update()
        User.change_select(None, None, True)

#download file

def start_single_file_download_therad(User: BaiDuCloud, path):
    func_ui.showinfo('提示', '已添加入解析任务')
    result = User.PCS_download_link(path, False)
    if not result['FailOrNot']:
        link_list = result['result']['link']
        path_file = result['result']['path']
        name_file = result['result']['name']
        user_agent = result['result']['UA']
        CORE_download.use_download_method(link_list, name_file, path_file, user_agent)
    else:
        func_ui.showwarning('警告', '获取失败')

def start_single_file_download(User: BaiDuCloud, path):
    Tdl = threading.Thread(target=start_single_file_download_therad, args=(User, path))
    Tdl.start()

def start_path_download(User: BaiDuCloud, path):
    Tdl = threading.Thread(target=User.file_loop, args=(path, False, False))
    Tdl.start()

#copy file
def copy_files(root_window, User: BaiDuCloud, pathList, name):
    if type(pathList) == str:
        pathList = [pathList]
        name = [name]
    result = APIgetPath(root_window, User, User.copy_file, pathList=pathList, nameList=name)
    result.show_get('/', False, False)

#move file

def move_files(root_window, User: BaiDuCloud, pathList, name):
    if type(pathList) == str:
        pathList=[pathList]
        name = [name]
    result = APIgetPath(root_window, User, User.move_file, pathList=pathList, nameList=name)
    result.show_get('/', False, False)

#delete file

def delete_file(User: BaiDuCloud, path):
    if type(path) == str:
        path = [path]
    result = User.delete_file(path)
    if result['FailOrNot']:
        ntc_id = func_ui.add_task('正在删除', 'percent', 0)
        User.gui_refresh(result['result']['data'], result['result']['task_id'], ntc_id)

def delete_file_thread(User: BaiDuCloud, path):
    Tdf = threading.Thread(target=delete_file, args=(User, path))
    Tdf.start()

#menu

def MenuAdaptor(fun, **kwds):
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

def copy(text):
    pyperclip.copy(text)
    func_ui.showinfo('', '已复制')

def attribute(wind, name, path, time, fs_id, size=None, fomat=None, md5=None):
    Img = tk.PhotoImage(file='./res/show.png')
    global attribute_wind
    attribute_wind = tk.Toplevel(master=wind, bg=Total_Seeting.Color0)
    attribute_wind.title('属性 - ' + name)
    attribute_wind.iconbitmap('./logo.ico')
    attribute_wind.resizable(0,0)
    if size:
        keys = ['名称', '路径', '创建时间', '文件ID', '大小', '格式', 'MD5']
        vals = [name, path, time, fs_id, size, fomat, md5]
    else:
        keys = ['名称', '路径', '创建时间', '文件ID']
        vals = [name, path, time, fs_id]

    count = 0
    for key, value in zip(keys, vals):
        count += 1
        labelINF = tk.Label(attribute_wind, text='■ ' + key, anchor="nw", compound='left',
                            image=Img, relief='flat', width=200, height=20, bg=Total_Seeting.Color0, 
                            fg='white').grid(row=count * 3 - 2, column=0, padx=5, sticky='W')
        labelINF = tk.Label(attribute_wind, text=value, compound='center', image=Img, relief='flat',
                            bg=Total_Seeting.Color0, fg='white').grid(row=count * 3 - 1, column=0, padx=5)
        Copy = tk.Label(attribute_wind, text='复制',bg=Total_Seeting.Color2,
                            fg=Total_Seeting.Fcolor, compound='center', relief='flat',
                            bd=-1, height=20, width=50, image=Img)
        Copy.grid(row=count * 3 - 1, column=1, padx=5, pady=5)
        Copy.bind("<Button-1>", lambda event, t1=value: copy(t1))
    return True

def menu(event, User: BaiDuCloud, inf, isfile, func_toplevel: TopLevels):
    """单文件 更多 按钮的菜单"""
    MenuBar = tk.Menu(func_toplevel.main_window, tearoff=0)
    if isfile:
        name = inf['name']
        path = inf['path']
        Time = inf['time']
        fs_id = inf['fs_id']
        ext = inf['category']
        md5 = inf['md5']
        size = NTG_base.size(inf['size'])
        
    else:
        name = inf['server_filename']
        path = inf['path']
        Time = inf['time']
        fs_id = inf['fs_id']
        
        
    MenuBar.add_command(label='移动', command=lambda: 
                        move_files(func_toplevel.main_window, User, path, name))
    MenuBar.add_command(label='删除', command=lambda t1=User, t3=path: 
                        delete_file_thread(t1, t3))
    MenuBar.add_command(label='复制', command=lambda: 
                        copy_files(func_toplevel.main_window, User, path, name))
    MenuBar.add_command(label='重命名', command=lambda: 
                        func_toplevel.ask_for_rename(User, name, path))
    if isfile:
        MenuBar.add_command(label='属性', command=lambda: 
                            attribute(func_toplevel.main_window, name, path, Time, fs_id,
                                        size, ext, md5))
        MenuBar.add_command(label='下载链接', command=lambda: 
                            func_toplevel.show_downlink(User.get_download_link(path, False)))
    else:
        MenuBar.add_command(label='属性', command=lambda: 
                            attribute(func_toplevel.main_window, name, path, Time, fs_id))
    MenuBar.post(event.x_root, event.y_root)

def change_order_func(bywhat, User: BaiDuCloud):
    Total_Seeting.ListOrder = bywhat
    Total_Seeting.save_setting()
    User.gui_refresh(False, False, False)
    return True


def change_order_reverse(bywhat, User: BaiDuCloud):
    Total_Seeting.ListReverse = bywhat
    Total_Seeting.save_setting()
    User.gui_refresh(False, False, False)
    return True

def upload_menu(event, root, User: BaiDuCloud, toplevel_func: TopLevels):
    """新建的菜单"""
    MenuBar = tk.Menu(root, tearoff=0)
    MenuBar.add_command(label='新建文件夹', command=lambda: toplevel_func.creat_dir_UI(User))
    MenuBar.add_command(label='上传文件', command=lambda: toplevel_func.upload(User))
    MenuBar.post(event.x_root, event.y_root)

def order_menu(event, root, User: BaiDuCloud):
    """排序按钮的菜单"""
    MenuBar = tk.Menu(root, tearoff=0)
    MenuBar.add_command(label='按时间排序', command=lambda: change_order_func('time', User))
    MenuBar.add_command(label='按名称排序', command=lambda: change_order_func('name', User))
    MenuBar.add_command(label='按大小排序', command=lambda: change_order_func('size', User))
    MenuBar.add_command(label='正序', command=lambda: change_order_reverse(True,  User))
    MenuBar.add_command(label='倒序', command=lambda: change_order_reverse(False, User))
    MenuBar.post(event.x_root, event.y_root)


#多文件
def multiple_select_move(main_window, User: BaiDuCloud):
    """多选的移动文件"""
    if User.SelectedList_File == [] and User.SelectedList_Dir == []:
        func_ui.showwarning('警告', '未选择任何文件/文件夹')
        return False
    name = []
    pathList = []
    for i in User.SelectedList_Dir:
        pathList.append(i['path'])
        name.append(i['server_filename'])
    for i in User.SelectedList_File:
        pathList.append(i['path'])
        name.append(i['name'])
    move_files(main_window, User, pathList, name)
    return True

def multiple_select_del(User: BaiDuCloud):
    """多选删除"""
    if User.SelectedList_File == [] and User.SelectedList_Dir == []:
        func_ui.showwarning('警告', '未选择任何文件/文件夹')
        return False
    pathList = []
    for i in User.SelectedList_Dir:
        pathList.append(i['path'])
    for i in User.SelectedList_File:
        pathList.append(i['path'])
    delete_file_thread(User, pathList)

def multiple_download(User: BaiDuCloud):
    """多文件整合下载，解析调用"""
    if Total_Seeting.Path == '' or not os.path.exists(Total_Seeting.Path):
        func_ui.showerror('错误', '未设置下载路径或路径不存在')
        return False
    if User.SelectedList_Dir != [] or User.SelectedList_File != []:
        func_ui.showinfo('提示', '已添加入解析任务')
        ntc_id = func_ui.add_task('请稍后...', 'cycle', -1)
        for i in User.SelectedList_Dir:
            User.file_loop(i['path'], False, ntc_id)
        for i in User.SelectedList_File:
            func_ui.manage_task(ntc_id, '正在解析' + i['path'], 'cycle', -1)
            result = User.PCS_download_link(i['path'], False)
            CORE_download.use_download_method(
                result['result']['link'], 
                result['result']['name'], 
                result['result']['path'], 
                result['result']['UA']
            )
        func_ui.delete_task(ntc_id)
    else:
        func_ui.showwarning('警告', '请选择文件下载')

    return True

def thread_mutiselect_down(User: BaiDuCloud):
    if Total_Seeting.Path == '' or not os.path.exists(Total_Seeting.Path):
        func_ui.showerror('错误', '未设置下载路径或路径不存在')
        return False
    Tthr = threading.Thread(target=multiple_download, args=(User, ))
    Tthr.start()



def copy_cookie(User: BaiDuCloud):
    pyperclip.copy(User.Cookie)
    func_ui.showinfo('完成', 'Cookie已经复制到剪切板')
    return True

def select_user_to_down_mix(root, surl, pwd, path, file_list=[], dir_list=[]):
    data = {
        'surl': surl,
        'pwd': pwd,
        'Dir': dir_list,
        'File': file_list,
        'path_len': path
    }
    selecter = SelectUser(root, 'select_to_down', data)
    selecter.show()

def select_user_to_save(root, md5, share_uk, fs_id, sign, logid, 
                        share_id, randsk, timestamp, surl, pwd, path):
    data = {
        'md5': md5,
        'share_uk': share_uk,
        'fs_id': fs_id,
        'sign': sign,
        'logid': logid,
        'share_id': share_id,
        'randsk': randsk,
        'path': path,
        'timestamp': timestamp,
        'surl': surl,
        'pwd': pwd,
    }
    selecter = SelectUser(root, 'share_to_save', data)
    selecter.show()


