import tkinter as tk
from PIL import Image, ImageTk
import os


class Deal(object):
    def __init__(self):
        self.get_all = r'F:\work\work\python\抢了么\get_all.png'
        self.get_an = r'F:\work\work\python\抢了么\get_an.png'

    def get(self):
        kind1 = kind.get()
        start1 = start.get()
        end1 = end.get()
        name1 = name.get()
        number1 = number.get()
        Time1 = Time.get()

        if self.check(kind1, name1, start1):
            root.destroy()
            os.system(os.path.abspath('my.py'))
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


root = tk.Tk()
win = root.geometry('1002x564')
root.iconbitmap(r'F:\work\bitbug_favicon.ico')
root.title('抢了么 抢票')

canvas = tk.Canvas(win, height=564, width=1002, bg='red')
"""图片预加载"""
Deal =Deal()
image = Image.open(Deal.get_all)
background = ImageTk.PhotoImage(image)
image = Image.open(Deal.get_an)
log_an = ImageTk.PhotoImage(image)
canvas.create_image(1002/2, 564/2, image=background)  # 背景
"""输入框"""
number = tk.Entry(win, relief=tk.FLAT, font=15)
kind = tk.Entry(win, font=15, relief=tk.FLAT)

Time = tk.Entry(win, font=15, relief=tk.FLAT)
start = tk.Entry(win, font=15, width=10, relief=tk.FLAT)
end = tk.Entry(win, font=15, width=10, relief=tk.FLAT)
name = tk.Entry(win, font=15, relief=tk.FLAT)
"""抢票按钮"""
button = tk.Button(win, image=log_an, command=Deal.get, relief=tk.FLAT)
"""显示"""
canvas.pack(padx=0, pady=0)
number.place(bordermode='outside', x=223, y=90)
kind.place(bordermode='outside', x=223, y=188)
Time.place(bordermode='outside', x=223, y=281)
start.place(bordermode='outside', x=223, y=384)
end.place(bordermode='outside', x=369, y=384)
name.place(bordermode='outside', x=223, y=476)
button.place(bordermode='outside', x=527, y=348)
root.mainloop()
