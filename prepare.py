import time
import re
import datetime
from get_ticket import config


class Oder(object):
    def __init__(self, s, taker, ticket_info, REPEAT_SUBMIT_TOKEN, key_check_isChange, date, seatType):
        self.proxies = {'http': '124.88.217.106:8080'}
        self.date = date
        self.seatType = config.data[seatType]
        self.REPEAT_SUBMIT_TOKEN = REPEAT_SUBMIT_TOKEN
        self.headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        self.query_url = r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=1531896755588&' \
                         r'tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=%s' % REPEAT_SUBMIT_TOKEN
        self.result_url = r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue'
        self.confirm_url = r'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        self.taker = taker
        self.s = s
        self.ticket_info = ticket_info
        self.oder_url = r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        self.submit_url = r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        self.oder_data = {
            '_json_att': "",
            'bed_level_order_num': '000000000000000000000000000000',
            'cancel_flag': 2,
            'oldPassengerStr': '',
            'passengerTicketStr': '',
            'randCode': "",
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN,
            'tour_flag': 'dc',
            'whatsSelect': 1
        }
        self.submit_data = {
            '_json_att': '',
            'fromStationTelecode': self.ticket_info[4],
            'leftTicket': self.ticket_info[12],
            'purpose_codes': '00',
            "REPEAT_SUBMIT_TOKEN": REPEAT_SUBMIT_TOKEN,
            'seatType': self.seatType,
            'stationTrainCode': self.ticket_info[3],
            'toStationTelecode': self.ticket_info[5],
            'train_date': '',
            'train_location': self.ticket_info[15],
            'train_no': self.ticket_info[2],
            }
        self.confirm_data = {
            '_json_att': '',
            'choose_seats': '',
            'dwAll': 'N',
            'key_check_isChange': key_check_isChange,
            'leftTicketStr': self.ticket_info[12],
            'oldPassengerStr': '',
            'passengerTicketStr': '',
            'purpose_codes': '00',
            'randCode': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN,
            'roomType': '00',
            'seatDetailType': '000',
            'train_location': self.ticket_info[15],
            'whatsSelect': '1'
        }
        self.result_data = {
            '_json_att': '',
            'orderSequence_no': 'E566808738',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
        }

    def passenger(self):
        """data准备"""
        oldPassengerStr = ''
        passengerTicketStr = ''
        for i in range(0, len(self.taker)):
            oldPassengerStr = self.taker[i]['passenger_name']+','+'1' + ',' + \
                              self.taker[i]['passenger_id_no']+','+self.taker[i]['passenger_type']+'_'+oldPassengerStr
            passengerTicketStr = self.seatType+',0,'+self.taker[i]['passenger_type']+','+self.taker[i]['passenger_name']
            passengerTicketStr = passengerTicketStr+',1,' + self.taker[i]['passenger_id_no']+','
            passengerTicketStr = passengerTicketStr+self.taker[i]['mobile_no']+',N'+passengerTicketStr
        date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.date, '%Y-%m-%d')))\
            .strftime('%a %b %d %Y %H:%M:%S GMT+0800')
        self.submit_data['train_date'] = date
        self.oder_data['oldPassengerStr'] = oldPassengerStr
        self.oder_data['passengerTicketStr'] = passengerTicketStr
        self.confirm_data['oldPassengerStr'] = oldPassengerStr
        self.confirm_data['passengerTicketStr'] = passengerTicketStr

    def oder(self):
        self.passenger()
        order_response = self.s.post(url=self.oder_url, headers=self.headers, data=self.oder_data, proxies=self.proxies)
        """提交乘客信息"""
        if order_response.status_code != 200:
            print(order_response.text)
            exit(5)
        print('提交乘客信息成功')
        print(order_response.text)
        submit_response = self.s.post(url=self.submit_url, headers=self.headers,
                                      data=self.submit_data, proxies=self.proxies)
        """提交列车信息"""
        if submit_response.status_code != 200:
            print(submit_response.text)
            exit(5)
        print('提交列车信息成功')
        print(submit_response.text)
        print(self.confirm_data)
        confirm_response = self.s.post(url=self.confirm_url, data=self.confirm_data,
                                       headers=self.headers, proxies=self.proxies)
        """提交订单"""
        if confirm_response.status_code != 200:
            print('提交订单失败')
            print(confirm_response.text)
            exit(5)
        print(confirm_response.text)
        query_response = self.s.post(
            url=re.sub(pattern='1531896755588', string=self.query_url, repl=str(int(time.time() * 1000))),
            headers=self.headers, proxies=self.proxies)
        """排队获取订单信息"""
        if query_response.status_code != 200:
            print('检验订单失败')
            print(query_response.text)
            exit(5)
        print(query_response.json()['data'])
        print(self.result_data)
        print(self.confirm_data)
        print(self.oder_data)
        print(self.submit_data)
        while not query_response.json()['data']['orderId']:
            self.query_url = r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=%s&' \
                             r'tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=%s' % (str(int(time.time() * 1000)),
                                                                                 self.REPEAT_SUBMIT_TOKEN)
            query_response = self.s.post(url=self.query_url, headers=self.headers, proxies=self.proxies)
            print(query_response.json()['data'])
            time.sleep(3)
        self.result_data['orderSequence_no'] = query_response.json()['data']['orderId']
        result_response = self.s.post(url=self.result_url, data=self.result_data,
                                      headers=self.headers, proxies=self.proxies)
        """获取订单信息"""
        if result_response.status_code != 200:
            print('出票检验失败')
            print(result_response.text)
            exit(5)
        print('出票成功')
        print(result_response.text)
