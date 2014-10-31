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
from SmartClinicServ.controller.login import login_required

@smartclinic.route('/user/regist', methods=['GET', 'POST'])
def register_user():
    register_error = None
    Log.info(request)
    if request.method == 'POST':
        try:
            user = User(email=request.form['email'], address=request.form['address'], password=generate_password_hash(request.form['password']),
                        department=request.form['department'], name=request.form['name'], gender=request.form['gender'], user_id=request.form['userid'], activated=False, registered_on=datetime.today())
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