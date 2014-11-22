__author__ = 'lacidjun'
# -*- coding: utf-8 -*-


class SmartClinicConfig(object):
    #: 데이터베이스 연결 URL
    DB_URL= 'mysql://root:1002@localhost/'
    #: 데이터베이스 파일 경로
    DB_FILE_PATH = 'user'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    #: 세션 타임아웃은 초(second) 단위(60분)
    PERMANENT_SESSION_LIFETIME = 60 * 60
    #: 쿠기에 저장되는 세션 쿠키
    SESSION_COOKIE_NAME = 'smartclinic_session'
    #: 로그 레벨 설정
    LOG_LEVEL = 'debug'
    #: 디폴트 로그 파일 경로
    LOG_FILE_PATH = '../SmartClinicServ/log/SmartClinicServ.log'
    #: 디폴트 SQLAlchemy trace log 설정
    DB_LOG_FLAG = 'True'



