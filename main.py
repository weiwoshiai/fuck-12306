from get_ticket import login
from get_ticket import check_ticket, prepare
import requests
import time


class Begin(object):
    def __init__(self, train, kind, Time, start, end, seatType, name, waite_time):
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

    def login2(self, username, password):
        login1 = login.Login(self.s, username=username, password=password)
        print(self.waite_time)
        self.s = login1.begin()
        return self.s

    def begin(self):
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
    name = '魏逸凡'  # input('输入乘车人姓名：多个乘客用","隔开')
    username = '17693212350'
    password = 'fan000000'
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
