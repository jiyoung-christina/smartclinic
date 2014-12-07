__author__ = 'lacidjun'
# -*- coding: utf-8 -*-

from flask import render_template, request, current_app, session, redirect, url_for
from functools import wraps
from werkzeug import check_password_hash

from SmartClinicServ.database import dao
from SmartClinicServ.SmartClinicLogger import Log
from SmartClinicServ.SmartClinicBlueprint import smartclinic
from SmartClinicServ.model.user import User
from SmartClinicServ.model.operator import Operator
@smartclinic.teardown_request
def close_db_session(exception=None):
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session_key = \
                request.cookies.get(
                    current_app.config['SESSION_COOKIE_NAME'])

            is_login = False
            if session.sid == session_key and \
                session.__contains__('user_info') :
                is_login = True

            if not is_login:
                return redirect('login')

            return f(*args, **kwargs)

        except Exception as e:
            Log.error("SmartClinicServ error occurs : %s" %
                      str(e))
            raise e

    return decorated_function

@smartclinic.route('/login', methods=['GET', 'POST'])
def login_page():
    login_error = None
    Log.info('login page')
    if request.method == 'POST':
        try:
            email = dao.query(User).filter_by(email = request.form['email']).first()
        except Exception as e:
            Log.error(str(e))
            raise e
        if email:
            if not check_password_hash(email.password, request.form['password']):
                login_error = 'Invalid password'
                return render_template('login.html'), 400
            else: #로그인 성공했을때
                session['user_info'] = email
                return render_template('index.html'), 200
        else:
            login_error = 'User email does not exist'
            Log.info(login_error)
            print login_error
            return render_template('login.html'), 400  #user does not exist 출력
    else:
        return render_template('login.html')

@smartclinic.route('/logout')
@login_required
def logout():
    session.clear()
    return render_template('login.html')

@smartclinic.route("/index", methods=['POST', 'GET'])
@smartclinic.route("/", methods=['GET', 'POST'])
@login_required
def index_page():
    if request.method == 'POST':
        return render_template('index.html')
    else:
        return render_template('index.html')

@smartclinic.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    login_error = None
    Log.info('ADMIN login page')
    if request.method == 'POST':
        try:
            email = dao.query(Operator).filter_by(email = request.form['email']).first()
        except Exception as e:
            Log.error(str(e))
            raise e
        if email:
            if not check_password_hash(email.password, request.form['password']):
                login_error = 'Invalid password'
            else: #로그인 성공했을때
                session['user_info'] = email
                return render_template('index.html'), 200
        else:
            login_error = 'User email does not exist'
            Log.info(login_error)
            return render_template('admin_login.html'), 400  #user does not exist 출력
    else:
        return render_template('admin_login.html')

@smartclinic.route('/video', methods=['GET', 'POST'])
def video_call():
    return render_template('video_page.html')