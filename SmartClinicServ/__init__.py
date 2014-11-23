#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for
from flask.ext.socketio import SocketIO
import os

def print_settings(config):
    print '========================================================'
    print 'SETTINGS for SmartClinic APPLICATION'
    print '========================================================'
    for key, value in config:
        print '%s=%s' % (key, value)
    print '========================================================'

def not_found(error):
    return render_template('404.html'), 404

def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500
    
    
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def create_app():
    smartClinic_app = Flask(__name__)
    # 기본 설정 운영 환경 또는 기본 설정을 변경을 하려면 실행 환경변수인 PHOTOLOG_SETTINGS에 변경할 설정을 담고 있는 파일 경로를 설정
    from SmartClinicServ.SmartClinicConfig import SmartClinicConfig
    smartClinic_app.config.from_object(SmartClinicConfig)
    print_settings(smartClinic_app.config.iteritems())
        
    # 로그 초기화
    from SmartClinicServ.SmartClinicLogger import Log
    log_filepath = os.path.join(smartClinic_app.root_path,
                                smartClinic_app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)
    
    # 데이터베이스 처리 
    from SmartClinicServ.database import DBManager
    db_file = smartClinic_app.config['DB_FILE_PATH']

    db_url = smartClinic_app.config['DB_URL'] + db_file
    Log.info(db_url)
    DBManager.init(db_url, eval(smartClinic_app.config['DB_LOG_FLAG']))
    DBManager.init_db()
       
    # 뷰 함수 모듈은 어플리케이션 객체 생성하고 블루프린트 등록전에 
    # 뷰 함수가 있는 모듈을 임포트해야 해당 뷰 함수들을 인식할 수 있음
    from SmartClinicServ.controller import *
    
    from SmartClinicServ.SmartClinicBlueprint import smartclinic
    smartClinic_app.register_blueprint(smartclinic)

    from SmartClinicServ.cache_session import SimpleCacheSessionInterface
    smartClinic_app.session_interface = SimpleCacheSessionInterface()
    
    # 공통으로 적용할 HTTP 404과 500 에러 핸들러를 설정
    smartClinic_app.error_handler_spec[None][404] = not_found
    smartClinic_app.error_handler_spec[None][500] = server_error
    
    # 페이징 처리를 위한 템플릿 함수
    smartClinic_app.jinja_env.globals['url_for_other_page'] = \
        url_for_other_page
    socketio = SocketIO(smartClinic_app)

    return smartClinic_app, socketio

