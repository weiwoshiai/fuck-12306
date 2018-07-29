import json
from get_ticket import config


class Login(object):
    def __init__(self, s, username, password, place):
        self.place = place
        self.headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        self.proxies = {'http': '124.88.217.106:8080'}
        self.check_url = r'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.url = r'https://kyfw.12306.cn/otn/login/init'
        self.img_url = r'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=' \
                       r'sjrand&0.14019682864683347'
        self.login_url = r'https://kyfw.12306.cn/passport/web/login'
        self.uamau_url = r'https://kyfw.12306.cn/otn/uamauthclient'
        self.s = s
        self.data = {
            'answer': '',
            'login': 'E',
            'rand': 'sjrand'
        }
        self.pw_data = {
                'appid': 'otn',
                'password': password,
                'username': username
            }

    def begin(self):
        self.capcha_check()
        self.pw_us()
        self.check_tk()
        return self.s

    def capcha_check(self):  # 检验验证码
        place = self.place.split(',')
        placed = ''
        for i in place:
            j = config.date[i]
            placed = j + ',' + placed
        self.data['answer'] = placed[0:len(placed)-1]
        print(self.s.cookies)
        print(self.data)
        check_response = self.s.post(url=self.check_url, data=self.data, proxies=self.proxies, headers=self.headers)
        check = json.loads(check_response.text)
        if check['result_message'] != '验证码校验成功':
            print(check_response.text)
            exit(10)
        print('验证码校验成功')

    def pw_us(self):  # 账号密码登录
        pw_response = self.s.post(url=self.login_url, data=self.pw_data, headers=self.headers, proxies=self.proxies)
        login_check = json.loads(pw_response.text)
        if login_check['result_message'] != '登录成功':
            print(pw_response.text)
            return 0
        print('登录成功')

    def check_otn(self):  # 获取tk
        umtk_url = r'https://kyfw.12306.cn/passport/web/auth/uamtk'
        umtk_response = self.s.post(url=umtk_url, data={'appid': 'otn'}, headers=self.headers, proxies=self.proxies)
        umtk_check = json.loads(umtk_response.text)
        if umtk_check['result_message'] != '验证通过':
            print(umtk_response.text)
        print('验证通过')
        tk = umtk_response.json()['newapptk']
        return tk

    def check_tk(self):  # 检验tk
        tk = self.check_otn()
        uamau_response = self.s.post(url=self.uamau_url, data={'tk': tk}, headers=self.headers, proxies=self.proxies)
        if uamau_response.json()['result_message'] != '验证通过':
            print('tk检验失败')
            exit(5)
        print('获取成功')
