import json
import Total_Seeting
import NTG_base
class ClientTasks:
    def __init__(self, surl, file_ids=[], randsk='yGuRX50BRyfiACmUWN6ScMpLVRUucQnnXuT%2FwR9sY%2FU%3D') -> None:
        #self.url = Total_Seeting.flash_link
        #self.password = Total_Seeting.fl_password
        #self.token = Total_Seeting.fl_token


        self.url = 'http://127.0.0.1:8080/'
        self.password = '123456'
        self.token = '110'

        self.randsk = randsk
        self.file_ids = file_ids
        self.surl = surl
        self.task_id = None
        pass

    def start_task(self):
        url = self.url + 'pulltask'
        data = json.dumps(
            {
                'randsk': self.randsk,
                'surl': self.surl,
                'fs_id': self.file_ids,
                'password': self.password,
                'token': self.token
            }
        )
        result = NTG_base.post(url, '', data, '')
        self.task_id = json.loads(result['text'])['taskid']
        return self.task_id

    def get_link(self):
        url = self.url + 'getlink'
        data = json.dumps(
            {
                'fs_id': self.file_ids,
                'randsk': self.randsk,
                'password': self.password,
                'token': self.token,
                'taskid': self.task_id,
            }
        )
        result = NTG_base.post(url, '', data, '')['text']
        result = json.loads(result)
        return result

    def get_status(self):
        url = self.url + 'getprocess'
        data = json.dumps(
            {
                'fs_id': self.file_ids,
                'randsk': self.randsk,
                'password': self.password,
                'token': self.token,
                'taskid': self.task_id,
            }
        )
        result = NTG_base.post(url, '', data, '')['code']
        return result

    def test(self):
        header = {
            'User-Agent': 'BaiduDiskManager'
        }
        data = json.dumps(
            {
                'randsk': '',
                'surl': '',
                'fs_id': '',
                'data': '中文测试',
                'password': self.password,
                'token': self.token
            }
        )
        print(NTG_base.post(self.url + 'test', header, data, ''))
        return 0

def 
a = ClientTasks('', '')
a.test()
