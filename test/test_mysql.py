# -*- coding: utf-8 -*-g
# @Time : 2020/12/6 19:19
# @Author : Blink_Leo
# @File : test_mysql.py
# @Software: PyCharm

import pymysql
from solve import login_register
from spider_static import spider_static_company_detail
import time
import decimal
from decimal import Decimal
from solve import do_data
from spider_static import spider_plate_information

context = decimal.getcontext()  # 获取decimal现在的上下文
context.rounding = decimal.ROUND_HALF_UP  # 修改rounding策略

db = pymysql.connect(host='localhost', user='root', password='123', database='work')
# db=pymysql.connect("test.db")
cursor = db.cursor()
# print("ok")
# sql = '''
#     select password from user
# '''
#
# num = cursor.execute(sql)
# results = cursor.fetchall()
#
# print(num)
# print(results[0][0])
# for i in results:
#     print(i[0],i[1])

# i=register.check_name('a')
# if(i):
#     print('ok')
# else:
#     print('xx')


# sql_create = '''
#             insert into user values (default,'s','111')
#         '''
# cursor.execute(sql_create)
#
# sql= '''
#             insert into company_base values (%s,%s,%s,%s)
#         '''
#
# a="1"
# b="2"
# c="3"
# d="4"
# db.ping(reconnect=True)
# cursor.execute(sql,[a,b,c,d])

# name='3'
# name='user_'+name
# sql_create = '''
#         create table {name}(
#             com_id varchar(10) primary key ,
#             simple_name varchar(10) not null ,
#             eng_id varchar(10) not null
#         )
# '''.format(name=name)
# db.ping(reconnect=True)
# cursor.execute(sql_create)
# db.commit()

# name='3'
# name='user_'+name
# sql_change1 = '''
#             update company_base set simple_name='青岛中程',name='青岛中资中程集团股份有限公司',eng_id='QDZC' where id='300208';
#         '''
# sql_change2 = '''
#         update company_base set simple_name='*ST舜喆B',name='广东舜喆(集团)股份有限公司',eng_id='STSZB' where id='200168';
#     '''
# sql_change3 = '''
#         update company_base set simple_name='昇兴股份',name='昇兴集团股份有限公司',eng_id='SXGF' where id='002752';
#     '''
# db.ping(reconnect=True)
# cursor.execute(sql_change1)
# cursor.execute(sql_change2)
# cursor.execute(sql_change3)
# db.commit()


# num = cursor.execute(sql)
# res = cursor.fetchall()
# for i in res:
#     for j in i:
#         print(j)
# print(res[0][1])


#
# for i in res:
#     print(i[0])


# db.commit()

# spider_static_company_detail.update_id('000001')
# time_=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# print(time_)

# spider_static_company_detail.update_all()
# a=spider_static_company_detail.update_id('000001')
# print(a)
# a="18"
# a=decimal.Decimal(a).quantize(decimal.Decimal("0.01"))
# a=str(a)
# print(a)
# sql='''
#         delete from  state
#     '''
# db.ping(reconnect=True)
# cursor.execute(sql)
# db.commit()

# do_data.select_stock('f','000001')
# res=do_data.get_my_stock('f')
# a=do_data.get_my_stock_data(res)
# print(a)

# sql='''
#     SELECT * FROM company_detail WHERE id in ('000001','000002','000005','000033') ORDER BY change_percent;
# '''
# db.ping(reconnect=True)
# cursor.execute(sql)
# res = cursor.fetchall()
# db.commit()
# for i in res:
#     print(i[6])


# res = do_data.get_search_state()
# # user_name = res[0][0]
# print(res[0])

# res=spider_plate_information.get_plate_data()
# print(res)
# login_register.create_user('b','b')
# res = do_data.get_search_state()
# user_name = res[0][0]
# # user_name='f'
#
# res = do_data.get_my_stock(user_name)
# # response = do_data.get_my_stock_data(res)
#
# # response['user_name'] = user_name
#
# print(res)

res = do_data.get_search_state()
user_name=res[0][0]
search_kind = res[0][1]
search_value = res[0][2]


if search_kind == '1':
    response = spider_static_company_detail.update_id(search_value)
elif search_kind == '2':
    response = spider_static_company_detail.update_eng_id(search_value)
else:
    response = spider_static_company_detail.update_simple_name(search_value)

# response = spider_static_company_detail.update_id()



str = response['turnover_ratio']
str = str[:-1]
flo = float(str)
response['turnover_ratio'] = flo

str = response['price_tem']
flo = float(str)
response['price_tem'] = flo

str = response['amplitude']
str = str[:-1]
flo = float(str)
response['amplitude'] = flo

response['user_name'] = user_name
