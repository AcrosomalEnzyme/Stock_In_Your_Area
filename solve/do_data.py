# -*- coding: utf-8 -*-g
# @Time : 2020/12/23 22:52
# @Author : Blink_Leo
# @File : do_data.py
# @Software: PyCharm

from spider_static import spider_static_company_detail
from spider_static import spider_plate_information
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123', database='work')

cursor = db.cursor()


def init(user_name, search_kind, search_value):
    sql = '''
        insert into state values (%s,%s,%s)
    '''
    db.ping(reconnect=True)
    cursor.execute(sql, [user_name, search_kind, search_value])
    db.commit()


def set_search(user_name, search_kind, search_value):
    sql = '''
            delete from state 
        '''
    db.ping(reconnect=True)
    cursor.execute(sql)
    db.commit()

    sql = '''
            insert into state values (%s,%s,%s)
        '''
    db.ping(reconnect=True)
    cursor.execute(sql, [user_name, search_kind, search_value])
    db.commit()


    # init(user_name, search_kind, search_value)
    # sql='''
    #     update state
    #     set search_kind=%s,search_value=%s
    #     where user_name=%s
    # '''
    # db.ping(reconnect=True)
    # cursor.execute(sql, [ search_kind, search_value])
    # db.commit()


def select_stock(user_name, id):
    # 检查是否已经有该股票
    name = "user_" + user_name
    sql = '''
            select * from {name} where com_id={id}
        '''.format(name=name, id=id)
    db.ping(reconnect=True)
    num = cursor.execute(sql)
    db.commit()

    if num == 0:
        sql = '''
            insert into {name} values ('{id}')
        '''.format(name=name, id=id)
        db.ping(reconnect=True)
        cursor.execute(sql)
        db.commit()
        print(id)


def get_search_state():
    sql = '''
                select * from state 
            '''
    db.ping(reconnect=True)
    cursor.execute(sql)
    res = cursor.fetchall()

    return res


def get_my_stock(user_name):
    name = "user_" + user_name
    sql = '''
                select * from {name} 
            '''.format(name=name)
    db.ping(reconnect=True)
    num = cursor.execute(sql)
    if num==0:
        return num
    res = cursor.fetchall()

    return res


def get_my_stock_data(res):
    data = {}
    j = 0
    all_id = "("
    for i in res:
        spider_static_company_detail.update_id(i[0])
        # data['j']=

    for i in res:
        all_id += "'"
        all_id += i[0]
        all_id += "'"
        all_id += ","

    all_id = list(all_id)
    all_id[-1] = ")"
    all_id = ''.join(all_id)

    sql = '''
        SELECT * FROM company_detail WHERE id in {all_id} ORDER BY change_percent DESC
    '''.format(all_id=all_id)
    db.ping(reconnect=True)
    cursor.execute(sql)
    res = cursor.fetchall()
    db.commit()

    data['data'] = res

    return data


def get_plate_data():

    spider_plate_information.get_plate_data()
    plate_data={}



    sql = '''
            select * from plate_up
    '''
    db.ping(reconnect=True)
    num = cursor.execute(sql)
    res = cursor.fetchall()
    plate_data['plate_up']=res

    sql = '''
               select * from plate_down
       '''
    db.ping(reconnect=True)
    num = cursor.execute(sql)
    res = cursor.fetchall()
    plate_data['plate_down'] = res

    return plate_data


