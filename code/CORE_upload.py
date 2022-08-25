#-*-coding:utf-8-*-
import random
import threading
import requests
from requests_toolbelt.multipart import encoder
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

class Upload:
    def __init__(self, url, header, file_path, name, pre_option=False, option_url=False) -> None:
        self.url = url
        self.option_url = option_url
        self.header = header
        self.file_path = file_path
        self.file_name = name
        self.pre_option = pre_option
        self.proxy = {
            #'http': '127.0.0.1:8888',
            #'https': '127.0.0.1:8888',
        }

        self.file_size = os.path.getsize(file_path)
        self.upload_size = 0
        pass
    
    def my_callback(self, monitor):
        # Your callback function
        print(self.upload_size)
        self.upload_size = monitor.bytes_read
        pass
    
    def close(self):
        self.process.close()
        

    def go(self):
        
        if self.pre_option:
            option_header = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
                'Access-Control-Request-Method': 'POST',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': 'c3.pcs.baidu.com',
                'Origin': 'https://pan.baidu.com',
                'Pragma': 'no-cache',
                'Referer': 'https://pan.baidu.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77',
            }
            print(NTG_base.option(self.url, option_header, '', self.proxy))
        self.header['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundaryRyIJMAdwAYGKNyDt'
        file_encoder = encoder.MultipartEncoder(
            fields={#'------WebKitFormBoundaryRyIJMAdwAYGKNyDt'
                #'Content-Disposition': 'form-data',
                #'name': "file",
                #'filename': "blob",
                #'Content-Type': '',
                'file': ('blob', open(self.file_path, 'rb'), 'application/octet-stream')},
                boundary='------WebKitFormBoundaryRyIJMAdwAYGKNyDt'
            )
        datas = encoder.MultipartEncoderMonitor(file_encoder, self.my_callback)
        self.process = requests.post(self.url, data=datas, headers=self.header, proxies=self.proxy, verify=False)
        print(self.process.text)

if __name__ == '__main__':
    a = Upload(
        'https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2?method=upload&app_id=250528&channel=chunlei&clienttype=0&web=1&logid=MTY1OTMzMjc0Njk2NjAuOTM4Nzk5NTkwNDcyOTAzNA==&path=%2FUI2.exe&uploadid=P1-MTAuMjI5LjIxNS40NToxNjU5MzMyNzU3OjMxODQ5NTYyNTgxMTU4MzkwMQ==&uploadsign=0&partseq=0',
        {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryRyIJMAdwAYGKNyDt',
            'Cookie': 'BIDUPSID=7F097D35F6A1126EEC213FF7458F52CE; PSTM=1647855221; BDUSS=EQwbzRibFdoVmpaWHEwWXRtUUdkb1BRWnRNbC1pYlcwdUU2T1FmVjB5U1ZYV1ppRVFBQUFBJCQAAAAAAAAAAAEAAACwBpxxYmFiecnqsMIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJXQPmKV0D5iS; BDUSS_BFESS=EQwbzRibFdoVmpaWHEwWXRtUUdkb1BRWnRNbC1pYlcwdUU2T1FmVjB5U1ZYV1ppRVFBQUFBJCQAAAAAAAAAAAEAAACwBpxxYmFiecnqsMIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJXQPmKV0D5iS; MCITY=-332%3A; BAIDUID=C23A1262696D2ECDD061FCDF32548991:FG=1; ZFY=B:BXhaZ7WOmGi8fSo7bZ3ltzf6syZo:BzZzWSvH22HncE:C; BAIDUID_BFESS=C23A1262696D2ECDD061FCDF32548991:FG=1; BAIDU_WISE_UID=wapp_1658928679549_98; newlogin=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; __yjs_duid=1_a4ee59ab7d54ef5e44711ed9b1c9d6531659238242646; STOKEN=758f078b929caef39ca87b0415351e70e8b3b3671467cf09b61b317598cdd54a; pcsett=1659419146-68f480c97eac637a24ad46634889d0aa; ab_sr=1.0.1_NDcxOTcxNDExMWFmOWFmMGQ3NDU2YTU1MmIzOWVmMzFhOWI3YzljM2QxOGQ1NWI2YzNmODU3OWU3ODUyNDYzMTRkYzIxY2JjNjRhYTRjMmVkYzk3YTdlYTZhODc5MWQ0YmJmOWEzZDE1NjhlOTQzZjQ4MzI4OTkxZmRhODA5YTIzZGIyNzlmMGZiNzZlMTk3NDhiZWNlYzA5MDZmNWYzOA==',
            'Host': 'c3.pcs.baidu.com',
            'Origin': 'https://pan.baidu.com',
            'Pragma': 'no-cache',
            'Referer': 'https://pan.baidu.com/',
            'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77',
        },
        'D:\\bili2.py',
        'UI2.exe',
        True
    )
    a.go()