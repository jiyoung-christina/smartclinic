__author__ = 'lacidjun'
# -*- coding: utf-8 -*-

from flask import render_template, request, current_app, session, redirect, url_for, jsonify

from SmartClinicServ.database import dao
from SmartClinicServ.SmartClinicLogger import Log
from SmartClinicServ.SmartClinicBlueprint import smartclinic
from SmartClinicServ.model.user import User
from SmartClinicServ.model.hospital import Hospital

from login import login_required

@smartclinic.route('/insert_hospital', methods=['POST', 'GET'])
#임시 병원 입력 페이지
def temp_insert():
    Log.info(request)
    if request.method == 'POST':
        try:
            hospital = Hospital(hosp_name = request.form['hosp_name'], hosp_subj = request.form['hosp_subj'], hosp_call = request.form['hosp_call'],
                   hosp_addr = request.form['hosp_addr'], hosp_page = request.form['hosp_page'])
            dao.add(hospital)
            dao.commit()
            Log.debug(hospital)
        except Exception as e:
            error = "DB error occur : " + str(e)
            Log.error(error)
            dao.rollback
            raise e
        else:
            return redirect('insert_hospital')
    else:
        return render_template('temp_hospital.html')



@smartclinic.route('/api/v1/test', methods=['POST', 'GET'])
#@login_required #postman으로 테스트할 경우 주석처리
def apiTest():
    try:
        user = dao.query(User).filter_by(email=request.form['id']).first()
    except Exception as e:
        Log.error(str(e))
        raise e
    return jsonify(data=user.email, kim=user.password)

@smartclinic.route('/api/v1/hospital', methods=['POST'])
def hospitalInfo():
    try:
        hospitals = dao.query(Hospital).all()
        hospitals_list = []
        for hospital in hospitals:
            hospitals_list.append(hospital.hosp_name)
    except Exception as e:
        Log.error(str(e))
        raise e
    return jsonify(hosp_name = hospitals_list)
