__author__ = 'lacidjun'
# -*- coding: utf-8 -*-

from flask import render_template, request, current_app, session, redirect, url_for, jsonify

from SmartClinicServ.database import dao
from SmartClinicServ.SmartClinicLogger import Log
from SmartClinicServ.SmartClinicBlueprint import smartclinic
from SmartClinicServ.model.user import User
from SmartClinicServ.model.hospital import Hospital
from SmartClinicServ.model.reservation import Reservation
from SmartClinicServ.model.operator import Operator
from SmartClinicServ.model.limousin import Limousin
from SmartClinicServ.model.guide import Guide
from login import login_required
import smtplib

@smartclinic.route('/insert_hospital', methods=['POST', 'GET'])
#임시 병원 입력 페이지
def temp_insert():
    Log.info(request)
    if request.method == 'POST':
        try:
            hospital = Hospital(hosp_name = request.form['hosp_name'], hosp_call = request.form['hosp_call'],
                   hosp_addr = request.form['hosp_addr'], hotels=request.form['hotels'],
                   price=request.form['price'], coupon=request.form['coupon'])
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
    sendemail('lacidjun@gmail.com', 'request limousin reservation', 'aa' + 'bb= ' + 'cccc')
    try:
        #user = dao.query(User).filter_by(email=request.form['id']).first()
    except Exception as e:
        Log.error(str(e))
        raise e
    return jsonify(data=user.email)

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
        hospital = dao.query(Hospital).filter_by(hosp_name=request.form['hosp_name']).first()

    except Exception as e:
        print "except"
        Log.error(str(e))
        raise e
    return jsonify(hospital=hospital)


@smartclinic.route('/api/v1/reservation', methods=['GET', 'POST'])
def reservationInfo():
    response_time = []
    if request.method == 'GET':
        try:
            print request.args.get('hosp_name')
            #print request.form['hosp_name'] + ' ' + request.form['hosp_subj'] + ' ' + request.form['date']
            reservations = dao.query(Reservation).filter_by(hosp_name=request.args.get('hosp_name'),
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
            reservation = Reservation(hosp_name=request.form['hosp_name'], purpose=request.form['purpose'], email = request.form['email'],
                   date=request.form['date'], time=request.form['time'])  #purpose 추가
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
        reservation = dao.query(Reservation).filter_by(hosp_name=request.form['hosp_name'], email=request.form['email'],
                                                       date=request.form['date']).first()
        reservation.state = 'on'
        dao.add(reservation)
        dao.commit()
        Log.debug(reservation)
    except Exception as e:
        Log.error(str(e))
        return jsonify(response='fail')

    try:
        user = dao.query(User).filter_by(email=request.form['email']).first()
        operator = dao.query(Operator).filter_by(hospital=reservation.hosp_name, language=user.language).first()
        return jsonify(name=operator.name)  #name = 해당병원전문가 리턴
    except Exception as e:
        Log.error(str(e))
        return jsonify(resoponse='fail')

@smartclinic.route('/api/v1/visit', methods=['GET'])
def visitUser():
    visit_user = []
    reservation_user = []
    try:
        reservations = dao.query(Reservation).filter_by(hosp_name=request.args.get('hosp_name'), date=request.args.get('date')).all() #hosp_subj삭제
        for reservation in reservations:
            reservation_user.append(reservation.email)
            if reservation.state == 'on':
                visit_user.append(reservation.email)

    except Exception as e:
        Log.error(str(e))
        return jsonify(response='fail')

    return jsonify(reservation_user=reservation_user, visit_user=visit_user)

@smartclinic.route('/api/v1/patient', methods=['GET'])
def patientInfo():
    try:
        reservation = dao.query(Reservation).filter_by(hosp_name=request.args.get('hosp_name'), date=request.args.get('date'),
                                                        email=request.args.get('email')).first()

        return jsonify(hosp_name=reservation.hosp_name, date=reservation.date, email=reservation.email, time=reservation.time,
                       state=reservation.state, purpose=reservation.purpose) #개인예약정보 리턴
    except Exception as e:
        Log.error(str(e))
        return jsonify(response='fail')

@smartclinic.route('/api/v1/guide', methods=['GET','POST'])
def guideInfo():
    try:
        guide = Guide(language=request.form['language'], period=request.form['period'], email = request.form['email'],
                party=request.form['party'], name=request.form['name'])  #purpose 추가
        dao.add(guide)
        dao.commit()
        Log.debug(guide)
    except Exception as e:
        error = "DB error occur : " + str(e)
        Log.error(error)
        return jsonify(response='fail')
    return jsonify(response='success')

@smartclinic.route('/api/v1/limousin', methods=['GET','POST'])
def remousinInfo():
    try:
        limousin = Limousin(airport=request.form['airport'], aircraft=request.form['aircraft'], email = request.form['email'],
                depart_date=request.form['depart_date'], depart_time=request.form['depart_time'], name=request.form['name'])  #purpose 추가
        dao.add(limousin)
        dao.commit()
        Log.debug(limousin)
    except Exception as e:
        error = "DB error occur : " + str(e)
        Log.error(error)
        return jsonify(response='fail')
    return jsonify(response='success')

@smartclinic.route('/api/v1/admin', methods=['GET'])
def getAdminHospital():
    try:
        operator = dao.query(Operator).filter_by(email=request.args.get('email')).first() #hosp_subj삭제
    except Exception as e:
        Log.error(str(e))
        return jsonify(response='fail')

    return jsonify(hospital=operator.hospital)



def sendemail(to_addr_list, subject, message, smtpserver='smtp.gmail.com:587'):
    header  = 'From: ggamcong119@gmail.com\n'
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login('ggamcong119@gmail.com','qorwlgns119')
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()