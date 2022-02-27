# -*- coding: utf-8 -*-g
# @Time : 2020/12/30 1:39
# @Author : Blink_Leo
# @File : test_app.py
# @Software: PyCharm

import urllib.request, urllib.error  # 制定URL，获取网页数据
from bs4 import BeautifulSoup  # 网页解析，获取数据
import json

request = urllib.request.Request("http://127.0.0.1:5000/search_data")
html = ""

response = urllib.request.urlopen(request)
html = response.read().decode("utf-8")
html = json.loads(html)
print(type(html))
