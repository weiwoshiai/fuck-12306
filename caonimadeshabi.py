import wx


def say_hi(event):
    print(password.GetValue())


class MyPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        bgk = r'F:\work\work\python\study\ui\抢了么？\背景图.png'
        ico = r'F:\work\work\python\study\ui\抢了么？\图标.ico'
        center = r'F:\work\work\python\study\ui\抢了么？\中心头像.png'

        to_bmp_image = wx.Image(bgk, wx.BITMAP_TYPE_PNG).ConvertToBitmap()  # 将图片转换成BMP格式
        self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))  # 导入图片
        a = wx.Image.GetAlphaBuffer(wx.Image(center))
        center = wx.Image(center, wx.BITMAP_TYPE_PNG).ConvertToBitmap()  # 将图片转换成BMP格式
        wx.StaticBitmap(self.bitmap, -1, center, (176, 123))  # 中心图片
        set_title = '抢了么'  # 设置头
        parent.SetTitle(set_title)
        icon = wx.Icon(ico, wx.BITMAP_TYPE_ICO)  # 设置图标
        parent.SetIcon(icon)
        label = wx.StaticText(self.bitmap, -1, 'hello', (359, 132))

    def login(self):
        password = wx.TextCtrl(self.bitmap, pos=(399, 132), size=(356, 89))
        username = wx.TextCtrl(self.bitmap, pos=(399, 232), size=(356, 89))
        button = wx.Button(self.bitmap, -1, label='登录', pos=(10, 10))
        button.Bind(wx.EVT_BUTTON, say_hi)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, 'Image', size=(1002, 564))
    my_panel = MyPanel(frame, -1)
    my_panel.login()
    frame.Show()  # 框架展示
    app.MainLoop()  # 事件循环
