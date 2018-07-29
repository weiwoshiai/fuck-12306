import wx


def say_hi():
    print('1')


# (1002, 564)
app = wx.App()
img = r'F:\work\work\python\12306\get_ticket\抢了么？\背景图.png'
bmp = wx.Image(img, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
frame = wx.Frame(None, title='没得', size=(1002, 564))
bitmap = wx.StaticBitmap(frame, -1, bmp, (0, 0))
frame.Show()
loadButton = wx.Button(frame, label='登录', pos=(100, 200), size=(100, 200))
app.MainLoop()
