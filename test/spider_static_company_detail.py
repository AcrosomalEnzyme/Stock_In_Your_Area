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
import json
import decimal
from decimal import Decimal
import time


db = pymysql.connect(host='localhost', user='root', password='123', database='work')

cursor = db.cursor()


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

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


def getData_init(id,place,simple_name):
    key = id + "." + place
    url="https://api-ddc-wscn.xuangubao.cn/market/real?fields=prod_name,trade_status,update_time,last_px,px_change,px_change_rate,preclose_px,open_px,high_px,low_px,amplitude,turnover_ratio,pe_rate,dyn_pe,dyn_pb_rate,market_value,circulation_value,turnover_volume,turnover_value,hq_type_code,securities_type,volume_ratio,circulation_shares,total_shares,bps&prod_code="+key

    html = askURL(url)  # 保存获取到的网页源码

    html = json.loads(html)

    context = decimal.getcontext()  # 获取decimal现在的上下文
    context.rounding = decimal.ROUND_HALF_UP  # 修改rounding策略


    if(html['data']['snapshot']=={}):

        trade_status = "已退市"
        sql = '''
                insert into company_detail values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''

        cursor.execute(sql, [id, simple_name, trade_status, "", "", "", "",
                             "", "", "", "", "", "", "",
                             "", "", "", "", "",
                             "", "", "", "", ""])
        db.commit()
        print(id)

        return 0

    # print("ok")

    # 股票代码
    id=id

    # 股票简称
    # simple_name=html['data']['snapshot'][key][0]
    # print(simple_name)

    # 交易状态
    trade_status=html['data']['snapshot'][key][1]
    if trade_status=="BREAK":
        trade_status="已休市"
    elif trade_status=="HALT":
        trade_status="停牌中"
    else:
        trade_status="已开盘"
    # print(trade_status)

    # 更新时间
    # time_=html['data']['snapshot'][key][2]
    # time_=str(time_)
    # update_time=time_[0]+time_[1]+":"+time_[2]+time_[3]
    update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(update_time)

    # 股价
    price_tem=html['data']['snapshot'][key][3]
    price_tem=str(price_tem)
    # print(price_tem)

    # 涨跌值
    change_=decimal.Decimal(html['data']['snapshot'][key][4]).quantize(decimal.Decimal("0.01"))
    change_=str(change_)
    # print(change_)


    # 涨跌百分比
    change_percent=decimal.Decimal(html['data']['snapshot'][key][5]).quantize(decimal.Decimal("0.01"))
    change_percent=str(change_percent)
    change_percent=change_percent+"%"
    # print(change_percent)

    # 昨日收盘价
    closing_price=decimal.Decimal(html['data']['snapshot'][key][6]).quantize(decimal.Decimal("0.01"))
    closing_price=str(closing_price)
    # print(closing_price)

    # 今日开盘价
    opening_price=decimal.Decimal(html['data']['snapshot'][key][7]).quantize(decimal.Decimal("0.01"))
    opening_price=str(opening_price)
    # print(opening_price)

    # 今日最高价
    highest=decimal.Decimal(html['data']['snapshot'][key][8]).quantize(decimal.Decimal("0.01"))
    highest=str(highest)
    # print(highest)

    # 今日最低价
    lowest=decimal.Decimal(html['data']['snapshot'][key][9]).quantize(decimal.Decimal("0.01"))
    lowest=str(lowest)
    # print(lowest)

    # 振幅
    amplitude=decimal.Decimal(html['data']['snapshot'][key][10]).quantize(decimal.Decimal("0.01"))
    amplitude=str(amplitude)
    amplitude = amplitude + "%"
    # print(amplitude)

    # 换手率
    turnover_ratio=decimal.Decimal(html['data']['snapshot'][key][11]).quantize(decimal.Decimal("0.01"))
    turnover_ratio=str(turnover_ratio)
    turnover_ratio = turnover_ratio + "%"
    # print(turnover_ratio)

    # 市盈率
    PER=decimal.Decimal(html['data']['snapshot'][key][12]).quantize(decimal.Decimal("0.01"))
    PER=str(PER)
    # print(PER)

    # 动态市盈率
    dynamic_PER=decimal.Decimal(html['data']['snapshot'][key][13]).quantize(decimal.Decimal("0.01"))
    dynamic_PER=str(dynamic_PER)
    # print(dynamic_PER)

    # 市净率
    PBR=decimal.Decimal(html['data']['snapshot'][key][14]).quantize(decimal.Decimal("0.01"))
    PBR=str(PBR)
    # print(PBR)

    # 总市值
    market_value=html['data']['snapshot'][key][15]/100000000
    market_value=decimal.Decimal(market_value).quantize(decimal.Decimal("0.0"))
    market_value=str(market_value)
    market_value=market_value+"亿"
    # print(market_value)


    # 流通市值
    circulation_market_value=html['data']['snapshot'][key][16]/100000000
    circulation_market_value=decimal.Decimal(circulation_market_value).quantize(decimal.Decimal("0.0"))
    circulation_market_value=str(circulation_market_value)
    circulation_market_value=circulation_market_value+"亿"
    # print(circulation_market_value)

    # 成交量
    turnover_volume=html['data']['snapshot'][key][17]/1000000
    turnover_volume=decimal.Decimal(turnover_volume).quantize(decimal.Decimal("0.0"))
    turnover_volume=str(turnover_volume)
    turnover_volume=turnover_volume+"万手"
    # print(turnover_volume)

    # 成交额
    turnover_value=html['data']['snapshot'][key][18]/100000000
    turnover_value=decimal.Decimal(turnover_value).quantize(decimal.Decimal("0.00"))
    turnover_value=str(turnover_value)
    turnover_value=turnover_value+"亿"
    # print(turnover_value)

    # # 是否停牌
    # suspend=""
    # if html['data']['snapshot'][key][19]=="SS.esa":
    #     suspend="停牌"
    # else:
    #     suspend = "正常交易"
    # print(suspend)


    # 量比
    volume_ratio=decimal.Decimal(html['data']['snapshot'][key][21]).quantize(decimal.Decimal("0.01"))
    volume_ratio=str(volume_ratio)
    # print(volume_ratio)

    # 流通股本
    circulation_shares=html['data']['snapshot'][key][22]/100000000
    circulation_shares=decimal.Decimal(circulation_shares).quantize(decimal.Decimal("0.00"))
    circulation_shares=str(circulation_shares)
    circulation_shares=circulation_shares+"亿"
    # print(circulation_shares)


    # 总股本
    total_shares=html['data']['snapshot'][key][23]/100000000
    total_shares=decimal.Decimal(total_shares).quantize(decimal.Decimal("0.00"))
    total_shares=str(total_shares)
    total_shares=total_shares+"亿"
    # print(total_shares)

    # 每股净资产
    BPS=decimal.Decimal(html['data']['snapshot'][key][24]).quantize(decimal.Decimal("0.01"))
    BPS=str(BPS)
    # print(BPS)

    sql='''
        insert into company_detail values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''

    cursor.execute(sql, [id,simple_name,trade_status,update_time,price_tem,change_,change_percent,
                         closing_price,opening_price,highest,lowest,amplitude,turnover_ratio,PER,
                         dynamic_PER,PBR,market_value,circulation_market_value,turnover_volume,
                         turnover_value,volume_ratio,circulation_shares,total_shares,BPS])
    db.commit()

    print(id)
    return 0

def getData_update(id,place,simple_name):
    key = id + "." + place
    url="https://api-ddc-wscn.xuangubao.cn/market/real?fields=prod_name,trade_status,update_time,last_px,px_change,px_change_rate,preclose_px,open_px,high_px,low_px,amplitude,turnover_ratio,pe_rate,dyn_pe,dyn_pb_rate,market_value,circulation_value,turnover_volume,turnover_value,hq_type_code,securities_type,volume_ratio,circulation_shares,total_shares,bps&prod_code="+key

    html = askURL(url)  # 保存获取到的网页源码

    html = json.loads(html)

    context = decimal.getcontext()  # 获取decimal现在的上下文
    context.rounding = decimal.ROUND_HALF_UP  # 修改rounding策略


    if(html['data']['snapshot']=={}):

        trade_status = "已退市"

        sql = '''
            update company_detail 
            set id=%s,simple_name=%s,trade_status=%s,update_time=%s,price_tem=%s,
            change_=%s,change_percent=%s,closing_price=%s,opening_price=%s,highest=%s,lowest=%s,amplitude=%s,turnover_ratio=%s,
            PER=%s,dynamic_PER=%s,PBR=%s,market_value=%s,circulation_market_value=%s,turnover_volume=%s,turnover_value=%s,
            volume_ratio=%s,circulation_shares=%s,total_shares=%s,BPS=%s
            where id=%s
        '''

        cursor.execute(sql, [id, simple_name, trade_status, "", "", "", "",
                             "", "", "", "", "", "", "",
                             "", "", "", "", "",
                             "", "", "", "", "",id])
        db.commit()
        print(id)

        return 0

    # print("ok")

    # 股票代码
    id=id

    # 股票简称
    # simple_name=html['data']['snapshot'][key][0]
    # print(simple_name)

    # 交易状态
    trade_status=html['data']['snapshot'][key][1]
    if trade_status=="BREAK":
        trade_status="已休市"
    elif trade_status=="HALT":
        trade_status="停牌中"
    else:
        trade_status="已开盘"
    # print(trade_status)

    # 更新时间
    update_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # print(update_time)

    # 股价
    price_tem=html['data']['snapshot'][key][3]
    price_tem=str(price_tem)
    # print(price_tem)

    # 涨跌值
    change_=decimal.Decimal(html['data']['snapshot'][key][4]).quantize(decimal.Decimal("0.01"))
    change_=str(change_)
    # print(change_)


    # 涨跌百分比
    change_percent=decimal.Decimal(html['data']['snapshot'][key][5]).quantize(decimal.Decimal("0.01"))
    change_percent=str(change_percent)
    change_percent=change_percent+"%"
    # print(change_percent)

    # 昨日收盘价
    closing_price=decimal.Decimal(html['data']['snapshot'][key][6]).quantize(decimal.Decimal("0.01"))
    closing_price=str(closing_price)
    # print(closing_price)

    # 今日开盘价
    opening_price=decimal.Decimal(html['data']['snapshot'][key][7]).quantize(decimal.Decimal("0.01"))
    opening_price=str(opening_price)
    # print(opening_price)

    # 今日最高价
    highest=decimal.Decimal(html['data']['snapshot'][key][8]).quantize(decimal.Decimal("0.01"))
    highest=str(highest)
    # print(highest)

    # 今日最低价
    lowest=decimal.Decimal(html['data']['snapshot'][key][9]).quantize(decimal.Decimal("0.01"))
    lowest=str(lowest)
    # print(lowest)

    # 振幅
    amplitude=decimal.Decimal(html['data']['snapshot'][key][10]).quantize(decimal.Decimal("0.01"))
    amplitude=str(amplitude)
    amplitude = amplitude + "%"
    # print(amplitude)

    # 换手率
    turnover_ratio=decimal.Decimal(html['data']['snapshot'][key][11]).quantize(decimal.Decimal("0.01"))
    turnover_ratio=str(turnover_ratio)
    turnover_ratio = turnover_ratio + "%"
    # print(turnover_ratio)

    # 市盈率
    PER=decimal.Decimal(html['data']['snapshot'][key][12]).quantize(decimal.Decimal("0.01"))
    PER=str(PER)
    # print(PER)

    # 动态市盈率
    dynamic_PER=decimal.Decimal(html['data']['snapshot'][key][13]).quantize(decimal.Decimal("0.01"))
    dynamic_PER=str(dynamic_PER)
    # print(dynamic_PER)

    # 市净率
    PBR=decimal.Decimal(html['data']['snapshot'][key][14]).quantize(decimal.Decimal("0.01"))
    PBR=str(PBR)
    # print(PBR)

    # 总市值
    market_value=html['data']['snapshot'][key][15]/100000000
    market_value=decimal.Decimal(market_value).quantize(decimal.Decimal("0.0"))
    market_value=str(market_value)
    market_value=market_value+"亿"
    # print(market_value)


    # 流通市值
    circulation_market_value=html['data']['snapshot'][key][16]/100000000
    circulation_market_value=decimal.Decimal(circulation_market_value).quantize(decimal.Decimal("0.0"))
    circulation_market_value=str(circulation_market_value)
    circulation_market_value=circulation_market_value+"亿"
    # print(circulation_market_value)

    # 成交量
    turnover_volume=html['data']['snapshot'][key][17]/1000000
    turnover_volume=decimal.Decimal(turnover_volume).quantize(decimal.Decimal("0.0"))
    turnover_volume=str(turnover_volume)
    turnover_volume=turnover_volume+"万手"
    # print(turnover_volume)

    # 成交额
    turnover_value=html['data']['snapshot'][key][18]/100000000
    turnover_value=decimal.Decimal(turnover_value).quantize(decimal.Decimal("0.00"))
    turnover_value=str(turnover_value)
    turnover_value=turnover_value+"亿"
    # print(turnover_value)

    # # 是否停牌
    # suspend=""
    # if html['data']['snapshot'][key][19]=="SS.esa":
    #     suspend="停牌"
    # else:
    #     suspend = "正常交易"
    # print(suspend)


    # 量比
    volume_ratio=decimal.Decimal(html['data']['snapshot'][key][21]).quantize(decimal.Decimal("0.01"))
    volume_ratio=str(volume_ratio)
    # print(volume_ratio)

    # 流通股本
    circulation_shares=html['data']['snapshot'][key][22]/100000000
    circulation_shares=decimal.Decimal(circulation_shares).quantize(decimal.Decimal("0.00"))
    circulation_shares=str(circulation_shares)
    circulation_shares=circulation_shares+"亿"
    # print(circulation_shares)


    # 总股本
    total_shares=html['data']['snapshot'][key][23]/100000000
    total_shares=decimal.Decimal(total_shares).quantize(decimal.Decimal("0.00"))
    total_shares=str(total_shares)
    total_shares=total_shares+"亿"
    # print(total_shares)

    # 每股净资产
    BPS=decimal.Decimal(html['data']['snapshot'][key][24]).quantize(decimal.Decimal("0.01"))
    BPS=str(BPS)
    # print(BPS)

    sql='''
        update company_detail 
        set id=%s,simple_name=%s,trade_status=%s,update_time=%s,price_tem=%s,
        change_=%s,change_percent=%s,closing_price=%s,opening_price=%s,highest=%s,lowest=%s,amplitude=%s,turnover_ratio=%s,
        PER=%s,dynamic_PER=%s,PBR=%s,market_value=%s,circulation_market_value=%s,turnover_volume=%s,turnover_value=%s,
        volume_ratio=%s,circulation_shares=%s,total_shares=%s,BPS=%s
        where id=%s
    '''

    cursor.execute(sql, [id,simple_name,trade_status,update_time,price_tem,change_,change_percent,
                         closing_price,opening_price,highest,lowest,amplitude,turnover_ratio,PER,
                         dynamic_PER,PBR,market_value,circulation_market_value,turnover_volume,
                         turnover_value,volume_ratio,circulation_shares,total_shares,BPS,id])
    db.commit()

    print(id)
    return 0

def init():
    sql = '''
            select id,place,simple_name from company_base 
    '''
    db.ping(reconnect=True)

    num = cursor.execute(sql)
    res = cursor.fetchall()

    for i in res:
        getData_init(i[0],i[1],i[2])

def update_id(id):
    sql = '''
                select id,place,simple_name from company_base where id=%s
        '''
    db.ping(reconnect=True)

    num = cursor.execute(sql,id)
    res = cursor.fetchall()

    getData_update(res[0][0], res[0][1], res[0][2])

def update_simple_name(simple_name):
    sql = '''
                select id,place,simple_name from company_base where simple_name=%s
        '''
    db.ping(reconnect=True)

    num = cursor.execute(sql,simple_name)
    res = cursor.fetchall()

    getData_update(res[0][0], res[0][1], res[0][2])

def update_eng_id(eng_id):
    sql = '''
                select id,place,simple_name from company_base where eng_id=%s
        '''
    db.ping(reconnect=True)

    num = cursor.execute(sql,eng_id)
    res = cursor.fetchall()

    getData_update(res[0][0], res[0][1], res[0][2])


def main():
    # 1.爬取网页
    init()




if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # init_db("movietest.db")
    print("爬取完毕！")



