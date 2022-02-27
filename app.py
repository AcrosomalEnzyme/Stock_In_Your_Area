from flask import Flask, render_template, url_for, request, flash, redirect, jsonify
from solve import login_register
import spider_static
import solve
from spider_static import spider_static_company_detail
import pymysql
import os
import time
import json
import decimal
from decimal import Decimal
import urllib.request, urllib.error  # 制定URL，获取网页数据
from solve import do_data

context = decimal.getcontext()  # 获取decimal现在的上下文
context.rounding = decimal.ROUND_HALF_UP  # 修改rounding策略

app = Flask(__name__)
app.secret_key = "123"

# user_name = '暂未登录'




@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            print(username)

            if not all([username, password]):
                flash('请填写所有信息')

            elif not solve.login_register.have_name(username):
                flash('用户不存在')

            elif solve.login_register.have_name(username):
                if not login_register.check_password(username, password):
                    flash('密码错误')
                else:
                    solve.do_data.set_search(username, '1', '000001')
                    return redirect(url_for("home"))



    except SyntaxError:
        pass

    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        print(username)

        if not all([username, password, password2]):
            flash('请填写所有信息')
        elif password != password2:
            flash('两次密码不一致，请重新输入')

        elif solve.login_register.have_name(username) == False:
            solve.login_register.create_user(username, password)
            flash('注册成功')
        else:
            flash('已有该用户名')

    return render_template('register.html')

@app.route('/search_data', methods=['GET','POST'])
def search_data():

    if request.method == 'POST':
        user_name=request.form.get('user_name_')
        search_kind = request.form.get('kind')
        search_value = request.form.get('content')

        do_data.set_search(user_name, search_kind, search_value)

        return redirect(url_for("result"))

@app.route('/select_stock', methods=['GET','POST'])
def select_stock():

    if request.method == 'POST':
        select_id=request.form.get('select_id')
        user_name = request.form.get('user_name_')

        do_data.select_stock(user_name, select_id)


        return redirect(url_for("home"))

@app.route('/my_select', methods=['GET','POST'])
def my_select():

    res = do_data.get_search_state()
    user_name = res[0][0]
    # user_name='f'

    res = do_data.get_my_stock(user_name)
    if res==0:
        response={'data':'','user_name':user_name}
        return jsonify(response), 200
    response = do_data.get_my_stock_data(res)

    response['user_name'] = user_name

    return jsonify(response), 200

@app.route('/stock_data', methods=['GET','POST'])
def stock_data():

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

    if response['id'] == '':
        response['user_name'] = user_name
        return jsonify(response), 200

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

    return jsonify(response), 200

@app.route('/plate_data', methods=['GET','POST'])
def plate_data():

    res = do_data.get_search_state()
    user_name = res[0][0]

    response = do_data.get_plate_data()
    response['user_name'] = user_name

    return jsonify(response), 200

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

@app.route('/plate_up', methods=['GET', 'POST'])
def plate_up():
    return render_template('plate_up.html')

@app.route('/plate_down', methods=['GET', 'POST'])
def plate_down():
    return render_template('plate_down.html')


if __name__ == '__main__':
    app.run()
