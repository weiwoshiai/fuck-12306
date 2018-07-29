from get_ticket import config
import re
import urllib.parse
import time


class Check_ticket(object):
    def __init__(self, s, Time, start, end, kind, train):
        self.proxies = {'http': '124.88.217.106:8080'}
        self.headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        self.find_url = r'https://ad.12306.cn/sdk/webservice/rest/appService/getAdAppInfo.json?placemen' \
                        r'tNo=0004&clientType=2&billMaterialsId=8e8aeaa663cd4db78f6da0e51a396d2c'
        self.user_url = r'https://kyfw.12306.cn/otn/login/checkUser'
        self.submit_url = r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        self.url = r'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        self.getpass_url = r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        self.time = Time
        self.start = start
        self.end = end
        self.kind = kind
        self.s = s
        self.train = train
        self.getpass_data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': '2a2e314a26b2b158ef646434bfab89e8'
            }

    def get_ticket_info(self):  # 获取车票信息
        Time = self.time
        start = self.start
        end = self.end
        kind = self.kind
        find_response = self.s.get(url=self.find_url, headers=self.headers, proxies=self.proxies)
        """进入查询界面"""
        if find_response.status_code != 200:
            print('查询界面获取失败')
            exit(5)
        started = config.data[start]
        ended = config.data[end]
        kinded = config.data[kind]
        where_url = r'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicket' \
                    r'DTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=%s' % (Time, started, ended, kinded)
        where_response = self.s.get(url=where_url, headers=self.headers, proxies=self.proxies)
        """进入查询结果界面"""
        info = where_response.json()
        ticket_info = info['data']['result']
        ticket_infoed = {}
        i = 0
        for ticket_name in ticket_info:
            ticket_infoed['%s' % i] = ticket_name.split('|')
            i = i+1
        user_response = self.s.post(url=self.user_url, headers=self.headers,
                                    data={'_json_att': ''}, proxies=self.proxies)
        """检查登录"""
        if user_response.status_code != 200:
            print('检查登录出错了')
            print(user_response.text)
            exit(5)
        print('检查登录成功')
        i = i-1
        while i != -1:
            if self.train in ticket_infoed['%s' % i]:
                ticket_info = ticket_infoed['%s' % i]
            i = i - 1
        """获取列车特码"""
        src_key = ticket_info[0]
        if src_key == '':
            print('该次列车不存在！')
            exit(1)
        src_key = urllib.parse.unquote(src_key)
        submit_data = {
            'back_train_date': str(time.localtime()[0])+'-'+str(time.localtime()[1])+'-'+str(time.localtime()[2]),
            'purpose_codes': kinded,
            'query_from_station_name': start,
            'query_to_station_name': end,
            'secretStr': src_key,
            'tour_flag': 'dc',
            'train_date': Time,
            'undefined': ''
        }
        """提交简单列车信息"""
        submit_response = self.s.post(url=self.submit_url, data=submit_data, headers=self.headers, proxies=self.proxies)
        if submit_response.json()['messages']:
            print(submit_response.text)
            print('请检查列车信息，以及起终点和列车号')
            exit(5)
        print(submit_response.text)
        print('提交列车简单信息成功')
        response = self.s.post(url=self.url, headers=self.headers, proxies=self.proxies, data={'_json_att': ''})
        """获取TOKEN"""
        text = response.text
        pat = re.compile(r'var globalRepeatSubmitToken = .+?;')
        REPEAT_SUBMIT_TOKEN = re.findall(string=text, pattern=pat)
        key_check_isChange = re.search(pattern="'key_check_isChange':'(.*?)'", string=text).group(1)
        REPEAT_SUBMIT_TOKEN = re.sub(string=REPEAT_SUBMIT_TOKEN[0], pattern=r'var globalRepeatSubmitToken = ', repl='')
        REPEAT_SUBMIT_TOKEN = re.sub(string=REPEAT_SUBMIT_TOKEN, pattern=';', repl='')
        REPEAT_SUBMIT_TOKEN = REPEAT_SUBMIT_TOKEN[1:len(REPEAT_SUBMIT_TOKEN)-1]
        self.getpass_data['REPEAT_SUBMIT_TOKEN'] = REPEAT_SUBMIT_TOKEN
        """获取乘客信息"""
        getpass_response = self.s.post(url=self.getpass_url, headers=self.headers,
                                       data=self.getpass_data, proxies=self.proxies)
        if getpass_response.status_code != 200:
            print('获取乘客信息失败')
            print(getpass_response.text)
            exit(5)
        taker = getpass_response.json()['data']['normal_passengers']
        print(getpass_response.text)
        return taker, ticket_info, REPEAT_SUBMIT_TOKEN, self.s, key_check_isChange
