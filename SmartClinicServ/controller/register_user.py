__author__ = 'lacidjun'
# -*- coding: utf-8 -*-

from flask import render_template, request, current_app, session, redirect, url_for, jsonify
from werkzeug import generate_password_hash
import os

from datetime import datetime
from SmartClinicServ.database import dao
from SmartClinicServ.SmartClinicLogger import Log
from SmartClinicServ.SmartClinicBlueprint import smartclinic
from SmartClinicServ.model.user import User
from SmartClinicServ.model.operator import Operator
from SmartClinicServ.controller.login import login_required

@smartclinic.route('/user/regist', methods=['GET', 'POST'])
def register_user():
    Log.info(request)
    if request.method == 'POST':
        try:
            user = User(email=request.form['email'], address=request.form['address'],
                        password=generate_password_hash(request.form['password']),
                        name=request.form['name'], gender=request.form['gender'])
            dao.add(user)
            dao.commit()
            Log.debug(user)
        except Exception as e:
            error = "DB error occur : " + str(e)
            Log.error(error)
            dao.rollback
            raise e
        else:
            return redirect('login')
    else:
        return redirect('login')

@smartclinic.route('/user/operator_regist', methods=['GET', 'POST'])
def register_operator_user():
    Log.info(request)
    if request.method == 'POST':
        try:
            operator = Operator(email=request.form['email'], password=generate_password_hash(request.form['password']),
                        hospital=request.form['hospital'], subject=request.form['subject'])
            dao.add(operator)
            dao.commit()
            Log.debug(operator)
        except Exception as e:
            error = "DB error occur : " + str(e)
            Log.error(error)
            dao.rollback
            raise e
        else:
            return redirect('admin_login')
    else:
        return redirect('admin_login')


def __get_user(email):
    try:
        current_user = dao.query(User).filter_by(email=email).first()
        Log.debug(current_user)
        return current_user

    except Exception as e:
        Log.error(str(e))
        raise e

@smartclinic.route('/user/check_name', methods=['POST'])
def check_name():
    username = request.json['username']
    #: DB에서 username 중복 확인
    if __get_user(username) :
        return jsonify(result = False)
    else:
        return jsonify(result = True)