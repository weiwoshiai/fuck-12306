from get_ticket import login
from get_ticket import check_ticket, prepare
import requests
import time
import tkinter as tk
from PIL import ImageTk, Image
import json


class Begin(object):
    def __init__(self, train, kind, Time, start, end, seatType, name, waite_time):
        self.headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        self.proxies = {'http': '124.88.217.106:8080'}
        self.url = r'https://kyfw.12306.cn/otn/login/init'
        self.img_url = r'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=' \
                       r'sjrand&0.14019682864683347'
        self.check_url = r'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.waite_time = waite_time
        self.train = train
        self.kind = kind
        self.Time = Time
        self.start = start
        self.end = end
        self.seatType = seatType
        self.name = name
        self.s = requests.Session()
        self.taker = {}

    def get_image(self):      # 获取验证码图片
        self.s.get(url=self.url, headers=self.headers)
        http_cookie = self.s.cookies
        print(http_cookie)
        captcha_response = self.s.get(self.img_url, cookies=http_cookie, headers=self.headers, proxies=self.proxies)
        with open('captcha.jpg', 'wb') as f:
            f.write(captcha_response.content)
        top = tk.Tk()
        win = top.geometry('293x190')
        canvas = tk.Canvas(top, height=190, width=293, bg='red')
        image = Image.open('captcha.jpg')
        image = ImageTk.PhotoImage(image)
        canvas.create_image(296/2, 190/2, image=image)
        canvas.pack()
        top.mainloop()
        return self.s

    def login2(self, username, password, place, s):  # 账号密码登录
        login1 = login.Login(s=s, username=username, password=password, place=place)
        self.s = login1.begin()
        return self.s

    def begin(self):  # 主菜单启动
        if self.waite_time != '0':
            self.waite_time = int(time.mktime(self.waite_time))
            if self.waite_time:
                while int(time.time()) != self.waite_time:
                    time.sleep(1)
                    print(time.time())
        check_ticket1 = check_ticket.Check_ticket(s=self.s, Time=self.Time, start=self.start, end=self.end,
                                                  kind=self.kind, train=self.train)
        self.taker, tickect_info, REPEAT_SUBMIT_TOKEN, self.s, key_check_isChange = check_ticket1.get_ticket_info()
        taker = self.passenger_deal()
        prepare.Oder(taker=taker, ticket_info=tickect_info, s=self.s,
                     REPEAT_SUBMIT_TOKEN=REPEAT_SUBMIT_TOKEN, key_check_isChange=key_check_isChange,
                     date=self.Time, seatType=self.seatType).oder()

    def passenger_deal(self):
        passenger_info = []
        passenger = self.name.split('，')
        for i in range(0, len(self.taker)):
            for j in range(0, len(passenger)):
                if passenger[j] == self.taker[i]['passenger_name']:
                    passenger_info.append(self.taker[i])
        return passenger_info


if __name__ == '__main__':
    train = 'G8004'  # input('输入乘坐的班次：')
    kind = '普通'  # input('输入票种：普通或者学生')
    Time = '2018-08-09'  # input('输入时间：年-月-日')
    start = '吉林'  # input('输入起点：')
    end = '长春'  # input('输入终点：')
    seatType = '二等座'  # input('输入座位类型：商务特等座，一等座，二等座，软卧，硬卧，硬座')
    name = '王梓旭'  # input('输入乘车人姓名：多个乘客用","隔开')
    username = '15943049458'
    password = 'wangzx1107'
    waite_time = '0'  # input('输入抢票时间：年,月,日,时,分,秒。任意时间输入0')
    if waite_time != '0':
        waite_time = waite_time.split(',')
        for i in range(0, len(waite_time)):
            waite_time[i] = int(waite_time[i])
        waite_time = tuple(waite_time)
    object_begin = Begin(train=train, kind=kind, Time=Time, start=start, end=end, seatType=seatType,
                         name=name, waite_time=waite_time)
    object_begin.login2(username=username, password=password)
    object_begin.begin()
