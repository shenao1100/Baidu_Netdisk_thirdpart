#-*- coding:utf-8 -*-
#CREATER: ShenAo

from concurrent.futures import thread

from numpy import percentile
import CORE_download
from CORE_upload import Upload
import NTG_base
import Total_Seeting
import func_other
import func_ui

import time
import re
import json
import base64
import os
import random
import hashlib
import threading
from urllib.parse import quote

class BaiDuCloud:
    def __init__(self, Cookie):
        self.Cookie = Cookie

        #缓存的文件列表
        self.TempList = {'FailOrNot': False}
        self.SelectedList_File = []
        self.SelectedList_Dir = []
        #缓存的路径(用于刷新)
        self.TempPath = False
        #容量信息
        self.Storage_Total = 0
        self.Storage_Used = 0
        self.Storage_Free = 0

        #Uk,bdstoken,name
        self.Uk = ''
        self.BDstoken = ''
        self.Name = ''
        self.BAIDUID = ''       #164F50B57D0C10E8AFF2F86977094400:FG=1
        self.sign = ''
        self.sign3 = ''
        self.blocklist = ''
        self.local_logid = self.gen_logid()
        self.head_photo = None
        #不变参数
        self.AppID = '250528'
        self.Channel = 'chunlei'
        #share
        self.needpr = {}
        self.randsk = {}
        self.uk = {}
        self.share_uk = {}
        self.share_id = {}
        self.Logid = {}
        self.surl = []
        self.pwd = {}
        self.time_stamp = {}
        self.time = {}
        self.share_sign = {}
        #loop
        self.share_task_id_loop = {}
        ips = os.popen("ipconfig /all").read()
        self.ipv6 = re.findall(r"本地链接 IPv6 地址. . . . . . . . : ([a-f0-9:]*::[a-f0-9:]*)", ips, re.I)
        if self.ipv6 == None or self.ipv6 == []:
            self.ipv6 = 'fe80::4095:4514:df11:affc%7'
        self.logid = str(int(time.time() * 1000)) + ',' + self.ipv6[0] + '%eth1,' + str(random.randint(100000, 999999))
        self.logid = base64.b64encode(self.logid.encode()).decode()
        self.rand1 = self.gen_rand()
        self.rand2 = self.gen_rand()
        self.uid = hashlib.md5(self.logid.encode()).hexdigest().upper()
        self.process_cookie()
    
    def set_gui_refresh(self, command):
        """
        设置刷新用户界面的命令，方便在其他类中调用
        """
        self.refresh_command = command
    
    def gui_refresh_thread(self, data, task_id, ntc_id):
        """
        每0.3秒循环一次检测task_id的任务是否完成
        """
        if data:
            while True:
                time.sleep(0.3)
                result = self.is_done(task_id, data)
                if result['FailOrNot']:
                    func_ui.manage_task(ntc_id, False, False, result['result']['percent'])
                    if result['result']['status'] == 'success':
                        
                        break
            func_ui.delete_task(ntc_id)
        self.refresh_command()

    def gui_refresh(self, data, task_id, ntc_id):
        Ttask = threading.Thread(target=self.gui_refresh_thread, args= (data, task_id, ntc_id))
        Ttask.start()

    def get_temp(self):
        """
        返回缓存的文件列表
        """
        return self.TempList
    
    def get_temp_path(self):
        """
        返回当前的路径
        """
        return self.TempPath
        
    def change_select(self, isFile, count, clear_all):
        """
        选择的变更，选择/取消选择/全选/取消全选
        """
        if isFile:
            if clear_all == None:
                if self.TempList['result']['File'][count]['select']:
                    self.SelectedList_File.remove(self.TempList['result']['File'][count])
                    self.TempList['result']['File'][count]['select'] = False
                    return False
                else:
                    self.TempList['result']['File'][count]['select'] = True
                    self.SelectedList_File.append(self.TempList['result']['File'][count])
                    return True
        else:
            if clear_all == None:
                if self.TempList['result']['Dir'][count]['select']:
                    self.SelectedList_Dir.remove(self.TempList['result']['Dir'][count])
                    self.TempList['result']['Dir'][count]['select'] = False
                    return False
                else:
                    self.TempList['result']['Dir'][count]['select'] = True
                    self.SelectedList_Dir.append(self.TempList['result']['Dir'][count])
                    return True
        if clear_all == True:
            self.SelectedList_Dir = []
            self.SelectedList_File = []
            for i in self.TempList['result']['File']:
                self.SelectedList_File.append(i)
                i['select'] = True
            for i in self.TempList['result']['Dir']:
                self.SelectedList_Dir.append(i)
                i['select'] = True
        elif clear_all == False:
            self.SelectedList_Dir = []
            self.SelectedList_File = []
            for i in self.TempList['result']['File']:
                i['select'] = False
            for i in self.TempList['result']['Dir']:
                i['select'] = False
        pass
        
    def get_UK_BDstoken(self):
        """
        获取用户的UK，STOKEN，用户名，SIGN
        """
        url = 'https://pan.baidu.com/'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'pan.baidu.com',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
        }
        result = NTG_base.get(url, header, '', '')
        if not result:
            return False
        else:
            result = result['cookie']
        self.LogID = result['BAIDUID']
        self.BAIDUID = result['BAIDUID']
        #获取UK，BDSTOKEN
        Url = 'https://pan.baidu.com/api/gettemplatevariable?clienttype=0&app_id=250528&web=1&fields=[%22sign1%22,%22time%22,%22sign3%22,%22sign2%22,%22username%22,%22bdstoken%22,%22token%22,%22uk%22,%22isdocuser%22,%22servertime%22]'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'pan.baidu.com',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
            'Cookie': self.Cookie,
        }
        #传回为html
        Result = NTG_base.get(Url, header, '', '')
        if Result:
            Result = Result['text']
            if Result == None or int(json.loads(Result)["errno"]) != 0:
                return False
            self.Uk = json.loads(Result)['result']['uk']
            self.BDstoken = json.loads(Result)['result']['bdstoken']
            self.Name = json.loads(Result)['result']['username']
            self.sign3 = json.loads(Result)['result']['sign3']
            self.sign = json.loads(Result)['result']['sign1']
            self.time = str(json.loads(Result)['result']['servertime'])
            Url = 'https://pan.baidu.com/api/loginStatus?clienttype=0&app_id=250528&web=1'
            Result = NTG_base.get(Url, header, '', '')
            if Result:
                Result = Result['text']
                self.head_photo = json.loads(Result)['login_info']['photo_url']
            return True
        else:
            return False
    
    
    def get_storage(self):
        """
        容量信息 总/剩余/已用
        """
        #获取容量信息
        Url = 'https://pan.baidu.com/api/quota?app_id=' + self.AppID + '&bdstoken=' + self.BDstoken + '&channel=' + self.Channel + '&checkexpire=1&checkfree=1&clienttype=0&web=1'
        header = {
            'Accept': '*/*',
            'User-Agent': 'netdisk',
            'Referer': 'https://pan.baidu.com/disk/home',
            'Host': 'pan.baidu.com',
            'Cookie': self.Cookie,
        }
        Result = NTG_base.get(Url, header, '', '')
        #传回为json
        if Result:
            Result = json.loads(Result['text'])
            if Result['errno'] == 0:
                self.Storage_Total = Result['total']
                self.Storage_Free = Result['free']
                self.Storage_Used = Result['used']
                return True
            else:
                return False
        else:
            return False
    

    def start_get_basic_inf(self):
        """
        登录时获取基础信息
        """
        if BaiDuCloud.get_UK_BDstoken(self):
            if BaiDuCloud.get_storage(self):
                self.blocklist = self.get_blocklist()
                return {
                    'FailOrNot': True, 
                    'result': {
                        'Storage_Total': NTG_base.size(self.Storage_Total),
                        'Storage_Used': NTG_base.size(self.Storage_Used),
                        'Storage_Free': NTG_base.size(self.Storage_Free),
                        'Uk': self.Uk,
                        'BDstoken': self.BDstoken,
                        'Name': self.Name,
                        'Photo': self.head_photo,
                    }
                }
            else:
                return {'FailOrNot': False, 'ErrorMessage': '获取容量信息时出错!', 'code': 1}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '获取用户信息时出错!', 'code': 0}

    

    def get_file_list(self, path: str, is_record):
        '''
        获取文件列表，path:路径-str
        '''
        if is_record:
            self.TempPath = path
            self.SelectedList_File = []
            self.SelectedList_Dir = []
        if self.Uk == '':
            return {'FailOrNot': False, 'ErrorMessage': '函数使用错误,请不要自行引用!\n\n基础信息出错', 'code': 2}
        elif path == '':
            return {'FailOrNot': False, 'ErrorMessage': '函数使用错误,请不要自行引用!\n\n路径不能为空', 'code': 3}
        Url = 'https://pan.baidu.com/api/list?app_id=' + self.AppID + '&bdstoken=' + self.BDstoken + '&channel=' + self.Channel + '&clienttype=0&desc=1&dir=' + quote(path) + '&num=99999999999999&order=' + Total_Seeting.ListOrder + '&page=1&showempty=0&web=1'
        header = {
            'Cache-Control': 'no-cache',
            'Accept': '*/*',
            'Accept-Language': 'zh-cn',
            'User-Agent': 'netdisk',
            'Host': 'pan.baidu.com',
            'Referer': Url,
            'Cookie': self.Cookie,
        }
        Result = NTG_base.get(Url, header, '', '')
        if Result:
            Result = json.loads(Result['text'])
            if Result['errno'] == 0:
                Result = Result['list']
                #整理json，提取信息
                ReturnInfo = {'Dir': [], 'File': []}
                for i in Result:
                    if i['isdir'] == 1:
                        #是文件夹
                        if len(i['server_filename']) > Total_Seeting.show_len:
                            show_name = i['server_filename'][:Total_Seeting.show_len] + '...'
                        else:
                            show_name = i['server_filename']
                            if i['path'] == '/apps':
                                show_name = '我的应用数据'
                        
                        Temp = {
                            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['server_mtime'])),
                            'fs_id': i['fs_id'],
                            'path': i['path'],
                            'server_filename': i['server_filename'],
                            'select': False,
                            'show_name': show_name,
                        }
                        if not is_record:
                            for f in self.SelectedList_Dir:
                                if f['fs_id'] == i['fs_id']:
                                    Temp['select'] = True
                        ReturnInfo['Dir'].append(Temp)
                    elif i['isdir'] == 0:
                        haveExtInFile = '.' in i['server_filename']
                        if len(i['server_filename']) > Total_Seeting.show_len:
                            show_name = i['server_filename'][:Total_Seeting.show_len] + '...'
                        else:
                            show_name = i['server_filename']
                        if haveExtInFile:
                            ext = i['server_filename'].split('.')[-1]
                        else:
                            ext = ''
                        Temp = {
                            'category': ext,
                            'fs_id': i['fs_id'],
                            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['server_mtime'])),
                            'size': i['size'],
                            'path': i['path'],
                            'name': i['server_filename'],
                            'md5': i['md5'],
                            'select': False,
                            'show_name': show_name,
                        }
                        if not is_record:
                            for f in self.SelectedList_File:
                                if f['fs_id'] == i['fs_id']:
                                    Temp['select'] = True
                        ReturnInfo['File'].append(Temp)
                if Total_Seeting.ListReverse:
                    ReturnInfo['File'] = ReturnInfo['File'][::-1]
                    ReturnInfo['Dir'] = ReturnInfo['Dir'][::-1]
                #更新缓存
                
                if is_record:
                    self.TempList = {'FailOrNot': True, 'result': ReturnInfo, 'path': path}
                return {'FailOrNot': True, 'result': ReturnInfo}
            else:
                return {'FailOrNot': False, 'ErrorMessage': '文件列表获取失败\n\n服务器返回错误, ServerErrorCode:' + str(Result['errno']), 'code': 4}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '文件列表获取失败\n\n服务器无响应', 'code': 5}
    
    
    def file_loop(self, start_path, in_loop, ntc_id):
        """
        递归下载路径内所有文件

        根据输入的start_path来获取目录下的文件夹/子文件夹/文件
        in_loop是区分用户输入还是循环引用
        若为false，则为用户输入
        true时，输入的应为int，代替pr
        """
        #计算需要被替换掉的
        if not in_loop:
            if start_path == '/':
                start_path_len = 0
            else:
                path_primary = len(start_path.split('/')[-1])
                start_path_len = len(start_path) - path_primary
        else:
            start_path_len = in_loop
        if not ntc_id:
            is_root = True
            ntc_id = func_ui.add_task('正在处理', 'cycle', -1)
        else:
            is_root = False
        #开始循环
        #   获取列表
        lists = self.get_file_list(start_path, False)
        if lists['FailOrNot']:
            for sg_file in lists['result']['File']:
                func_ui.manage_task(ntc_id, '正在新建下载任务' + sg_file['path'], 'cycle', -1)
                result = self.PCS_download_link(sg_file['path'], start_path_len)
                if not result['FailOrNot']:
                    link_list = result['result']['link']
                    path_file = result['result']['path']
                    name_file = result['result']['name']
                    user_agent = result['result']['UA']
                    CORE_download.use_download_method(link_list, name_file, path_file, user_agent)
            for sg_dir in lists['result']['Dir']:
                func_ui.manage_task(ntc_id, '正在解析' + sg_dir['path'], 'cycle', -1)
                self.file_loop(sg_dir['path'], start_path_len, ntc_id)
        if is_root:
            func_ui.delete_task(ntc_id)

    def gen_rand(self):
        """
        生成40位RAND随机码
        """
        sets = 'abdef1234567890'
        result = ''
        for i in range(40):
            result += random.choice(sets)
        return result
    
    def gen_logid(self):
        logid = str(int(time.time() / 1000))
        sets = '1234567890'
        for i in range(7):
            logid += random.choice(sets)
        logid += '.'
        for i in range(16):
            logid += random.choice(sets)
        logid = base64.b64encode(logid.encode()).decode()
        return logid

    def gen_dp_logid(self):
        logid = ''
        sets = '1234567890'
        for i in range(20):
            logid += random.choice(sets)
        return logid

    def PCS_download_link(self, path, need_pr):
        """PCS接口"""
        devuid = self.uid + '|0'
        #devuid = '090D0060C3F77A510B89C52C8991422B|0'
        cuid = devuid
        time_now = self.time#str(int(time.time()))
        data = 'app_id=250528&check_blue=1&es=1&es1=1&clienttype=17&path=' + quote(path).replace('/', '%2F') + '&version=2.271.76&channel=p2p-pc_2.0_pc_netdisk_default&apn_id=1_0&freeisp=0&queryfree=0&use=0&version_app=10.1.72&origin=dlna&ver=1&devuid=' + devuid + '&cuid=' + cuid + '&rand=' + self.rand1 + '&time=' + time_now + '&to=h0,d0,d6,d7,d8s,d9&bflag=h0,d0,d6,d7,d8s,d9,h0-d10&dtype=1&err_ver=1.0&vip=0'
        header = {
            'Host': 'd.pcs.baidu.com',
            'User-Agent': 'netdisk;11.8.2;NTGtech;android-android;10;JSbridge4.4.0;jointBridge;1.1.0',
            'Accept': '*/*',
            'Content-Length': '453',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.Cookie,
        }
        url = 'http://d.pcs.baidu.com/rest/2.0/pcs/file?method=locatedownload'
        result = NTG_base.post(url, header, data, '')
        if result:
            result = json.loads(result['text'])
            link_list = []
            for i in result['urls']:
                link_list.append(i['url'])
            if need_pr:
                if path[need_pr:][0] == '/':
                    path_real = Total_Seeting.Path + path[need_pr:]
                else:
                    path_real = Total_Seeting.Path + '/' + path[need_pr:]
            else:
                path_real = Total_Seeting.Path + '/' + path.split('/')[-1]
            return {
                'FailOrNot': False, 
                'result': {
                    'link': link_list, 
                    'UA': 'netdisk;11.8.2;NTGtech;android-android;10;JSbridge4.4.0;jointBridge;1.1.0',
                    'path': path_real,
                    'name': path_real.split('/')[-1],
                    }
                }
            #CORE_download.use_download_method(link_list, path_real.split('/')[-1], path_real,  
            #                                'netdisk;11.8.2;NTGtech;android-android;10;JSbridge4.4.0;jointBridge;1.1.0')
        else:
            return {'FailOrNot': False, 'ErrorMessage': '文件列表获取失败\n\n服务器无响应', 'code': 29}
    
    def original_download_link(self, path, need_pr):
        """原版接口"""
        url = 'https://pan.baidu.com/cms/fgid?method=query&path=' + path + '&wp_retry_num=2&version=3.0.0.132&cr_cnt=0'
        
        header = {
            'Connection': 'Keep-Alive',
            'Host': 'pan.baidu.com',
            'User-Agent': 'netdisk;7.12.1.1;PC;PC-Windows;10.0.19041;WindowsBaiduYunGuanJia',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.Cookie,
        }
        result = NTG_base.get(url, header, '', '')
        
        header = {
            'Connection': 'Keep-Alive',
            'Host': 'd.pcs.baidu.com',
            'User-Agent': 'netdisk;7.12.1.1;PC;PC-Windows;10.0.19041;WindowsBaiduYunGuanJia',
            'Accept': '*/*',
            'Content-Length': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.Cookie,
        }
        url = 'https://d.pcs.baidu.com/rest/2.0/pcs/file?app_id=250528&method=locatedownload&check_blue=1&es=1&esl=1&path=' + quote(path).replace('/', '%2F').replace('_', '%5F').replace('.', '%2E') + '&ver=4.0&dtype=1&err_ver=1.0&ehps=0&open_pflag=0&clienttype=8&channel=00000000000000000000000000000000&version=7.12.1.1&devuid=' + self.uid + '&rand=' + self.rand1 + '&time=' + str(int(time.time())) + '&rand2=' + self.rand2 + '&vip=0&wp_retry_num=2&logid=' + self.logid + '&dpkg=1&sd=0'
        result = NTG_base.post(url, header, '', '')
        if result:
            result = json.loads(result['text'])
            down_link = result['urls'][0]['url']
            if need_pr:
                if path[need_pr:][0] == '/':
                    path_real = Total_Seeting.Path + path[need_pr:]
                else:
                    path_real = Total_Seeting.Path + '/' + path[need_pr:]
            else:
                path_real = Total_Seeting.Path + '/' + path.split('/')[-1]
            CORE_download.use_download_method(down_link, path_real.split('/')[-1], path_real,  
                                            'netdisk')
        else:
            return {'FailOrNot': False, 'ErrorMessage': '文件列表获取失败\n\n服务器无响应', 'code': 41}

    def get_download_link(self, path, need_pr):
        """账号内下 预览接口"""
        #我要吐槽一句
        #首先是rand随机值，根本就是个定量，我觉得40个0都能过
        #然后是logid，这logid根本就是login ID，每个客户端自动生成的，合着也是定量
        #devuid和cuid是一样的，但是不知道啥意思
        #
        #就这么几个定量把我整蒙了我去他的
        #

        #获取SIGN(sign1, 2, 3天知道他为啥要这么多sign)
        url = 'http://pan.baidu.com/api/mediainfo?check_blue=1&app_id=250528&type=M3U8_FLV_264_480&path=' + quote(path).replace('/', '%2F') + '&ehps=0&devuid=' + self.uid + '&clienttype=80&channel=android_5.1.1_LIO-AN00_bdnetdisktv_1022917u&version=1.0.0&logid=' + self.logid + '&cuid=' + self.uid + '&network_type=wifi&firstlaunchtime=' + str(int(time.time() - 40)) + '&rand=' + self.rand1 + '&time=' + str(int(time.time())) + '&apn_id=1_0&freeisp=0&queryfree=0&nom3u8=1&dlink=1&media=1&origin=dlna&needthird=1&thirdsign=' + self.sign3
        header = {
            'Accept': '*/*',
            'User-Agent': 'netdisk',
            'Host': 'pan.baidu.com',
            'Accept-Language': 'zh-cn',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Referer': url,
            'Cookie': self.Cookie,
        }
        result = NTG_base.get(url, header, '', '')
        if result:
            result = json.loads(result['text'])
            down_link = result['info']['dlink']
            if need_pr:
                if path[need_pr:][0] == '/':
                    path_real = Total_Seeting.Path + path[need_pr:]
                else:
                    path_real = Total_Seeting.Path + '/' + path[need_pr:]
            else:
                path_real = Total_Seeting.Path + '/' + path.split('/')[-1]
            return down_link
        else:
            return {'FailOrNot': False, 'ErrorMessage': '文件列表获取失败\n\n服务器无响应', 'code': 42}
    
    #########################################################################################
    #                                        分享下载
    #########################################################################################
    def share_get_sign(self, surl):
        """
        获取share_sign并添加进list
        """
        url = 'https://pan.baidu.com/share/tplconfig?surl=' + surl + '&fields=sign,timestamp&channel=chunlei&web=1&app_id=250528&clienttype=0'
        header = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'netdisk',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': url,
            'Cookie': self.Cookie,
        }
        result = NTG_base.get(url, header, '', '')
        if result:
            result = result['text']
            result = json.loads(result)
            sign = result['data']['sign']
            self.time_stamp[len(self.surl)] = str(result['data']['timestamp'])
            return sign
        else:
            return False
    
    def share_get_randsk(self, surl, pwd):
        """
        获取验证用的RANDSK并存入list
        """
        if surl[0] == '1':
            surl = surl[1:]
        url = 'https://pan.baidu.com/share/verify?channel=chunlei&clienttype=0&web=1&app_id=250528&surl=' + surl
        header = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://pan.baidu.com/disk/home',
            'Cookie': self.Cookie,
        }
        data = 'pwd=' + str(pwd)
        result = NTG_base.post(url, header, data, '')
        if result:
            result = result['text']
            try:
                result = json.loads(result)
                if result['errno'] != 0:
                    return False
            except:
                return False
            randsk = result['randsk']
            return randsk
        else:
            return False

    def share_get_uk_share_id(self, surl, Randsk):
        '''
        获取uk, share_id, bdstoken (均不变量)
        '''
        url = 'https://pan.baidu.com/s/' + surl
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39",
    		"Cookie": self.Cookie + '; BDCLND=' +  Randsk
        }
        result = NTG_base.get(url, header, '', '')
        
        if result:
            result = result['text']
            #正则获取
            Sign = re.search(r'locals.mset\((\{.*?\})\);', str(result))
            
            try:
                sign = json.loads(Sign.group(1))
            except:
                return {'FailOrNot': False, 'ErrorMessage': '获取UK时出错', 'code': 43}
            #获取信息
            Uk = str(sign['uk'])
            BDstoken = str(sign['bdstoken'])
            SharerID = str(sign['shareid'])
            SharerUk = str(sign['share_uk'])
            Share_Id = str(sign['shareid'])
            return {'FailOrNot': True, 'result': {'Uk': Uk, 'Share_Id': Share_Id, 'BDstoken': BDstoken, 'shareID': SharerID, 'share_Uk': SharerUk}}

        else:
            return {'FailOrNot': False, 'ErrorMessage': '向服务器获取UK、SHAREID、BDSTOKEN时出错', 'code': 45}
    
    def share_get_log_id(self, share_id, sign, uk):
        """
        获取Logid并返回，不存list
        """
        url = 'https://pan.baidu.com/share/autoincre?app_id=250528&channel=chunlei&clienttype=0&shareid=' + share_id + '&sign=' + sign + '&timestamp=' + self.time + '&type=1&uk=' + uk + '&web=1'
        header = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.Cookie,
            'Referer': 'https://pan.baidu.com/disk/home',
        }
        result = NTG_base.get(url, header, '', '')['headers']
        try:
            log_id = result['Logid']
            return log_id
        except:
            return False

    def share_get_list(self, isroot, path, s_id):
        """
        原版接口获取分享链接目录下文件列表
        """
        if isroot or path == '/':
            content = 'root=1'
        else:
            content = 'dir=' + quote(path).replace('/', '%2F')
        self.TempPath = path
        self.SelectedList_File = []
        self.SelectedList_Dir = []
        url = 'https://pan.baidu.com/share/list?app_id=250528&channel=chunlei&clienttype=0&desc=1&num=999&order=time&page=1&' + content + '&shareid=' + self.share_id[s_id] + '&showempty=0&uk=' + self.share_uk[s_id] + '&web=1'
        header = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'BDCLND=' +  self.randsk[s_id],
            'Referer': 'https://pan.baidu.com/disk/home',
        }
        result = NTG_base.get(url, header, '', '')
        if result:
            result = json.loads(result['text'])
            if not (result['errno'] == 0 or result['errno'] == '0'):
                func_ui.showinfo('提示', '分享链接可能被和谐')
                return {'FailOrNot': False, 'ErrorMessage': '分享获取文件列表时出错', 'code': 46}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '分享获取文件列表时出错', 'code': 46}
        #分出dir和file
        dir_list = []
        file_list = []
        if isroot:
            #求出需要替换的部分
            f_path = len(result['list'][0]['path'])
            f_name = len(result['list'][0]['server_filename'])
            self.needpr[s_id] = f_path - f_name - 1
            #求完
        #开分
        for sg_fl in result['list']:
            if sg_fl['isdir'] == 0 or sg_fl['isdir'] == '0':     #文件
                
                haveExtInFile = '.' in sg_fl['server_filename']
                if haveExtInFile:
                    ext = sg_fl['server_filename'].split('.')[-1]
                else:
                    ext = ''
                temp = {
                    'name': sg_fl['server_filename'],
                    'time': str(sg_fl['server_mtime']),
                    'md5': sg_fl['md5'],
                    'path': sg_fl['path'],
                    'save_path': sg_fl['path'][self.needpr[s_id]:],
                    'fs_id': str(sg_fl['fs_id']),
                    'size': sg_fl['size'],
                    'category': ext,
                    'select': False,
                }
                file_list.append(temp)
            else:
                temp = {
                    'name': sg_fl['server_filename'],
                    'path': sg_fl['path'],
                    'time': str(sg_fl['server_mtime']),
                    'save_path': sg_fl['path'][self.needpr[s_id]:],
                    'fs_id': str(sg_fl['fs_id']),
                    'select': False,
                }
                dir_list.append(temp)
        self.TempList = {'FailOrNot': True, 'result': {'Dir': dir_list, 'File': file_list}, 'path': path}
        result = {
            'File': file_list,
            'Dir': dir_list,
            'needpr': self.needpr[s_id],
        }
        return result
        #下载/创建新任务
        #for i in file_list:
        #    ntc.Change('获取下载链接:\n' + i['name'])
        #    self.get_share_download_link(i['md5'], uk, share_uk, i['fs_id'], sign, logid, share_id, randsk, i['save_path'])
        #for i in dir_list:
        #    ntc.Change('创建新的文件树任务:\n' + i['name'])
        #    self.share_get_list(uk, share_id, False, needpr, i['name'], share_uk, sign, logid, randsk, ntc)

    def curve_salvation_get_sign(self, share_id, sign, share_uk, randsk, fs_id, time_stamp):
        '''
        !!!会导致黑号，已弃用，仅作为获取sign使用!!!

        获取下载链接，转json
        bdstoken isnoualink均为小文件传参，不适用
        uk为分享者的uk
        '''
        url = 'https://pan.baidu.com/api/sharedownload?app_id=250528&channel=chunlei&clienttype=12&sign=' + sign + '&timestamp=' + time_stamp + '&web=1'
        data = "encrypt=0&extra=" + quote('{"sekey":"' + quote(randsk) + '"}').replace('/','%2F').replace('25', '') + "&fid_list=%5B" + fs_id + "%5D&primaryid=" + share_id + "&uk=" + share_uk + "&product=share"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39",
    		"Cookie": self.Cookie,
    		"Referer": "https://pan.baidu.com/disk/home",
            'Hose': 'pan.baidu.com',
            'Accept': '*/*'
        }
        for i in range(5):
            result = NTG_base.post(url, header, data, '')
            if not result:
                continue
            result = result['text']
            server_time = str(json.loads(result)["server_time"])
            result = json.loads(result)['list'][0]['dlink']
            can_use = 'sign=' in result
            if can_use:
                temp = result.split('&')
                for i in temp:
                    is_sign = 'sign=' in i
                    if is_sign:
                        sign = i[5:].replace('FDTAER', 'FDtAERVJouK')
                return sign, server_time
            else:
                result = {'FailOrNot': False, 'ErrorMessage': '获取下载链接时出错', 'code': 47}

        return result


    def get_share_download_link(self, md5, share_uk, fs_id, sign, logid, share_id, randsk, uk, time_stamp, path):
        """
        分享获取下载链接
        """
        new_sign, server_time = self.curve_salvation_get_sign(share_id, sign, share_uk, randsk, fs_id, time_stamp)
        devuid = self.uid + '|0'
        url = 'http://d.pcs.baidu.com/rest/2.0/pcs/file?method=locatedownload'
        header = {
            'Host': 'd.pcs.baidu.com',
            'User-Agent': 'netdisk;7.16.1.11;PC;PC-Windows;10.0.19043;WindowsBaiduYunGuanJia',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.Cookie,
        }
        data = 'app_id=250528&check_blue=1&es=1&es1=1&clienttype=0&path=' + md5 + '&fid=' + share_uk + '-250528-' + fs_id + '&dstime=' + server_time + '&rt=sh&sign=' + new_sign + '&expires=8h&chkv=1&chkbd=0&chkpc=&dp-logid=' + logid + '&dp-callid=0&shareid=' + share_id + '&r=586722525&resvsflag=1-12-0-1-1-1&vuk=' + uk + '&file_type=0&version=2.2.91.26&channel=p2p-pc_2.0_pc_netdisk_default&apn_id=1_0&freeisp=0&queryfree=0&use=0&version_app=11.6.3&origin=dlna&ver=4.0&devuid=' + devuid + '&cuid=' + devuid + '&rand=' + self.rand1 + '&time=' + server_time + '&vip=0'
        result = NTG_base.post(url, header, data, '')['text']
        for i in range(5):
            try:
                link_list = []
                for i in json.loads(result)['urls']:
                    link_list.append(i['url'])
                if path[0] == '/':
                    path_real = Total_Seeting.Path + path
                else:
                    path_real = Total_Seeting.Path + '/' + path
                CORE_download.use_download_method(link_list, path_real.split('/')[-1], path_real,  
                                                    'netdisk;7.16.1.11;PC;PC-Windows;10.0.19043;WindowsBaiduYunGuanJia')
                return True
            except:
                continue
    
    def share_download_link_loop_thread(self, start_path, is_root, s_id):
        Tshare_down = threading.Thread(target=self.get_share_download_link_loop, args=(start_path, is_root, s_id))
        Tshare_down.start()

    def get_share_download_link_loop(self, start_path, is_root, s_id, start_path_len=False, ntc_id=False, count=False):
        """
        下载分享链接中某文件夹内所有文件

        根据输入的start_path来获取目录下的文件夹/子文件夹/文件
        in_loop是区分用户输入还是循环引用
        若为false，则为用户输入
        true时，输入的应为int，代替pr
        """
        #计算需要被替换掉的
        if not start_path_len:
            start_path_len = len(start_path)
        #task
        if not ntc_id:
            ntc_id = func_ui.add_task('正在处理', 'cycle', -1)
            count = len(self.share_task_id_loop)
            self.share_task_id_loop[count] = {}
            self.share_task_id_loop[count]['found'] = 1
            self.share_task_id_loop[count]['checked'] = 0
        #开始循环
        #   获取列表
        self.share_task_id_loop[count]['checked'] += 1
        lists = self.share_get_list(False, start_path, s_id)
        if lists:
            for sg_file in lists['File']:
                func_ui.manage_task(ntc_id, '正在新建下载任务' + sg_file['path'], 'cycle', -1)
                md5 = sg_file['md5']
                share_uk = self.share_uk[s_id]
                fs_id = sg_file['fs_id']
                sign = self.share_sign[s_id]
                logid = self.Logid[s_id]
                share_id = self.share_id[s_id]
                randsk = self.randsk[s_id]
                time_stamp = self.time_stamp[s_id]
                path = sg_file['path'][start_path_len:]
                uk = self.uk[s_id]
                func_ui.showinfo('', path + '\n' + sg_file['path'] + '\n' + str(start_path_len))
                self.get_share_download_link(md5, share_uk, fs_id, sign, logid, share_id, randsk, uk, time_stamp, path)
            for sg_dir in lists['Dir']:
                self.share_task_id_loop[count]['found'] += 1
                func_ui.manage_task(ntc_id, '正在解析' + sg_dir['path'], 'cycle', -1)
                self.get_share_download_link_loop(sg_dir['path'], False, s_id, start_path_len, ntc_id, count)
        if self.share_task_id_loop[count]['found'] == self.share_task_id_loop[count]['checked']:
            func_ui.delete_task(ntc_id)

    def share_save_loop_thread(self, start_path, ToPath, s_id, start_path_len=False, ntc_id=False, count=False, datas=False):
        Tshare_down = threading.Thread(target=self.get_share_save_loop, args=(start_path, ToPath, s_id, start_path_len, ntc_id, count, datas))
        Tshare_down.start()

    def get_share_save_loop(self, start_path, ToPath, s_id, start_path_len=False, ntc_id=False, count=False, datas=False):
        """
        保存分享链接内特定文件夹内所有文件
        
        根据输入的start_path来获取目录下的文件夹/子文件夹/文件
        in_loop是区分用户输入还是循环引用
        若为false，则为用户输入
        true时，输入的应为int，代替pr
        """
        
        #计算需要被替换掉的
        if not start_path_len:
            start_path_len = len(start_path)
        #task
        if not ntc_id:
            ntc_id = func_ui.add_task('正在处理', 'cycle', -1)
            count = len(self.share_task_id_loop)
            self.share_task_id_loop[count] = {}
            self.share_task_id_loop[count]['found'] = 1
            self.share_task_id_loop[count]['checked'] = 0
        #开始循环
        #   获取列表
        self.share_task_id_loop[count]['checked'] += 1
        if not datas:
            lists = self.share_get_list(False, start_path, s_id)
        else:
            lists = datas
        if lists:
            for sg_file in lists['File']:
                func_ui.manage_task(ntc_id, '正在保存' + sg_file['path'], 'cycle', -1)
                share_uk = self.share_uk[s_id]
                fs_id = sg_file['fs_id']
                logid = self.Logid[s_id]
                share_id = self.share_id[s_id]
                randsk = self.randsk[s_id]
                surl = self.surl[s_id - 1]
                path = sg_file['path'][start_path_len:]
                self.save(ToPath + '/' + path, fs_id, randsk, share_id, share_uk, logid, surl)
            for sg_dir in lists['Dir']:
                self.share_task_id_loop[count]['found'] += 1
                func_ui.manage_task(ntc_id, '正在解析' + sg_dir['path'], 'cycle', -1)
                self.creat_dir(NTG_base.get_back_path(ToPath + '/' + sg_dir['path'][start_path_len:]))
                self.get_share_save_loop(sg_dir['path'], ToPath, s_id, start_path_len, ntc_id, count)
        if self.share_task_id_loop[count]['found'] == self.share_task_id_loop[count]['checked']:
            func_ui.delete_task(ntc_id)

    def share_basic_inf(self, original_surl, pwd) -> int:
        """
        应用于初始化分享链接信息，返回s_id
        """
        ntc_id = func_ui.add_task('请稍后', 'cycle', -1)
        if original_surl == '':
            func_ui.delete_task(ntc_id)
            return False
        original_surl = func_other.ProcessLink(original_surl)
        self.surl.append(original_surl)
        self.pwd[len(self.surl)] = pwd
        self.time = str(int(time.time()))
        func_ui.manage_task(ntc_id, '获取参数 [1/4]', 'cycle', -1)
        self.randsk[len(self.surl)] = self.share_get_randsk(original_surl[1:], pwd)
        print(self.randsk[len(self.surl)])
        if not self.randsk[len(self.surl)]:
            self.randsk[len(self.surl)] = self.share_get_randsk(original_surl, pwd)
            if not self.randsk[len(self.surl)]:
                func_ui.delete_task(ntc_id)
                return False
        func_ui.manage_task(ntc_id, '获取参数 [2/4]', 'cycle', -1)
        self.share_sign[len(self.surl)] = self.share_get_sign(original_surl)
        if not self.share_sign[len(self.surl)]:
            self.share_sign[len(self.surl)] = self.share_get_sign(original_surl[1:])
            if not self.share_sign[len(self.surl)]:
                func_ui.delete_task(ntc_id)
                return False
        func_ui.manage_task(ntc_id, '获取参数 [3/4]', 'cycle', -1)
        temp = self.share_get_uk_share_id(original_surl, self.randsk[len(self.surl)])
        if not temp['FailOrNot']:
            temp = self.share_get_uk_share_id(original_surl[1:], self.randsk[len(self.surl)])
        self.uk[len(self.surl)] = temp['result']['Uk']
        self.share_uk[len(self.surl)] = temp['result']['share_Uk']
        self.share_id[len(self.surl)] = temp['result']['Share_Id']
        self.Logid[len(self.surl)] = self.share_get_log_id(self.share_id[len(self.surl)], self.share_sign[len(self.surl)], self.uk[len(self.surl)])
        func_ui.manage_task(ntc_id, '获取参数 [4/4]', 'cycle', -1)
        self.share_get_list(True, '/', len(self.surl))
        func_ui.delete_task(ntc_id)
        return len(self.surl)

    
    ###############################################################################
    #                           批量保存
    ###############################################################################

    def CreateDir(self, dir, BDstoken, Logid, randsk):
        """
        新建文件夹
        """
        url = 'https://pan.baidu.com/api/create?a=commit&channel=chunlei&web=1&app_id=250528&bdstoken=' + BDstoken + '&logid=' + base64.b64encode(Logid.encode()).decode() + '&clienttype=0'
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '45',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36",
    		"Cookie": self.Cookie + " ;BDCLND=" + randsk,
    		"Referer": "https://pan.baidu.com/disk/home?",
            'sec-ch-ua': '\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"92\"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        dir = dir.replace('//','/')
        data = 'path=' + quote(dir).replace('/', '%2F') + '&isdir=1&block_list=%5B%5D'
        result = NTG_base.post(url, header, data, '')['text']

    def api_save(self, ToPath, fs_id, Randsk, Share_Id, Share_Uk, Logid, Surl):
        ToPath += '/example.zip'
        self.save(ToPath, fs_id, Randsk, Share_Id, Share_Uk, Logid, Surl)
        func_ui.showinfo('', '保存完成')
        return {'FailOrNot': False}

    def save(self, SavePath, fs_id, Randsk, Share_Id, Share_Uk, Logid, Surl):
        '''
        将分享的文件保存至指定目录
        变量: fs_id, SavePath
        '''
        sekey = quote(Randsk).replace('25', '')
        url = 'https://pan.baidu.com/share/transfer?shareid=' + str(Share_Id) + '&from=' + str(Share_Uk) + '&sekey=' + sekey + '&ondup=newcopy&async=1&channel=chunlei&web=1&app_id=250528&bdstoken=' + self.BDstoken + '&logid=' + base64.b64encode(Logid.encode()).decode() + '&clienttype=0'
        header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '45',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36",
    		"Cookie": self.Cookie,
    		"Referer": "https://pan.baidu.com/s/" + Surl,
            'sec-ch-ua': '\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"92\"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        #前面变成//的地方都修复成/
        SavePath = NTG_base.get_back_path(SavePath.replace('//','/')).replace('//','/')
        if SavePath[-1] == '/' and SavePath != '/':
            SavePath = SavePath[:-1]
        if type(fs_id) == str:
            data = 'fsidlist=' + quote('[' + str(fs_id) + ']') + '&path=' + quote(SavePath).replace('/','%2F')
        else:
            data = 'fsidlist=' + quote(str(fs_id)) + '&path=' + quote(SavePath).replace('/','%2F')
        result = json.loads(NTG_base.post(url, header, data, '')['text'])
        print(result)
        return result['errno']

    def share_get_list_api(self, share_id, isroot, needpr, path, share_uk, randsk):
        if isroot:
            content = 'root=1'
        else:
            content = 'dir=' + quote(path).replace('/', '%2F')
        url = 'https://pan.baidu.com/share/list?app_id=250528&channel=chunlei&clienttype=0&desc=1&num=999&order=time&page=1&' + content + '&shareid=' + share_id + '&showempty=0&uk=' + share_uk + '&web=1'
        header = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.Cookie + '; BDCLND=' +  randsk,
            'Referer': 'https://pan.baidu.com/disk/home',
        }
        result = NTG_base.get(url, header, '', '')
        if result:
            result = json.loads(result['text'])
            if not (result['errno'] == 0 or result['errno'] == '0'):
                func_ui.showinfo('提示', '分享链接可能被和谐')
                return {'FailOrNot': False, 'ErrorMessage': '分享获取文件列表时出错', 'code': 46}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '分享获取文件列表时出错', 'code': 46}
        #分出dir和file
        dir_list = []
        file_list = []
        if isroot:
            #求出需要替换的部分
            f_path = len(result['list'][0]['path'])
            f_name = len(result['list'][0]['server_filename'])
            needpr = f_path - f_name - 1
            #求完
        #开分
        for sg_fl in result['list']:
            if sg_fl['isdir'] == 0 or sg_fl['isdir'] == '0':     #文件
                temp = {
                    'name': sg_fl['server_filename'],
                    'time': sg_fl['server_mtime'],
                    'md5': sg_fl['md5'],
                    'path': sg_fl['path'],
                    'save_path': sg_fl['path'][needpr:],
                    'fs_id': str(sg_fl['fs_id']),
                    'size': sg_fl['size'],
                }
                file_list.append(temp)
            else:
                temp = {
                    'name': sg_fl['path'],
                    'save_path': sg_fl['path'][needpr:],
                    'fs_id': str(sg_fl['fs_id']),
                }
                dir_list.append(temp)
        return {'FailOrNot': True, 'result': (dir_list, file_list, needpr)}

    def save_get_list(self, uk, share_id, isroot, needpr, path, share_uk, 
                    sign, logid, randsk, ntc_id, surl, pwd,
                    BDstoken, select_path, Logid):
        func_ui.manage_task(ntc_id, '正在保存文件 - 获取文件树:' + path, False, False)
        result = self.share_get_list_api(share_id, isroot, needpr, path, share_uk, randsk)
        if not result['FailOrNot']:
            return False
        else:
            dir_list, file_list, needpr = result['result']
        #下载/创建新任务
        if isroot == True:
            #尝试一波带走
            for i in dir_list:
                func_ui.manage_task(ntc_id, '正在保存文件 - 创建任务:' + i['name'], False, False)
                result = self.save(select_path + i['save_path'], i['fs_id'], randsk, share_id, share_uk, logid, surl)
                if result == 'error':
                    #不行就曲线救国
                    func_ui.manage_task(ntc_id, '正在批量保存文件 - 创建任务:' + i['name'], False, False)
                    if i['save_path'] != '/':
                        Cdir = select_path + i['save_path']
                        self.CreateDir(Cdir, BDstoken, Logid, randsk)
                    self.save_get_list(uk, share_id, False, needpr, i['name'], share_uk, 
                                        sign, logid, randsk, ntc_id, surl, pwd, BDstoken, select_path,
                                        Logid)
        else:
            for i in dir_list:
                func_ui.manage_task(ntc_id, '正在保存文件 - 创建任务:' + i['name'], False, False)
                if i['save_path'] != '/':
                    Cdir = select_path + i['save_path']
                    self.CreateDir(Cdir, BDstoken, Logid, randsk)
                self.save_get_list(uk, share_id, False, needpr, i['name'], share_uk, 
                                    sign, logid, randsk, ntc_id, surl, pwd, BDstoken, select_path,
                                    Logid)
        for i in file_list:
            func_ui.manage_task(ntc_id, '正在保存文件 - ' + i['name'], False, False)
            self.save(select_path + i['save_path'], i['fs_id'], randsk, share_id, share_uk, logid, surl)
        

    def share_start_save(self, surl, pwd, ToPath):
        Tsave = threading.Thread(target=self.share_start_save_thread, args= (surl, pwd, ToPath))
        Tsave.start()
        return {'FailOrNot': False}

    def share_start_save_thread(self, surl, pwd, ToPath):
        surl = func_other.ProcessLink(surl)
        ntc_id = func_ui.add_task('正在保存文件 - 前置准备', 'cycle', -1)
        func_ui.manage_task(ntc_id, '正在保存文件 - 前置准备 [1/4]', False, False)
        randsk = self.share_get_randsk(surl, pwd)
        if not randsk:
            func_ui.showerror('错误', '分享链接或提取码错误\n\n或需要验证码, 请重新分享文件')
            func_ui.delete_task(ntc_id)
            return False
        func_ui.manage_task(ntc_id, '正在保存文件 - 前置准备 [2/4]', False, False)
        sign = self.share_get_sign(surl)
        if not sign:
            func_ui.delete_task(ntc_id)
            func_ui.showerror('错误', '我们遇到错误，请重试\n获取sign时出错')
            return False
        func_ui.manage_task(ntc_id, '正在保存文件 - 前置准备 [3/4]', False, False)
        temp = self.share_get_uk_share_id(surl, randsk)
        if not temp['FailOrNot']:
            func_ui.delete_task(ntc_id)
            func_ui.showerror('错误', '我们遇到错误，请重试\n获取信息时出错')
            return False
        uk = temp['result']['Uk']
        share_uk = temp['result']['share_Uk']
        share_id = temp['result']['Share_Id']
        BDstoken = temp['result']['BDstoken']
        func_ui.manage_task(ntc_id, '正在保存文件 - 前置准备 [4/4]', False, False)
        Logid = self.share_get_log_id(share_id, sign, uk)
        if not Logid:
            func_ui.delete_task(ntc_id)
            func_ui.showerror('错误', '我们遇到错误，请重试\n获取logid时出错')
            return False
        func_ui.manage_task(ntc_id, '正在保存文件 - 获取文件树', False, False)
        self.save_get_list(uk, share_id, True, None, '/', share_uk, sign, Logid, randsk,
                        ntc_id, surl, pwd, BDstoken, ToPath, Logid)
        func_ui.delete_task(ntc_id)
        pass
    ###############################################################################
    #                           文件操作
    ###############################################################################


    def is_done(self, task_id, data):
        url = 'https://pan.baidu.com/share/taskquery?taskid=' + str(task_id) + '&channel=chunlei&web=1&app_id=250528&bdstoken=' + self.BDstoken + '&logid=' + base64.b64encode(self.LogID.encode()).decode() + '&clienttype=0'
        header = {
            'Accept': '*/*',
            "User-Agent": "netdisk",
            "Cookie": self.Cookie,
        }
        Result = NTG_base.post(url, header, data, '')
        if Result:
            Result = json.loads(Result['text'])
            if Result['errno'] == 0:
                if Result['status'] == 'success':
                    Result['progress'] = 100
                try:
                    return {'FailOrNot': True, 'result': {'status': Result['status'], 'percent': str(Result['progress'])}}
                except:
                    return {'FailOrNot': True, 'result': {'status': 'success', 'percent': '100'}}
            else:
                return {'FailOrNot': False, 'ErrorMessage': '查询失败' + str(Result['errno']), 'code': 61}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '查询失败\n\nServerErrorCode:' + str(Result['errno']), 'code': 62}

    def re_name(self, pathList, nameList):
        Url = 'https://pan.baidu.com/api/filemanager?opera=rename&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken=' + self.BDstoken + '&logid=' + base64.b64encode(self.LogID.encode()).decode() + '&clienttype=0'
        header = {
            'Accept': '*/*',
            "User-Agent": "netdisk",
            "Cookie": self.Cookie,
        }
        data = '['
        count = 1
        if type(pathList) != list:
            pathList = [str(pathList)]
            nameList = [str(nameList)]
        for i,r in zip(pathList, nameList):
            if count == len(pathList):
                data += '{\"path\":\"' + i + '\",\"newname\":\"' + r + '\"}]'
            else:
                data += '{\"path\":\"' + i + '\",\"newname\":\"' + r + '\"},'
            count += 1
        data = quote(data).replace('/','%2F')
        data = 'filelist=' + data
        Result = NTG_base.post(Url, header, data, '')
        if Result:
            Result = json.loads(Result['text'])
            if Result['errno'] == 0:
                return {'FailOrNot': True, 'result': {'data': data, 'task_id': Result['taskid']}}
            else:
                return {'FailOrNot': False, 'ErrorMessage': '文件无法重命名\n\nServerErrorCode:' + str(Result['errno']), 'code': 25}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '重命名时遇到意外错误\n\nServerErrorCode:' + str(Result['errno']), 'code': 24}

    def copy_file(self, pathList, nameList, ToPath):
        '''
        pathList:   源文件的路径，['/文件1', '/文件2']
        nameList:   源文件名称，['文件1', '文件']
        ToPath:     转移到哪里'/myresource/'
        '''
        Url = 'https://pan.baidu.com/api/filemanager?opera=copy&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken=' + self.BDstoken + '&logid=' + base64.b64encode(self.LogID.encode()).decode() + '&clienttype=0'
        header = {
            'Accept': '*/*',
            "User-Agent": "netdisk",
            "Cookie": self.Cookie,
        }
        data = '['
        count = 1
        for i,r in zip(pathList, nameList):
            if count == len(pathList):
                data += '{\"path\":\"' + i + '\",\"dest\":\"' + ToPath + '\",\"newname\":\"' + r + '\"}]'
            else:
                data += '{\"path\":\"' + i + '\",\"dest\":\"' + ToPath + '\",\"newname\":\"' + r + '\"},'
            count += 1
        data = quote(data).replace('/','%2F')
        data = 'filelist=' + data
        Result = NTG_base.post(Url, header, data, '')
        if Result:
            Result = json.loads(Result['text'])
            if Result['errno'] == 0:
                return {'FailOrNot': True, 'result': {'data': data, 'task_id': Result['taskid']}}
            else:
                return {'FailOrNot': False, 'ErrorMessage': '文件无法复制', 'code': 23}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '复制时遇到意外错误', 'code': 22}

    def move_file(self, pathList, nameList, ToPath):
        Url = 'https://pan.baidu.com/api/filemanager?opera=move&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken=' + self.BDstoken + '&logid=' + base64.b64encode(self.LogID.encode()).decode() + '&clienttype=0'
        header = {
            'Accept': '*/*',
            "User-Agent": "netdisk",
            "Cookie": self.Cookie,
        }
        data = '['
        count = 1
        for i,r in zip(pathList, nameList):
            if count == len(pathList):
                data += '{\"path\":\"' + i + '\",\"dest\":\"' + ToPath + '\",\"newname\":\"' + r + '\"}]'
            else:
                data += '{\"path\":\"' + i + '\",\"dest\":\"' + ToPath + '\",\"newname\":\"' + r + '\"},'
            count += 1
        data = quote(data).replace('/','%2F')
        
        data = 'filelist=' + data
        Result = NTG_base.post(Url, header, data, '')
        if Result:
            Result = json.loads(Result['text'])
            if Result['errno'] == 0:
                return {'FailOrNot': True, 'result': {'data': data, 'task_id': Result['taskid']}}
            else:
                return {'FailOrNot': False, 'ErrorMessage': '文件无法移动', 'code': 21}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '移动时遇到意外错误', 'code': 20}


    def delete_file(self, pathList):
        Url = 'https://pan.baidu.com/api/filemanager?opera=delete&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528&bdstoken=' + self.BDstoken + '&logid=' + base64.b64encode(self.LogID.encode()).decode() + '&clienttype=0'
        header = {
            'Accept': '*/*',
            "User-Agent": "netdisk",
            "Cookie": self.Cookie,
        }
        count = 1
        data = '['
        for i in pathList:
            if count == len(pathList):
                data += '\"' + i + '\"]'
            else:
                data += '\"' + i + '\",'
            count += 1
        data = quote(data).replace('/','%2F')
        data = 'filelist=' + data
        Result = NTG_base.post(Url, header, data, '')
        if Result:
            Result = json.loads(Result['text'])
            if Result['errno'] == 0:
                return {'FailOrNot': True, 'result': {'data': data, 'task_id': Result['taskid']}}
            else:
                return {'FailOrNot': False, 'ErrorMessage': '文件无法删除, 这可能是由于账号权限问题导致的\n若持续遇到此错误, 请重新登入账号, 并解开删除验证权限\n\nServerErrorCode:' + str(Result['errno']), 'code': 19}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '删除时遇到意外错误\n\nServerErrorCode:' + str(Result['errno']), 'code': 18}
    
    def creat_dir(self, path):
        url = 'https://pan.baidu.com/api/create?a=commit&channel=chunlei&web=1&app_id=250528&bdstoken=' + self.BDstoken + '&logid=' + base64.b64encode(self.LogID.encode()).decode() + '&clienttype=0'
        header = {
            'Accept': '*/*',
            "User-Agent": "netdisk",
            "Cookie": self.Cookie,
        }
        data = 'path=' + quote(path).replace('/','%2F') + '&isdir=1&block_list=%5B%5D'
        result = NTG_base.post(url, header, data, '')
        if result:
            result = json.loads(result['text'])
            if result['errno'] == 0:
                return {'FailOrNot': True}
            else:
                return {'FailOrNot': False, 'ErrorMessage': '创建文件夹时出错\n\nServerErrorCode:' + str(result['errno']), 'code': 32}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '服务器响应错误', 'code': 33}

    ##############################################
    #               对网盘信息的获取
    ##############################################
    
    def get_share_link(self, fs_id, Pwd):
        if type(fs_id) == list:

            fs_id = str(fs_id)
        else:
            fs_id = '[' + str(fs_id) + ']'
        Url = 'https://pan.baidu.com/share/set?channel=chunlei&clienttype=0&web=1&channel=chunlei&web=1&app_id=250528&bdstoken=' + self.BDstoken + '&logid=' + base64.b64encode(self.LogID.encode()).decode() + '&clienttype=0'
        data = 'channel_list=' + quote('[]') +'&period=30&pwd=' + str(Pwd) + '&schannel=4&fid_list=' + quote(fs_id).replace('/','%2F')
        header = {
            'Accept': '*/*',
            "User-Agent": "netdisk",
            "Cookie": self.Cookie,
        }
        Result = NTG_base.post(Url, header, data, '')
        if Result:
            Result = json.loads(Result['text'])
            if Result['errno'] == 0:
                self.Surl = func_other.ProcessLink(Result['link'])
                return {'FailOrNot': True, 'result': self.Surl}
            else:
                return {'FailOrNot': False, 'ErrorMessage': '此文件无法分享或提取码中有中文\n\nServerErrorCode:' + str(Result['errno']), 'code': 16}
        else:
            return {'FailOrNot': False, 'ErrorMessage': '分享失败', 'code': 17}


    
    def process_cookie(self):
        try:
            self.Stoken = re.search(r'STOKEN=(.+?);', str(self.Cookie))
            self.Stoken = self.Stoken.group(1)
            self.Bduss = re.search(r'BDUSS=(.+?);', str(self.Cookie))
            self.Bduss = self.Bduss.group(1)
            self.LogID = re.search(r'BAIDUID=(.+?);', str(self.Cookie))
            self.LogID = self.LogID.group(1)
            if self.Stoken == '' or self.Bduss == '' or self.LogID == '':
                return {'FailOrNot': False, 'ErrorMessage': '参数错误\n\nCookie无法被处理(Empty)', 'code': 6}
            else:
                return {'FailOrNot': True, 'result': {'Bduss': self.Bduss, 'Stoken': self.Stoken, 'LogID': self.LogID}, 'code': 6}
        except:
            return {'FailOrNot': False, 'ErrorMessage': '参数错误\n\nCookie无法被处理(正则表达式无法被执行)', 'code': 7}

    ##################################################
    #
    #                   UPLOAD
    #
    ##################################################

    def get_blocklist(self):
        url = 'https://nd-static.bdstatic.com/m-static/v20-main/js/chunk-1197e479.bf8a1bc6.js'
        header = {
            'authority': 'nd-static.bdstatic.com',
            'method': 'GET',
            'path': '/m-static/v20-main/js/chunk-1197e479.bf8a1bc6.js',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://pan.baidu.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30',
        }
        result = NTG_base.get(url, header, '', '')['text']
        self.blocklist = re.search(r'blockList=\'.*\]\'', str(result))
        self.blocklist = self.blocklist.group(0)
        if not self.blocklist:
            return False
        else:
            self.blocklist = self.blocklist.replace('blockList=\'[\"', '').replace('\"]\'', '')
            return self.blocklist
    
    def get_uploadID(self, ToPath, name):
        Path = quote(ToPath + name).replace('/', '%2F')
        ToPath = quote(ToPath).replace('/', '%2F')
        url = 'https://pan.baidu.com/api/precreate?clienttype=0&app_id=250528&web=1&dp-logid=90659200449625940032'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '153',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.Cookie,
            'Host': 'pan.baidu.com',
            'Origin': 'https://pan.baidu.com',
            'Pragma': 'no-cache',
            'Referer': 'https://pan.baidu.com/disk/main?from=homeFlow',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data = 'path=' + Path + '&autoinit=1&target_path=' + ToPath + '&block_list=%5B%22' + self.blocklist + '%22%5D&local_mtime=' + str(int(time.time()))
        result = NTG_base.post(url, header, data, '')['text']
        uploadid = json.loads(result)['uploadid']
        return uploadid
    
    def upload_file_thread(self, upload_path, name, file_path):
        upload_task = threading.Thread(target=self.upload_file, args=(upload_path, name, file_path))
        upload_task.start()
    
    def upload_file(self, upload_path, name, file_path):
        uploadid = self.get_uploadID(upload_path, name)
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.Cookie,
            'Host': 'pan.baidu.com',
            'Origin': 'https://pan.baidu.com',
            'Pragma': 'no-cache',
            'Referer': 'https://pan.baidu.com/disk/main',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77',
            'X-Requested-With': 'XMLHttpRequest',
        }
        #options and post file
        url = 'https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2?method=upload&app_id=250528&channel=chunlei&clienttype=0&web=1&logid={}&path={}&uploadid={}&uploadsign=0&partseq=0'.format(
            self.local_logid,
            NTG_base.url_quote(upload_path + '/' + name),
            uploadid
        )
        task = Upload(url, header, file_path, name, pre_option=True)
        task.go()
        #creat file
        dp_logid = self.gen_dp_logid()
        url = 'https://pan.baidu.com/api/create?isdir=0&rtype=1&bdstoken={}&clienttype=0&app_id=250528&web=1&dp-logid={}'.format(
            self.BDstoken,
            dp_logid
        )
        data = 'path={}&size={}&uploadid={}&target_path={}&block_list=%5B%22{}%22%5D&local_mtime={}'.format(
            NTG_base.url_quote(upload_path + '/' + name),
            str(os.path.getsize(file_path)),
            uploadid,
            NTG_base.url_quote(upload_path + '/'),
            self.blocklist,
            str(int(time.time()))
        )
        NTG_base.get(url, header, '', '')
        



if Total_Seeting.svip_cookie != '':
    try:
        Total_Seeting.svip_user = BaiDuCloud(Total_Seeting.svip_cookie)
        Total_Seeting.svip_user.start_get_basic_inf()
    except:
        pass

if __name__ == '__main__':
    user = BaiDuCloud('')
    print(user.get_blocklist())
    #user_temp = BaiDuCloud('BDUSS=m90a2tocEIwQWcxeEVqekhMRWllem9HN2lRd2kwdGdUY01WQkRIWUdDOUFRVmhpRVFBQUFBJCQAAAAAAAAAAAEAAACwBpxxYmFiecnqsMIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEC0MGJAtDBif; STOKEN=f08526b0fa4d01c8d05b9c60dc26022b447517625beeb290848f26af55407f85')
    #user_temp.start_get_basic_inf()
    #user_temp.share_start_download('1LkedIckXVkYgUMxL92ouKQ', '0000')
