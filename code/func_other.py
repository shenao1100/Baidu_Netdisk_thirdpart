#-*- coding:utf-8 -*-
#CREATER: ShenAo

import NTG_base
import Total_Seeting
import func_ui

import tkinter as tk
from tkinter import filedialog
from subprocess import call
import pyperclip
import threading
import subprocess
import json
import time
import ast
import os

def ProcessLink(input):
    found = 'https://pan.baidu.com/s/' in input
    if found == True:
        found = '#list/' in input
        init_found = 'init?surl=' in input
        if found == True and init_found == False:
            input = NTG_base.getSubstr(input, 'https://pan.baidu.com/s/', '#list/')
        elif found == False and init_found == False:
            input = NTG_base.strstr(input, 'https://pan.baidu.com/s/')
        elif found == True and init_found == True:
            input = NTG_base.getSubstr(input, '?surl=', '#list/')
        elif found == False and init_found == True:
            input = NTG_base.strstr(input, '?surl=')
        return input
    else:
        return input


def colorChange(part, color):
    if type(part) == list:
        for i in part:
            i['bg'] = color
    else:
        part['bg'] = color


class Notice:
    def __init__(self, Title):
        self.Color0 = Total_Seeting.Color0     #背景色
        self.Color0_5 = Total_Seeting.Color0_5
        self.Color1 = Total_Seeting.Color1      #标签色
        self.Color2 = Total_Seeting.Color2      #按钮色
        self.Color3 = Total_Seeting.Color3      #Satu色
        self.Fcolor = Total_Seeting.Fcolor      #字体色
        self.Color2_Hold = Total_Seeting.Color2_Hold
        self.Color1_Hold = Total_Seeting.Color1_Hold

        self.Img =  tk.PhotoImage(file = './res/show.png')
        self.bg=tk.PhotoImage(file = './res/notice.png')
        self.window = tk.Toplevel(bg=self.Color0)
        self.window.title(Title)
        self.window.protocol("WM_DELETE_WINDOW", lambda: func_ui.showwarning('警告', '请不要关闭'))
        self.window.iconbitmap('./logo.ico')
        self.window.resizable(0,0)
        self.labelINF = tk.Label(self.window, anchor= 'e', text='', compound='top', 
                                image=self.Img, relief='flat', width=350, height=100, 
                                bg=self.Color0, fg='white', font=('Arial', 16, "bold"),
                                justify="right")
        self.labelINF.grid(row=0, column=0, padx=5)

    def Change(self, text):
        #if len(text) > 14:
        #    text='..' + text[(len(text) - 14):]
        self.labelINF['text'] = text
        self.labelINF.update()
        return True

    def Destory(self):
        self.window.destroy()

def change_pause_shart(part: tk.Button, command):
    if part['text'] == '▷':
        part['text'] = '||'
        part.update()
        command.start_task()
    elif part['text'] == '||':
        part['text'] = '▷'
        part.update()
        command.pause_task()

def select_ext(list, ext: str):
    ext = ext.lower().replace('.', '')
    inf_50px = {
        #图片
        'png': list['50px_photo'],
        'bmp': list['50px_photo'],
        'jpg': list['50px_photo'],
        'png': list['50px_photo'],
        'tif': list['50px_photo'],
        'gif': list['50px_photo'],
        'pcx': list['50px_photo'],
        'tga': list['50px_photo'],
        'exif': list['50px_photo'],
        'fpx': list['50px_photo'],
        'svg': list['50px_photo'],
        'psd': list['50px_photo'],
        'cdr': list['50px_photo'],
        'pcd': list['50px_photo'],
        'dxf': list['50px_photo'],
        'ufo': list['50px_photo'],
        'eps': list['50px_photo'],
        'ai': list['50px_photo'],
        'raw': list['50px_photo'],
        'WMF': list['50px_photo'],
        'webp': list['50px_photo'],
        'avif': list['50px_photo'],
        'apng': list['50px_photo'],
        #视频
        'mp4': list['50px_video'],
        'mov': list['50px_video'],
        'wmv': list['50px_video'],
        'flv': list['50px_video'],
        'avi': list['50px_video'],
        'avchd': list['50px_video'],
        'webm': list['50px_video'],
        'mkv': list['50px_video'],
        #iso
        'iso': list['50px_iso'],
        #excel
        'xlsx': list['50px_excel'],
        'xls': list['50px_excel'],
        'csv': list['50px_excel'],
        #ppt
        'pptx': list['50px_ppt'],
        'pptm': list['50px_ppt'],
        'pps': list['50px_ppt'],
        'ppsx': list['50px_ppt'],
        'ppa': list['50px_ppt'],
        'ppam': list['50px_ppt'],
        'pot': list['50px_ppt'],
        'potx': list['50px_ppt'],
        'thmx': list['50px_ppt'],
        #word
        'docx': list['50px_word'],
        'docm': list['50px_word'],
        'doc': list['50px_word'],
        'dotx': list['50px_word'],
        'dotm': list['50px_word'],
        'dot': list['50px_word'],
        #txt
        'txt': list['50px_txt'],
        #音乐
        #'cda': list['50px_music'],
        #'wav': list['50px_music'],
        #'mp3': list['50px_music'],
        #'wma': list['50px_music'],
        #'ra': list['50px_music'],
        #'midi': list['50px_music'],
        #'ogg': list['50px_music'],
        #'ape': list['50px_music'],
        #'flac': list['50px_music'],
        #'aac': list['50px_music'],
    }
    inf_long = {
        #图片
        'png': list['Short_photo'],
        'bmp': list['Short_photo'],
        'jpg': list['Short_photo'],
        'png': list['Short_photo'],
        'tif': list['Short_photo'],
        'gif': list['Short_photo'],
        'pcx': list['Short_photo'],
        'tga': list['Short_photo'],
        'exif': list['Short_photo'],
        'fpx': list['Short_photo'],
        'svg': list['Short_photo'],
        'psd': list['Short_photo'],
        'cdr': list['Short_photo'],
        'pcd': list['Short_photo'],
        'dxf': list['Short_photo'],
        'ufo': list['Short_photo'],
        'eps': list['Short_photo'],
        'ai': list['Short_photo'],
        'raw': list['Short_photo'],
        'WMF': list['Short_photo'],
        'webp': list['Short_photo'],
        'avif': list['Short_photo'],
        'apng': list['Short_photo'],
        #视频
        'mp4': list['Short_video'],
        'mov': list['Short_video'],
        'wmv': list['Short_video'],
        'flv': list['Short_video'],
        'avi': list['Short_video'],
        'avchd': list['Short_video'],
        'webm': list['Short_video'],
        'mkv': list['Short_video'],
        #iso
        'iso': list['Short_iso'],
        'img': list['Short_iso'],
        'gho': list['Short_iso'],
        'wim': list['Short_iso'],
        #excel
        'xlsx': list['Short_excel'],
        'xls': list['Short_excel'],
        'csv': list['Short_excel'],
        #ppt
        'pptx': list['Short_ppt'],
        'pptm': list['Short_ppt'],
        'pps': list['Short_ppt'],
        'ppsx': list['Short_ppt'],
        'ppa': list['Short_ppt'],
        'ppam': list['Short_ppt'],
        'pot': list['Short_ppt'],
        'potx': list['Short_ppt'],
        'thmx': list['Short_ppt'],
        #word
        'docx': list['Short_word'],
        'docm': list['Short_word'],
        'doc': list['Short_word'],
        'dotx': list['Short_word'],
        'dotm': list['Short_word'],
        'dot': list['Short_word'],
        #txt
        'txt': list['Short_txt'],
        #zip
        'rar': list['Short_zip'],
        'zip': list['Short_zip'],
        'tar': list['Short_zip'],
        'gz': list['Short_zip'],
        '7z': list['Short_zip'],
        #音乐
        'cda': list['Short_music'],
        'wav': list['Short_music'],
        'mp3': list['Short_music'],
        'wma': list['Short_music'],
        'ra': list['Short_music'],
        'midi': list['Short_music'],
        'ogg': list['Short_music'],
        'ape': list['Short_music'],
        'flac': list['Short_music'],
        'aac': list['Short_music'],
    }

    Img_50px = inf_50px.get(ext, list['50px_file'])
    Img_Short = inf_long.get(ext, list['Short_file'])
    return {'50px': Img_50px, 'Short': Img_Short}

def open_download_dir():
    call(['explorer', Total_Seeting.Path.replace('/', '\\')])

def paste(part: tk.Entry):
    part.delete(0, 'end')
    part.insert(0, pyperclip.paste())
    return True

def creat_share_task(user, surl, pwd):
    if len(surl) == 0:
        func_ui.showinfo('提示', '分享链接不能为空')
        return False
    if Total_Seeting.svip_user:
        surl = ProcessLink(surl)
        Total_Seeting.svip_user.share_start_download(surl, pwd)
    elif user:
        surl = ProcessLink(surl)
        user.share_start_download(surl, pwd)
    else:
        func_ui.showinfo('提示', '您需要先登录并点击一个账号才能进行此操作')
        return False
        
def creat_share_task_thread(user, surl, pwd):
    Tsc = threading.Thread(target=creat_share_task, args=(user, surl, pwd))
    Tsc.start()

#
#       main page function
#




def get_virus_info(part: tk.Label):
    #腾讯的接口
    url_c = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf'
    url_w = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryConfirmAdd,WomWorld,WomAboard'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69'
    }
    temp_w = NTG_base.get(url_w, header, '', '')
    temp_c = NTG_base.get(url_c, header, '', '')
    if temp_c and temp_w:
        country_inf = json.loads(temp_c['text'])
        word_inf = json.loads(temp_w['text'])
        for i in country_inf['data']['diseaseh5Shelf']['areaTree']:
            if i['name'] == '中国':
                cn_confrim_today = i['today']['confirm']
                cn_now_confrim = i['total']['nowConfirm']
                cn_total_dead = i['total']['dead']
                cn_total_confrim = i['total']['confirm']
        data_w = word_inf['data']['WomWorld']
        wd_confrim_today = data_w['nowConfirmAdd']
        wd_now_confrim = data_w['nowConfirm']
        wd_total_confrim = data_w['confirm']
        wd_total_dead = data_w['dead']
    else:
        part['text'] = '获取失败\n请点击主页按钮刷新'
        part.update()
        return False
    text=('截止到当日\n中国:' + 
            '\n今日新增确诊:' + str(cn_confrim_today) +
            '   现确诊:' + str(cn_now_confrim) + 
            '   总死亡:' + str(cn_total_dead) + 
            '   总确诊:' + str(cn_total_confrim) + 
            '\n海外:' + 
            '\n较昨日:' + str(wd_confrim_today) +
            '   现确诊:' + str(wd_now_confrim) + 
            '   总死亡:' + str(wd_total_dead) + 
            '   总确诊:' + str(wd_total_confrim))
    part['text'] = text
    part.update()
    return True

def change_help(part: tk.Label):
    help_list = [
        '在我的账号界面左上角单击\"+\"\n即可添加账号',
        '本程序的批量保存不受数量限制\n但需要更长的时间',
        '需要一键更改多个文件的名称/添加\n序号?\n试试批量重命名功能!',
        '需要将很多文件中的每一个都分享出\n链接?\n试试批量分享功能!',
        '想使用多线程下载引擎?\n现已支持Aria2c和IDM!\n在设置里更改吧!',
        '出现问题?\n尝试设置中的恢复出厂设置',
        '若您想要分享此软件\n请前往设置中删除个人信息\n否则有信息泄露的风险',
        '返回上一层请点击地址栏左边的箭头',
        '全选?全不选?\n点击地址栏左边的对勾试试吧!',
        '使用Aira2c下载文件时\n操作可能会有延迟',
        '移动复制删除去哪了？\n左键单击文件右侧的三个点试试!',
        '一键回到根目录?\n找找地址栏右侧有没有房子图标吧!',
        '下载需要设置下载路径\n在设置里点击浏览即可设置!',
        '无法登录想知道是不是网络问题?\n尝试设置中的网络测试!',
        '您每点一次主页按钮\n疫情信息都会刷新',
        '我们的疫情信息来源于\n腾讯新闻，腾讯新闻的信息\n来源于国家国家卫健委\n真实有效',
        '若您遇到打开文件夹时的\n未响应，您的网络状态可能不是很好',
        '本软件不会上传您的任何信息\n因为我连服务器都没有\n更新检测靠的是gitee',
        '我的确想做好看的UI\n奈何库不支持css',
        '由于使用的接口不同，我们可以更快的\n下载视频文件',
        '想要以图标的方式可视化您的文件？\n试试更多中的网盘分析!'
    ]
    while True:
        for msg in help_list:
            part['text'] = msg
            part.update()
            time.sleep(7)

def good_whatever(part: tk.Label):
    hour = time.localtime().tm_hour
    #so, 为啥python没有switch呢???????????
    if hour >= 0 and hour <= 2:
        day_time = '午夜好，注意身体'
    elif hour > 2 and hour <= 6:
        day_time = '凌晨好，注意作息'
    elif hour > 6 and hour <= 11:
        day_time = '早上好，新的一天'
    elif hour > 11 and hour <= 13:
        day_time = '中午好'
    elif hour > 13 and hour <= 18:
        day_time = '下午好'
    elif hour > 18 and hour < 24:
        day_time = '晚上好, 该休息了'
    text='  欢迎!  | ' + day_time
    part['text'] = text
    part.update()

#
#           login
#

def Boot_CheckCookieLoop() -> list:
    #启动时检查cookie文件，并分割cookie
    if os.path.exists('./data/cookie.dat'):
        CookieTemp = NTG_base.read_file('./data/cookie.dat')
        os.remove('./data/cookie.dat')
    else:
        CookieTemp = False

    if os.path.exists('./data/cookieTotal.dat'):
        result = NTG_base.read_file('./data/cookieTotal.dat')
        if result != '':
            CookieList = ast.literal_eval(result)
            if CookieTemp:
                CookieList.append(CookieTemp)
            CookieList = list(set(CookieList))
            NTG_base.write_file('./data/cookieTotal.dat', str(CookieList))
            Total_Seeting.Cookie_Loop = CookieList
            return CookieList
        else:
            return False
    else:
        if CookieTemp:
            Total_Seeting.Cookie_Loop = [CookieTemp]
            NTG_base.write_file('./data/cookieTotal.dat', str([CookieTemp]))
            return [CookieTemp]
        else:
            return False

def delete_cookie(cookie):
    Total_Seeting.Cookie_Loop.remove(cookie)
    NTG_base.write_file('./data/cookieTotal.dat', str(Total_Seeting.Cookie_Loop))

def Start_Browser():
    #自己写浏览器用pyqt太大了
    #用MBPython吧，官方文档是错的
    #干脆直接用以前的成品算了
    if os.path.exists('./data/cookie.dat'):
        os.remove('./data/cookie.dat')
    call('./cookie.exe')
    if os.path.exists('./data/cookie.dat'):
        result = NTG_base.read_file('./data/cookie.dat')
        Total_Seeting.Cookie_Loop.append(result)
        NTG_base.write_file('./data/cookieTotal.dat', str(Total_Seeting.Cookie_Loop))
        os.remove('./data/cookie.dat')
        return result
    else:
        return False






def process_input_rename(OriginalFilename, inputName):
    """多选时批量修改名字"""
    resultList = []
    count = 1
    leagle = '[number]' in inputName or '[origin]' in inputName
    if not leagle:
        func_ui.showwarning('警告', '文件名必须带有序号([number])或原文件名([origin])')
        return {'list': [], 'str': '文件名必须带有序号([number])或原文件名([origin])'}
    for i in OriginalFilename:
        filename, extension = os.path.splitext(i)
        insert = inputName.replace('[number]', str(count))
        insert = insert.replace('[ext]', extension)
        insert = insert.replace('[origin]', filename)
        resultList.append(insert)
        count += 1
    Resultstr = ''
    count = 0
    for i in resultList:
        Resultstr += i + '\n'
        count += 1
        if count == 15:
            Resultstr += '...'
            break
    return {'list': resultList, 'str': Resultstr}

def change_down_thread(thread):
    Total_Seeting.down_thread = thread
    Total_Seeting.save_setting()

def change_aria_start(tf):
    Total_Seeting.aria_start_with = tf
    Total_Seeting.save_setting()

def change_down_engine(text):
    Total_Seeting.down_method = text
    Total_Seeting.save_setting()

def save_PRC(text):
    Total_Seeting.aria_RPC = text
    Total_Seeting.save_setting()

def change_setting_downpath(part):
    path_text=filedialog.askdirectory()
    if not path_text == '':
        part['text'] = path_text
        part.update()
        Total_Seeting.Path = path_text
        Total_Seeting.save_setting()

def change_setting_idmpath(part):
    path_text=filedialog.askopenfilename()
    if not path_text == '':
        part['text'] = path_text
        part.update()
        Total_Seeting.idm_path = path_text
        Total_Seeting.save_setting()

def network_test():
    if NTG_base.get('http://pan.baidu.com/', '', '', ''):
        func_ui.showinfo('提示', '网络通畅')
    else:
        func_ui.showwarning('警告', '无法连接')

def reset_all():
    file_list = [
        './data/conf.dat',
        './data/cookieTotal.dat',
    ]
    for i in file_list:
        if os.path.exists(i):
            os.remove(i)
    func_ui.showwarning('警告', '删除完成\n按是退出，请手动重启程序')
    os._exit(0)

def start_aria2c():
    if Total_Seeting.aria_start_with:
        Ttask = threading.Thread(target=subprocess.Popen, args= ('./res/aria2c/RPC_in.exe', ))
        Ttask.start()

def open_download_dir():
    Ttask = threading.Thread(target=call, args= (['explorer', Total_Seeting.Path.replace('/', '\\')], ))
    Ttask.start()

def open_url(urls):
    Ttask = threading.Thread(target=call, args= (['explorer', urls], ))
    Ttask.start()

def check_for_update():
    return True
    result = NTG_base.get(Total_Seeting.update_url, '', '', '')
    try:
        result = json.loads(result['text'])
        if result['vernum'] > Total_Seeting.ver_num:
            func_ui.showinfo('', '发现更新\n{}'.format(result['msg']))
            open_url(result['url'])
    except:
        check_for_update()
