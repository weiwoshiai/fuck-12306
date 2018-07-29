import re
from get_ticket import config
import selenium.webdriver as web


def begin(text):
    pat = re.compile(r'title=\".*?\" data=\".*?\"')
    data = re.findall(string=text, pattern=pat)
    for i in data:
        try:
            for j in i.split(' '):
                try:
                    key = re.search(pattern='title=\"(.*?)\"', string=j).group(1)
                except:
                    wor = re.search(pattern='data=\"(.*?)\"', string=j).group(1)
            print(key, wor)
            config.data[key] = wor
        except:
            pass
    return config.data


browser = web.PhantomJS()
browser.get('https://kyfw.12306.cn/otn/leftTicket/init')
a = ['#nav_list1', '#nav_list', '.cityflip', 'a.cityflip:nth-child(2)']
for i in range(3, 7):
    a.append(a[1]+str(i))
    a.append(a[2])
    a.append(a[3])
a[1] = '#nav_list2'
print(a)
browser.find_element_by_css_selector('#fromStationText').click()
text = browser.page_source
config.data = begin(text)
for css in a:
    browser.find_element_by_css_selector(css).click()
    text = browser.page_source
    config.data = begin(text)
    while css == 'a.cityflip:nth-child(2)':
        try:
            browser.find_element_by_css_selector(css).click()
            text = browser.page_source
            config.data = begin(text)
        except:
            break
browser.close()
a = str(config.data)
a = re.sub(pattern=',', repl=',\n', string=a)
with open('config,py', 'w', encoding='utf-8') as f:
    f.write(str(a))
