import re
import requests

url = r'https://image.baidu.com/search/index?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=' \
      r'1&pv=&fm=rs1&word=%E4%B9%8C%E5%85%8B%E5%85%B0%E7%BE%8E%E5%A5%B3&oriquery=%E7%BE%8E%E5%A5%B3' \
      r'&ofr=%E7%BE%8E%E5%A5%B3&sensitive=80'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
response = requests.get(url=url, headers=headers)
pat = re.compile(r'<ul class="imglist"[\s\S]+?</ul>')
img = re.findall(pattern=pat, string=response.text)
with open('1.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
