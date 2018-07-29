import tkinter as tk
from PIL import Image, ImageTk
from get_ticket import main
import os


class Deal(object):
    def __init__(self):
        self.log_all = r'F:\work\work\python\抢了么\log_all.png'
        self.log_an = r'F:\work\work\python\抢了么\log_an.png'
        self.see = r'F:\work\work\python\抢了么\see.png'
        self.seen = r'F:\work\work\python\抢了么\seen.png'
        self.get_all = r'F:\work\work\python\抢了么\get_all.png'
        self.get_an = r'F:\work\work\python\抢了么\get_an.png'

    def login(self):
        pwd = password.get()
        user = username.get()
        cap = captcha.get()
        if main.Begin(None, None, None, None, None, None, None, None).login2(s=s, place=cap, password=pwd, username=user):
            root.destroy()
            os.system(os.path.abspath('get.py'))
        else:
            top = tk.Toplevel()
            top.geometry('200x100')
            top.title('密码错误')
            text = tk.Label(top, text='密码错误', font='20', bg='red')
            ok = tk.Button(top, text='OK', font='20', bg='green', command=top.destroy)
            text.place(bordermode='outside', x=50, y=25)
            ok.place(bordermode='outside', x=75, y=75)

    def check(self, pwd, user, cap):
        if (pwd == '123') | (user == '123') | (cap == '123'):
            return True
        else:
            return False


s = main.Begin(None, None, None, None, None, None, None, None).get_image()
root = tk.Tk()
win = root.geometry('1002x564')
root.iconbitmap(r'F:\work\bitbug_favicon.ico')
root.title('抢了么 登录')
canvas = tk.Canvas(win, height=564, width=1002, bg='red')
"""图片预加载"""
Deal =Deal()
image = Image.open(Deal.log_all)
background = ImageTk.PhotoImage(image)
image = Image.open(Deal.log_an)
log_an = ImageTk.PhotoImage(image)
canvas.create_image(1002/2, 564/2, image=background)  # 背景
"""输入框"""
username = tk.Entry(win, relief=tk.FLAT, font=15)
captcha = tk.Entry(win, font=15, relief=tk.FLAT)
captcha.insert(0, '1,2,3,4')
password = tk.Entry(win, show='*', font=15, relief=tk.FLAT)
"""登录按钮"""
button = tk.Button(win, image=log_an, command=Deal.login, relief=tk.FLAT)
"""显示"""
canvas.pack(padx=0, pady=0)
username.place(bordermode='outside', x=645, y=197)
password.place(bordermode='outside', x=645, y=276)
captcha.place(bordermode='outside', x=645, y=350)
button.place(bordermode='outside', x=628, y=424)
root.mainloop()
