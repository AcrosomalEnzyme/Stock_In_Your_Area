# -*- coding: utf-8 -*-g
# @Time : 2020/12/7 22:21
# @Author : Blink_Leo
# @File : spider_allcom.py
# @Software: PyCharm

import pymysql
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作

db = pymysql.connect(host='localhost', user='root', password='123', database='work')

cursor = db.cursor()

sql = '''
            insert into company_base values (%s,%s,%s,%s,%s)
        '''
place = "-1"


# 得到指定一个URL的网页内容
def askURL(url):
    # 模拟浏览器头部信息
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(baseurl):
    url = baseurl
    html = askURL(url)  # 保存获取到的网页源码

    # print(html)

    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")

    infor = soup.find_all('td')
    list = []

    for item in infor:
        list.append(item.string)
        # print(item.string)

    for i in range(0, 6):
        # print(list[i])
        del list[0]

    for item in range(len(list)):
        if item % 5 == 1:
            id = list[item]

        if item % 5 == 2:
            simple_name = list[item]

        if item % 5 == 3:
            name = list[item]

        if item % 5 == 4:
            eng_id = list[item]

            db.ping(reconnect=True)
            place = check_place(id)
            cursor.execute(sql, [id, simple_name, name, eng_id, place])
            db.commit()

    print("ok")

    return 0


def getData2(baseurl1, baseurl3):
    for x in range(2, 186):
        url = baseurl1 + str(x) + baseurl3
        html = askURL(url)  # 保存获取到的网页源码
        soup = BeautifulSoup(html, "html.parser")

        infor = soup.find_all('td')
        list = []

        for item in infor:
            list.append(item.string)
            # print(item.string)

        for i in range(0, 6):
            # print(list[i])
            del list[0]

        for item in range(len(list)):
            if item % 5 == 1:
                id = list[item]

            if item % 5 == 2:
                simple_name = list[item]

            if item % 5 == 3:
                name = list[item]

            if item % 5 == 4:
                eng_id = list[item]

                db.ping(reconnect=True)
                place = check_place(id)
                cursor.execute(sql, [id, simple_name, name, eng_id, place])
                db.commit()

        print(x)

    return 0


def main():
    baseurl = "http://www.yz21.org/stock/info/"

    baseurl1 = "http://www.yz21.org/stock/info/stocklist_"
    baseurl3 = ".html"

    # 1.爬取网页
    datalist = getData(baseurl)
    datalist = getData2(baseurl1, baseurl3)

    sql_change1 = '''
            update company_base set simple_name='青岛中程',name='青岛中资中程集团股份有限公司',eng_id='QDZC' where id='300208';
        '''
    sql_change2 = '''
            update company_base set simple_name='*ST舜喆B',name='广东舜喆(集团)股份有限公司',eng_id='STSZB' where id='200168';
        '''
    sql_change3 = '''
            update company_base set simple_name='昇兴股份',name='昇兴集团股份有限公司',eng_id='SXGF' where id='002752';
        '''
    db.ping(reconnect=True)
    cursor.execute(sql_change1)
    cursor.execute(sql_change2)
    cursor.execute(sql_change3)
    db.commit()


def check_place(id):
    place = ""
    one = id[0:1]
    three = id[0:3]
    if (one == "5" or one == "6" or one == "9"):
        place = "SS"
        return place
    else:
        if (
                three == "009" or three == "126" or three == "110" or three == "201" or three == "202" or three == "203" or three == "204"):
            place = "SS"
            return place
        else:
            place = "SZ"
            return place


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    print("爬取完毕！")
