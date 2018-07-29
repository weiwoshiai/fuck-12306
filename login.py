from PIL import Image
import os
import json


class Login(object):
    def __init__(self, s, username, password):
        self.headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        self.proxies = {'http': '124.88.217.106:8080'}
        self.check_url = r'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.url = r'https://kyfw.12306.cn/otn/login/init'
        self.img_url = r'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=' \
                       r'sjrand&0.14019682864683347'
        self.login_url = r'https://kyfw.12306.cn/passport/web/login'
        self.uamau_url = r'https://kyfw.12306.cn/otn/uamauthclient'
        self.data = {
            'answer': '',
            'login_site': 'E',
            'rand': 'sjrand'
            }
        self.s = s
        self.pw_data = {
                'appid': 'otn',
                'password': password,
                'username': username
            }

    def begin(self):
        self.get_image()
        print('1,1    2,1    3,1    4,1\n1,2    2,2    3,2    4,2')
        print('double place use "," to connect')
        place = input('please input the check place')
        self.capcha_check(place)
        self.pw_us()
        self.check_tk()
        return self.s

    def get_image(self):      # 获取验证码图片
        self.s.get(url=self.url, headers=self.headers)
        http_cookie = self.s.cookies
        captcha_response = self.s.get(self.img_url, cookies=http_cookie, headers=self.headers, proxies=self.proxies)
        with open('captcha.jpg', 'wb') as f:
            f.write(captcha_response.content)
        im = Image.open('captcha.jpg')
        im.show()
        im.close()

    def capcha_check(self, place):  # 检验验证码
        place = place.split(',')
        placed = ''
        for i in range(0, len(place)):
            if i % 2 == 0:
                placed = placed + str((int(place[i])-1) * 72+36)
            if i % 2 != 0:
                placed = placed + str((int(place[i])-1)*80+70)
            placed = placed + ','
        self.data['answer'] = placed[0:len(placed)-1]
        check_response = self.s.post(url=self.check_url, data=self.data, proxies=self.proxies, headers=self.headers)
        check = json.loads(check_response.text)
        if check['result_message'] != '验证码校验成功':
            print(check_response.text)
            self.get_image()
            print('1,1    2,1    3,1    4,1\n1,2    2,2    3,2    4,2')
            print('double place use "," to connect')
            place = input('please input the check place')
            self.capcha_check(place)
            return 0
        print('验证码校验成功')
        os.system('taskkill /f /im Microsoft.Photos.exe')

    def pw_us(self):  # 账号密码登录
        pw_response = self.s.post(url=self.login_url, data=self.pw_data, headers=self.headers, proxies=self.proxies)
        login_check = json.loads(pw_response.text)
        if login_check['result_message'] != '登录成功':
            print(pw_response.text)
            self.pw_data['username'] = input('重新输入账号')
            self.pw_data['password'] = input('重新输入密码')
            self.pw_us()
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
