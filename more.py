from PIL import Image
from get_ticket import main
import time
from threading import Thread
import os


class MyThread(Thread):
    def __init__(self, func, args):
        super().__init__()
        self.func = func
        self.args = args
        self.result = self.func(*self.args)

    def back_result(self):
        try:
            return self.result
        except Exception:
            return None


"""train=train, kind=kind, Time=Time, start=start, end=end, seatType=seatType,"""
""""name=name, username=username, password=password, waite_time=waite_time'"""
train = 'K7727'  # input('输入乘坐的班次：')
kind = '普通'  # input('输入票种：普通或者学生')
Time = '2018-07-28'  # input('输入时间：年-月-日')
start = '北京'  # input('输入起点：')
end = '天津'  # input('输入终点：')
seatType = '硬卧'  # input('输入座位类型：商务特等座，一等座，二等座，软卧，硬卧，硬座')
name = '***'  # input('输入乘车人姓名：多个乘客用","隔开')
username = ['***', '***']
password = ['***', '***']
waite_time = '0'  # input('输入抢票时间：年,月,日,时,分,秒。任意时间输入0')
info = [train, kind, Time, start, end, seatType, name, username, password, waite_time]
begin = main.Begin(train=train, kind=kind, Time=Time, start=start, end=end, seatType=seatType, name=name,
                   waite_time=waite_time)
thread = []
for i in range(0, 2):
    t = MyThread(func=begin.login2, args=(username[i], password[i]))
    thread.append(t)
for i in thread:
    i.start()
for i in thread:
    t = Thread(target=begin.begin(i.back_result()))
    thread[i] = t
for i in thread:
    i.start()




