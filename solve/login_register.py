# -*- coding: utf-8 -*-g
# @Time : 2020/12/6 23:42
# @Author : Blink_Leo
# @File : login_register.py
# @Software: PyCharm

import pymysql

db = pymysql.connect(host='localhost', user='root', password='123', database='work')
# autocommit =True
cursor = db.cursor()


# sql_name = '''
#     select name from user
# '''
# sql_password='''
#     select password from user
# '''

def have_name(name):
    sql_name = '''
        select * from user where name=%s
    '''
    db.ping(reconnect=True)
    if (cursor.execute(sql_name, name) == 0):
        # cursor.close()
        # db.close()
        return False
    else:
        # cursor.close()
        # db.close()
        return True


def create_user(name, password):
    sql_create = '''
            insert into user values (default,%s,%s)
        '''
    db.ping(reconnect=True)
    cursor.execute(sql_create, [name, password])
    # db.commit()

    name = 'user_' + name
    sql_create = '''
            create table {name}(
                com_id varchar(10) primary key 
            )
    '''.format(name=name)
    db.ping(reconnect=True)
    cursor.execute(sql_create)
    db.commit()


    # cursor.close()
    # db.close()
    return True


def check_password(name, my_password):
    sql_name = '''
            select password from user where name=%s
        '''
    db.ping(reconnect=True)
    num = cursor.execute(sql_name, name)
    res = cursor.fetchall()

    if (my_password == res[0][0]):
        return True
    else:
        return False
