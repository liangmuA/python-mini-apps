# 目标：爬取网页的排行榜信息
# 查看tiobe网站的合规协议：robots.txt
# 安装requests插件
# 编写python程序爬取数据

import requests
from lxml import html

# 定义url
url = "https://www.tiobe.com/tiobe-index/"

# 发送请求
requests.get(url) # 注意都是get请求

document = html.fromstring(requests.get(url).text)

# 获取表头
th_list = document.xpath("//*[@id='top20']/thead/tr/th/text()")
print(th_list)

# 获取表格行
tr_list = document.xpath("//*[@id='top20']/tbody/tr")
for tr in tr_list:
    print(tr.xpath("./td/text()"))