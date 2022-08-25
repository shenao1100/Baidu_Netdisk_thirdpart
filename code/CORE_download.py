#-*-coding:utf-8-*-
import random
import threading
import requests
import urllib
import urllib.request
import json
import time
import os
from win10toast import ToastNotifier
from subprocess import call

import func_ui
import NTG_base
import Total_Seeting
##########################################
#               方式分配
##########################################
def use_download_method(url, name, path, UserAgent):

    if Total_Seeting.down_method == 'local':
        if type(url) == list:
            url = url[0]
        dtsk = Download(path, name, url, '', UserAgent)
        dtsk.start()
    elif Total_Seeting.down_method == 'local_mulit':
        if type(url) == list:
            url = url[0]                                                                                                                                                    
        path = path[:(len(path) - len(path.split('/')[-1]))]
        dtsk = MultDownload(path, name, url, '', UserAgent, Total_Seeting.down_thread)
        dtsk.start()
    elif Total_Seeting.down_method == 'aria2c':
        path = path[:(len(path) - len(path.split('/')[-1]))]
        dtsk = Aria2cDownload(url, path, name, UserAgent)
        dtsk.start()
    elif Total_Seeting.down_method == 'IDM':
        if type(url) == list:
            url = url[0]
        path = path[:(len(path) - len(path.split('/')[-1]))]
        if Total_Seeting.idm_path == '' or os.path.exists(Total_Seeting.idm_path) == False:
            func_ui.showwarning('警告', 'IDM路径不存在，请前往设置重新设置IDM的路径')
            return False
        call([Total_Seeting.idm_path, '/d', url, '/p', path, '/f', name])
##########################################
#               多线程
##########################################
class MultDownload(threading.Thread):
    Tasks = []
    downcount = 0
    def __init__(self, Path, Name, Url, Proxy, UserAgent, thread):
        threading.Thread.__init__(self)
        MultDownload.Tasks.append(self)
        self.Name = Name
        self.Path = Path
        self.Url = Url 
        self.Proxy = Proxy
        self.header = {
            'User-Agent': UserAgent,
        }
        self.Satus = 'Ready'
        self.Pause = False

        self.downloadedSize = 0
        self.TotalSize = 0
        self.Progress = 0
        self.Percent = 0
        self.speed = 0
        self.thread = thread

        self.thread_downsize_loop = []
        self.thread_downlen_loop = []
        self.thread_temppath_loop = {}
        self.thread_staus_loop = {}
        self.down_of_a_sec = 0

    def init_assign(self):
        for i in range(5):
            try:
                self.response = requests.get(self.Url, headers=self.header, proxies=self.Proxy, stream=True, verify=False)
                break
            except:
                continue
        self.chunk_size = 1024       # 每次下载的数据大小
        try:
            self.TotalSize = int(self.response.headers['content-length'])  # 下载文件总大小
        except:
            return False
        per_downsize = int(self.TotalSize / self.thread)
        count = 1
        while count < self.thread:
            count += 1
            self.thread_downsize_loop.append(per_downsize)
        self.thread_downsize_loop.append(self.TotalSize - (per_downsize * (self.thread - 1)))
        #0-500 501-1000.png 1001-end
        end_size = 0
        count = 0
        for sizes in self.thread_downsize_loop:
            if count == 0:
                self.thread_downlen_loop.append(str(end_size) + '-' + str(end_size + sizes))
                count += 1
            else:
                self.thread_downlen_loop.append(str(end_size + 1) + '-' + str(end_size + sizes))
            end_size += sizes
        return self.thread_downlen_loop
    
    def calculate_speed(self):
        while True:
            if self.Satus == 'Deleted' or self.Satus == 'Done':
                break
            else:
                time.sleep(1)
                self.speed = NTG_base.size(round(self.down_of_a_sec, 2))
                self.down_of_a_sec = 0

    def down_thread(self, area, path, id, length):
        downed_len = 0
        self.thread_staus_loop[id] = False
        self.thread_temppath_loop[id] = path
        header_down = self.header
        header_down['Range'] = 'bytes=' + area
        while True:
            try:
                response = requests.get(self.Url, headers=header_down, proxies=self.Proxy, stream=True, verify=False)
                break
            except:
                time.sleep(0.3)
                continue
        with open(path,'wb') as files:
            try:
                for data in response.iter_content(chunk_size=self.chunk_size):
                    if self.Satus == 'Deleted':
                        response.close()
                        return True
                    while self.Pause:
                        self.Satus = 'Pause'
                        time.sleep(1)
                    if self.Pause == False:
                        self.Satus = 'Download'
                        if self.Satus == 'Delete':
                            response.close()
                            return True
                        else:
                            try:
                                files.write(data)
                            except:
                                break
                            self.downloadedSize+= len(data)
                            self.down_of_a_sec += len(data)
                            downed_len += len(data)
                            self.Progress = round((self.downloadedSize / self.TotalSize), 4)
                            self.Percent = round(self.Progress * 100, 2)
            except:
                self.downloadedSize -= downed_len
                time.sleep(0.3)
                self.down_thread(area, path, id, length)
        if length == downed_len or length == downed_len + 1 or length == downed_len - 1:
            self.thread_staus_loop[id] = True
            return True
        else:
            self.downloadedSize -= downed_len
            time.sleep(0.3)
            self.down_thread(area, path, id, length)
    
    def complete_and_combine(self):
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)
        with open(os.path.join(self.Path, self.Name), 'ab') as target_file:
            thread_id = 0
            for i in self.thread_temppath_loop:
                thread_id += 1
                with open(self.thread_temppath_loop[thread_id], 'rb') as orig_file:
                    while True:
                        small_data = orig_file.read(1024)
                        if not small_data:
                            break
                        else:
                            target_file.write(small_data)
                os.remove(self.thread_temppath_loop[thread_id])
        self.Satus = 'Done'

    def run(self):
        Total_Seeting.multi_down_count += 1
        NTG_base.write_file('./data/mdc.dat', str(Total_Seeting.multi_down_count))
        initial = self.init_assign()
        if not initial:
            self.Satus = '错误: 连接不可用或被屏蔽'
            return False
        count = 0
        Tdown = threading.Thread(target=self.calculate_speed)
        Tdown.start()
        for i, l in zip(self.thread_downlen_loop, self.thread_downsize_loop):
            count += 1
            temp_path = os.path.join(Total_Seeting.temp_path, str(Total_Seeting.multi_down_count))
            if not os.path.exists(temp_path):
                try:
                    os.makedirs(temp_path)
                except:
                    None
            temp_path = os.path.join(Total_Seeting.temp_path, str(Total_Seeting.multi_down_count), i + '.tmp')
            Tdown = threading.Thread(target=self.down_thread, args=(i, temp_path, count, l))
            Tdown.start()
        while True:
            time.sleep(0.1)
            if len(self.thread_staus_loop) == self.thread:
                count = 0
                for i in self.thread_staus_loop:
                    if self.thread_staus_loop[i] == True:
                        count += 1
                        continue
                    else:
                        count = 0
                    #combine
                if count == self.thread:
                    break
        self.complete_and_combine()
        return True


    def delete_task(self):
        if self.Satus != 'Ready':
            try:
                os.remove(self.Path)
            except:
                self.Satus = 'Error'
        self.Path = ''
        self.Url = '' 
        self.Proxy = ''

        self.Satus = 'Deleted'
        self.Pause = True

        self.downloadedSize = 0
        self.TotalSize = 0
        self.Progress = 0
        self.Percent = 0
        self.speed = 0
        if self in MultDownload.Tasks:
            MultDownload.Tasks.remove(self)
        thread_id = 0
        try:
            for i in self.thread_temppath_loop:
                thread_id += 1
                while True:
                    try:
                        os.remove(self.thread_temppath_loop[thread_id])
                        break
                    except:
                        time.sleep(0.1)
                        continue
        except:
            return True
        return True
    
    def pause_task(self):
        self.Pause = True

    def start_task(self):
        self.Pause = False

    def get_status(self):
        haveExtInFile = '.' in self.Name
        if haveExtInFile:
            ext = self.Name.split('.')[-1]
        else:
            ext = ''
        result = {
            'Self': self,
            'Satus': self.Satus,
            'Pause': self.Pause,
            'Name': self.Name,
            'Progress': self.Progress,
            'Percent': str(self.Percent) + '%',
            'speed': self.speed,
            'ext': ext,
            'download': NTG_base.size(self.downloadedSize),
            'total': NTG_base.size(self.TotalSize),
        }
        return result
   

class Download(threading.Thread):
    Tasks = []
    def __init__(self, Path, Name, Url, Proxy, UserAgent):
        threading.Thread.__init__(self)
        Download.Tasks.append(self)
        self.Name = Name
        self.Path = Path
        self.Url = Url 
        self.Proxy = Proxy
        self.header = {
            'User-Agent': UserAgent,
        }
        self.Satus = 'Ready'
        self.Pause = False

        self.downloadedSize = 0
        self.TotalSize = 0
        self.Progress = 0
        self.Percent = 0
        self.speed = 0

    def run(self):
        temp_name_len = len(self.Path.split('/')[-1])
        if not os.path.exists(self.Path[:(len(self.Path) - temp_name_len)]):
            if self.Path[:(len(self.Path) - temp_name_len)][-1] == '/':
                os.makedirs(self.Path[:(len(self.Path) - temp_name_len - 1)])
            else:
                os.makedirs(self.Path[:(len(self.Path) - temp_name_len)])
        for i in range(5):
            try:
                self.response = requests.get(self.Url, headers=self.header, proxies=self.Proxy, stream=True, verify=False)
                break
            except:
                continue
        self.chunk_size = 1024       # 每次下载的数据大小
        self.TotalSize = int(self.response.headers['content-length'])  # 下载文件总大小
        timeStart = time.time()
        BeenDownload = 0
        if self.response.status_code == 200:         #判断是否响应
            if self.Path == '':
                return True
            with open(self.Path,'wb') as self.file:
                for self.data in self.response.iter_content(chunk_size=self.chunk_size):
                    if self.Satus == 'Deleted':
                        break
                    while self.Pause:
                        self.Satus = 'Pause'
                        time.sleep(1)
                    if self.Pause == False:
                        if (time.time() - timeStart) >= 1:
                            timeEnd = time.time()
                            nowDownload = self.downloadedSize
                            self.speed = NTG_base.size(round((nowDownload - BeenDownload) / (timeEnd - timeStart), 2))
                            timeStart = time.time()
                            BeenDownload = nowDownload
                        self.Satus = 'Download'
                        if self.Satus == 'Delete':
                            break
                        else:
                            try:
                                self.file.write(self.data)
                            except:
                                break
                            self.downloadedSize+= len(self.data)
                            self.Progress = round((self.downloadedSize / self.TotalSize), 4)
                            self.Percent = round(self.Progress * 100, 2)
                if self.Satus == 'Download':
                    self.Satus = 'Done'
                    if not self.Satus == 'Deleted' and self.downloadedSize == self.TotalSize:
                        notice(self.Name)
                        Download.Tasks.remove(self)                 
        else:
            self.Satus = '错误:服务器拒绝请求:' + str(self.response.status_code)

    def delete_task(self):
        if self.Satus != 'Ready':
            self.file.close()
            try:
                os.remove(self.Path)
            except:
                self.Satus = 'Error'
        self.Path = ''
        self.Url = '' 
        self.Proxy = ''

        self.Satus = 'Deleted'
        self.Pause = True

        self.downloadedSize = 0
        self.TotalSize = 0
        self.Progress = 0
        self.Percent = 0
        self.speed = 0
        Download.Tasks.remove(self)
        return True
    
    def pause_task(self):
        self.Pause = True

    def start_task(self):
        self.Pause = False

    def get_status(self):
        haveExtInFile = '.' in self.Name
        if haveExtInFile:
            ext = self.Name.split('.')[-1]
        else:
            ext = ''
        result = {
            'Self': self,
            'Satus': self.Satus,
            'Pause': self.Pause,
            'Name': self.Name,
            'Progress': self.Progress,
            'Percent': str(self.Percent) + '%',
            'speed': self.speed,
            'ext': ext,
            'download': NTG_base.size(self.downloadedSize),
            'total': NTG_base.size(self.TotalSize),
        }
        return result


#########################################
#               Aria2c方式
#########################################

class Aria2cDownload(threading.Thread):
    Tasks = []
    def __init__(self, url, path, name, UserAgent):
        threading.Thread.__init__(self)
        Aria2cDownload.Tasks.append(self)
        self.url = url
        self.path = path
        self.ua = UserAgent
        self.name = name
        self.Path = self.path + self.name
        self.taskID = False

        self.Satus = 'Ready'
        self.Pause = False
        self.Delete = False

        self.downloadedSize = 0
        self.TotalSize = 0
        self.Progress = 0
        self.Percent = 0
        self.speed = 0

    def add_file(self):
        if type(self.url) != list:
            self.url = [self.url]
        jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                           'method':'aria2.addUri',
                           'params':[self.url,
                           {'header':'User-Agent: ' + self.ua,
                           'max-connection-per-server': str(Total_Seeting.down_thread),
                           'max-concurrent-downloads': '100',
                           'dir': self.path,
                           'out': self.name}]})
        response = NTG_base.post(Total_Seeting.aria_RPC, '', jsonreq, '')['text']
        response = json.loads(response)
        TaskID = response['result']
        self.taskID = TaskID

    def get_down_staus(self):
        jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                          'method':'aria2.tellStatus',
                          'params':[self.taskID]})
        #jsonreq = bytes(jsonreq.encode())
        #c = urllib.request.urlopen('http://localhost:6800/jsonrpc', jsonreq)
        response = NTG_base.post(Total_Seeting.aria_RPC, '', jsonreq, '')['text']
        response = json.loads(response)
        #response = json.loads(c.read())
        #总大小
        self.TotalSize = int(response['result']['files'][0]['length'])
        self.speed = (NTG_base.size(response['result']['downloadSpeed']) + 
                    '[' + str(len(response['result']['files'][0]['uris'])) + ']')
        self.downloadedSize = int(response['result']['files'][0]['completedLength'])
        downstatus = response['result']['status']
        if self.downloadedSize == 0:
            self.Progress == 0.0000
        else:
            self.Progress = round((self.downloadedSize / self.TotalSize), 4)
        self.Percent = round(self.Progress * 100, 2)
        status = {
            'paused': 'Pause',
            'active': 'Download',
            'complete': 'Done',
        }
        self.Satus = status.get(downstatus, '错误:服务器拒绝请求')
        return 0


    def delete_task(self):
        self.url = ''
        self.path = ''
        self.Satus = 'Deleting'
        self.Pause = True
        self.Delete = True
        self.downloadedSize = 0
        self.TotalSize = 0
        self.Progress = 0
        self.Percent = 0
        self.speed = 0
        try:
            Aria2cDownload.Tasks.remove(self)
        except:
            return False
        if not self.taskID:
            return True
        jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                          'method':'aria2.remove',
                          'params':[self.taskID]})
        response = NTG_base.post(Total_Seeting.aria_RPC, '', jsonreq, '')['text']
        response = json.loads(response)
        os.remove(self.Path)
        os.remove(self.Path + '.aria2')
        self.Satus = 'Deleted'
        return response

    def pause_task(self):
        if not self.taskID or self.Satus == 'Done':
            return True
        self.Satus = 'Pauseing'
        self.Pause = True
        jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                          'method':'aria2.pause',
                          'params':[self.taskID]})
        response = NTG_base.post(Total_Seeting.aria_RPC, '', jsonreq, '')['text']
        response = json.loads(response)
        return response

    def start_task(self):
        if not self.taskID or self.Satus == 'Done':
            return True
        self.Satus = 'Starting'
        self.Pause = False
        jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                          'method':'aria2.unpause',
                          'params':[self.taskID]})
        response = NTG_base.post(Total_Seeting.aria_RPC, '', jsonreq, '')['text']
        response = json.loads(response)
        return response

    def get_status(self):
        haveExtInFile = '.' in self.name
        if haveExtInFile:
            ext = self.name.split('.')[-1]
        else:
            ext = ''
        if self.Pause == True and self.Satus != 'Pause':
            self.Satus = 'Pauseing'
        if self.Pause == False and self.Satus != 'Download':
            self.Satus = 'Starting'
        if self.Delete == True:
            self.Satus = 'Deleted'
        result = {
            'Self': self,
            'Satus': self.Satus,
            'Pause': self.Pause,
            'Name': self.name,
            'Progress': self.Progress,
            'Percent': str(self.Percent) + '%',
            'speed': self.speed,
            'ext': ext,
            'download': NTG_base.size(self.downloadedSize),
            'total': NTG_base.size(self.TotalSize),
        }
        return result

    def run(self):
        self.add_file()
        while True:
            self.get_down_staus()
            if self.Satus == 'Deleted':
                break
            if self.Satus == 'Done':
                notice(self.name)
                Aria2cDownload.Tasks.remove(self)
                break

##############################################
#               总操作
#############################################
def get_all():
    result = []
    for i in Download.Tasks:
        result.append(i.get_status())
    for i in Aria2cDownload.Tasks:
        result.append(i.get_status())
    for i in MultDownload.Tasks:
        result.append(i.get_status())
    return result

def pause_all_true():
    for task in get_all():
        task = task['Self']
        Taria2c = threading.Thread(target=task.pause_task, args = ())
        Taria2c.start()
        
    

def delete_all_true():
    for task in get_all():
        task = task['Self']
        Taria2c = threading.Thread(target=task.delete_task, args = ())
        Taria2c.start()
        
        

def start_all_true():
    for task in get_all():
        task = task['Self']
        Taria2c = threading.Thread(target=task.start_task, args = ())
        Taria2c.start()
        

def pause_all():
    Taria2c = threading.Thread(target=pause_all_true)
    Taria2c.start()
    

def delete_all():
    Taria2c = threading.Thread(target=delete_all_true)
    Taria2c.start()

def start_all():
    Taria2c = threading.Thread(target=start_all_true)
    Taria2c.start()

def notice(file_name):
    try:
        note = ToastNotifier()
        note.show_toast(title='下载完成',
                        msg = file_name + ' 已完成',
                        icon_path = './logo.ico',
                        duration = 3,
                        threaded=True)
        return True
    except:
        #这个包有问题，如果连续提示就会报错冲突，只能加个try
        return True

######################################################
#                   上传
######################################################

class UpLoad:
    def __init__(self, url, header, file_path) -> None:
        
        pass