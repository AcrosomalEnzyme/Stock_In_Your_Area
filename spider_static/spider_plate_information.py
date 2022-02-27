# -*- coding: utf-8 -*-g
# @Time : 2020/12/31 22:46
# @Author : Blink_Leo
# @File : spider_plate_information.py
# @Software: PyCharm

import pymysql
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import json
import decimal
from decimal import Decimal
import time

db = pymysql.connect(host='localhost', user='root', password='123', database='work')

cursor = db.cursor()


# 得到指定一个URL的网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # html = response.read().decode("gbk")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def get_plate():
    url = "https://flash-api.xuangubao.cn/api/plate/rank?field=core_avg_pcp&type=0"
    html = askURL(url)  # 保存获取到的网页源码
    html = json.loads(html)

    # context = decimal.getcontext()  # 获取decimal现在的上下文
    # context.rounding = decimal.ROUND_HALF_UP  # 修改rounding策略

    res = {}
    data = html['data']
    res['plate_up'] = [data[0], data[1], data[2], data[3], data[4],
                       data[5]]

    data.reverse()

    # print(type(data))
    res['plate_down'] = [data[0], data[1], data[2], data[3], data[4],
                         data[5]]

    return res

def get_plate_data():

    plate_code=get_plate()
    base_url="https://flash-api.xuangubao.cn/api/plate/data?fields=plate_id,plate_name,fund_flow,rise_count,fall_count,stay_count,limit_up_count,core_avg_pcp,core_avg_pcp_rank,core_avg_pcp_rank_change,top_n_stocks,bottom_n_stocks&plates="

    context = decimal.getcontext()  # 获取decimal现在的上下文
    context.rounding = decimal.ROUND_HALF_UP  # 修改rounding策略

    sql='''
        delete from plate_up
    '''
    db.ping(reconnect=True)
    cursor.execute(sql)
    # res = cursor.fetchall()
    db.commit()
    sql = '''
            delete from plate_down
        '''
    db.ping(reconnect=True)
    cursor.execute(sql)
    # res = cursor.fetchall()
    db.commit()

    j=1
    for i in plate_code['plate_up']:
        i=str(i)
        url=base_url+i
        html = askURL(url)  # 保存获取到的网页源码
        html = json.loads(html)

        id=str(j)

        plate_name=html['data'][i]['plate_name']

        plate_change_percent=html['data'][i]['core_avg_pcp']
        plate_change_percent = decimal.Decimal(plate_change_percent*100).quantize(decimal.Decimal("0.01"))
        plate_change_percent = str(plate_change_percent)
        plate_change_percent+="%"

        company_id = html['data'][i]['top_n_stocks']['items'][0]['symbol']
        company_id=company_id[:-3]

        company_change_percent=html['data'][i]['top_n_stocks']['items'][0]['change_percent']
        company_change_percent = decimal.Decimal(company_change_percent * 100).quantize(decimal.Decimal("0.01"))
        company_change_percent = str(company_change_percent)
        company_change_percent += "%"

        simple_name=html['data'][i]['top_n_stocks']['items'][0]['stock_chi_name']

        sql = '''
                    insert into plate_up values (%s,%s,%s,%s,%s,%s)
                '''
        db.ping(reconnect=True)
        cursor.execute(sql,[id,plate_name,company_id,simple_name,plate_change_percent,company_change_percent])
        # res = cursor.fetchall()
        db.commit()

        j+=1

    j=1
    for i in plate_code['plate_down']:
        i = str(i)
        url = base_url + i
        html = askURL(url)  # 保存获取到的网页源码
        html = json.loads(html)

        id = str(j)

        plate_name = html['data'][i]['plate_name']

        plate_change_percent = html['data'][i]['core_avg_pcp']
        plate_change_percent = decimal.Decimal(plate_change_percent * 100).quantize(decimal.Decimal("0.01"))
        plate_change_percent = str(plate_change_percent)
        plate_change_percent += "%"

        company_id = html['data'][i]['bottom_n_stocks']['items'][0]['symbol']
        company_id = company_id[:-3]

        company_change_percent = html['data'][i]['bottom_n_stocks']['items'][0]['change_percent']
        company_change_percent = decimal.Decimal(company_change_percent * 100).quantize(decimal.Decimal("0.01"))
        company_change_percent = str(company_change_percent)
        company_change_percent += "%"

        simple_name = html['data'][i]['bottom_n_stocks']['items'][0]['stock_chi_name']

        sql = '''
                    insert into plate_down values (%s,%s,%s,%s,%s,%s)
                '''
        db.ping(reconnect=True)
        cursor.execute(sql, [id, plate_name, company_id, simple_name, plate_change_percent, company_change_percent])
        # res = cursor.fetchall()
        db.commit()

        j += 1



