#-*- coding:utf-8 -*-
#CREATER: ShenAo
#import qrcode
import requests
import urllib
import urllib3
import qrcode
import base64
import threading
from urllib.parse import quote
#功能性函数
#text content cookie
def get(url,header,data,proxy):
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.get(url=url, headers=header, data=data, proxies=proxy, verify=False, timeout=10)
        cookie_value = {}
        for key,value in response.cookies.items():  
            cookie_value[key] = value 
        return {
            'text':response.text, 
            'content': response.content, 
            'cookie': cookie_value, 
            'headers': response.headers,
            'code': response.status_code
        }
    except:
        return False


def post(url,header,data,proxy):
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.post(url=url, headers=header, data=data, proxies=proxy, verify=False)
        cookie_value = {}
        for key,value in response.cookies.items():  
            cookie_value[key] = value 
        return {
            'text':response.text, 
            'content': response.content, 
            'cookie': cookie_value, 
            'headers': response.headers,
            'code': response.status_code
        }
    except:
        return False

def put(url,header,data,proxy):
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.put(url=url, headers=header, data=data, proxies=proxy, verify=False)
        cookie_value = {}
        for key,value in response.cookies.items():  
            cookie_value[key] = value 
        return {
            'text':response.text, 
            'content': response.content, 
            'cookie': cookie_value, 
            'headers': response.headers,
            'code': response.status_code
        }
    except:
        return False

def option(url,header,data,proxy):
    requests.packages.urllib3.disable_warnings()
    try:
        response = requests.options(url=url, headers=header, data=data, proxies=proxy, verify=False)
        cookie_value = {}
        for key,value in response.cookies.items():  
            cookie_value[key] = value 
        return {
            'text':response.text, 
            'content': response.content, 
            'cookie': cookie_value, 
            'headers': response.headers,
            'code': response.status_code
        }
    except:
        return False
    
def getSubstr(input,start,end):
    #php中的setsubstr    获取在input中夹在start和end中间的文本
    find_num = input.find(start)
    result = input[find_num+len(start):]
    find_end_num = result.find(end)
    result = result[:find_end_num]
    return result

def strstr(input,fn):
    #php中的strstr      获取input中fn后的所有文本
    find_num = input.find(fn)
    result = input[find_num+len(fn):]
    return result

def strstr_front(input,fn):
    #获取input中fn前的所有文本
    find_num = input.find(fn)
    result = input[:find_num]
    return result

def read_file(path):
    with open(path) as fp:
        content = fp.read()
        try:
            content = base64.b64decode(content.encode()).decode()
            return content
        except:
            write_file(path, content)
            return content

def write_file(filepath,insert):
    filepath = filepath.replace('/','\\')
    insert = base64.b64encode(insert.encode()).decode()
    try:
        with open(filepath,'w',encoding='utf-8') as wf:
            wf.write(insert)
        return True
    except:
        return False

def urlencode(str) :
    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]

def byteOrBytes(size):
    if size == 1: return '字节'
    return '字节'

def size(size):
    times = 0
    size = int(size)
    while size > 1024:
        size /= 1024
        times += 1
    switch = {0: byteOrBytes(size),
            1 : 'KB',
            2 : 'MB',
            3 : 'GB',
            4 : 'TB',
            5 : 'EB',
            6 : 'ZB',
        }
    unit =  switch.get(times, '未知单位')
    fSize = '%.2f' % size
    if int(float(fSize)) == float(fSize):
        return str(int(float(fSize))) + unit
    return str(fSize) + unit

def get_back_path(input):
    if input != '/':
        temp_result = input[:(len(input) - len(input.split('/')[-1]) - 1)]
        if temp_result == '':
            temp_result = '/'
    else:
        temp_result = '/'
    temp_result = temp_result.replace('//','/')
    return temp_result

    
def make_qr(str, path):
    qr=qrcode.QRCode(
        version=4,  #生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M, #L:7% M:15% Q:25% H:30%
        box_size=10, #每个格子的像素大小
        border=2, #边框的格子宽度大小
    )
    qr.add_data(str)
    qr.make(fit = True)
    img = qr.make_image()
    img.save(path)
    return 0

def creat_thread(command, **kwarg):
    thread_start = threading.Thread(target=command, args=kwarg)
    thread_start.start()

def url_quote(insert):
    return quote(insert).replace('/', '%2F')