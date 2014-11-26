__author__ = 'lacidjun'
# -*- coding: utf-8 -*-

from flask import render_template, request, current_app, session, redirect, url_for, jsonify

from SmartClinicServ.database import dao
from SmartClinicServ.SmartClinicLogger import Log
from SmartClinicServ.SmartClinicBlueprint import smartclinic
from SmartClinicServ.model.user import User
from SmartClinicServ.model.hospital import Hospital
from SmartClinicServ.model.reservation import Reservation
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

        return redirect('insert_hospital')
    else:
        return render_template('temp_hospital.html')

@smartclinic.route('/delete_hospital', methods=['POST'])
def temp_delete():
    if request.method == 'POST':
        try:
            hospital = dao.query(Hospital).filter_by(hosp_name = request.form['hosp_name']).first()
            dao.delete(hospital)
            dao.commit()
        except Exception as e:
            error = "DB error occur : " + str(e)
            Log.error(error)
            dao.rollback
            raise e

    return jsonify(hosp_name = 'test')

@smartclinic.route('/api/v1/test', methods=['POST', 'GET'])
#@login_required #postman으로 테스트할 경우 주석처리
def apiTest():
    try:
        user = dao.query(User).filter_by(email=request.form['id']).first()
    except Exception as e:
        Log.error(str(e))
        raise e
    return jsonify(data=user.email, kim=user.password)

@smartclinic.route('/api/v1/hospitals', methods=['POST'])
def hospitalsInfo():
    try:
        hospitals = dao.query(Hospital).all()
        hospitals_list = []
        for hospital in hospitals:
            hospitals_list.append(hospital.hosp_name)
    except Exception as e:
        Log.error(str(e))
        raise e
    return jsonify(hosp_name = hospitals_list)

@smartclinic.route('/api/v1/hospital', methods=['POST'])
def hospitalInfo():
    try:
        print request.form['hosp_name']
        hospital = dao.query(Hospital).filter_by(hosp_name=request.form['hosp_name']).first()
    except Exception as e:
        Log.error(str(e))
        raise e
    return jsonify(hosp_name = hospital.hosp_name, hosp_subj = hospital.hosp_subj, hosp_call = hospital.hosp_call,
                   hosp_addr = hospital.hosp_addr, hosp_page = hospital.hosp_page)

@smartclinic.route('/api/v1/reservation', methods=['GET', 'POST'])
def reservationInfo():
    response_time = []
    if request.method == 'GET':
        try:
            print request.args.get('hosp_name')
            #print request.form['hosp_name'] + ' ' + request.form['hosp_subj'] + ' ' + request.form['date']
            reservations = dao.query(Reservation).filter_by(hosp_name=request.args.get('hosp_name'), hosp_subj=request.args.get('hosp_subj'),
                                                        date=request.args.get('date')).all()
            print reservations
            for reservation in reservations:
                response_time.append(reservation.time)
        except Exception as e:
            Log.error(str(e))
            raise e
        return jsonify(time_table=response_time)

    elif request.method == 'POST':
        try:
            reservation = Reservation(hosp_name=request.form['hosp_name'], hosp_subj=request.form['hosp_subj'], email = request.form['email'],
                   date=request.form['date'], time=request.form['time'])
            dao.add(reservation)
            dao.commit()
            Log.debug(reservation)
        except Exception as e:
            error = "DB error occur : " + str(e)
            Log.error(error)
            dao.rollback
            return jsonify(response='fail')

    return jsonify(response='success')


@smartclinic.route('/api/v1/came', methods=['POST'])
def userState():
    try:
        reservation = dao.query(Reservation).filter_by(hosp_name=request.form['hosp_name'], hosp_subj=request.form['hosp_subj'],
                                                       email=request.form['email'], date=request.form['date']).first()
        reservation.state = 'on'
        dao.add(reservation)
        dao.commit()
        Log.debug(reservation)
    except Exception as e:
        Log.error(str(e))
        return jsonify(response='fail')

    return jsonify(response='success')

@smartclinic.route('/api/v1/visit', methods=['GET'])
def visitUser():
    visit_user = []
    reservation_user = []
    try:
        reservations = dao.query(Reservation).filter_by(hosp_name=request.args.get('hosp_name'), hosp_subj=request.args.get('hosp_subj'),
                                                       date=request.args.get('date')).all()
        for reservation in reservations:
            reservation_user.append(reservation.email)
            if reservation.state == 'on':
                visit_user.append(reservation.email)

    except Exception as e:
        Log.error(str(e))
        return jsonify(response='fail')

    return jsonify(reservation_user=reservation_user, visit_user=visit_user)

