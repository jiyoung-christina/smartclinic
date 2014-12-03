# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask.ext.mail import Mail

class DBManager:
    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag=True):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag)
        DBManager.__session = \
            scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=DBManager.__engine))

        global dao
        dao = DBManager.__session

    @staticmethod
    def init_db(app):
        from SmartClinicServ.model import *
        from SmartClinicServ.model import Base
        Base.metadata.create_all(bind=DBManager.__engine)

        app.config.update(
            DEBUG=True,
            #EMAIL SETTINGS
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=465,
            MAIL_USE_SSL=True,
            MAIL_USERNAME='ggamcong119@google.com',
            MAIL_PASSWORD='qorwlgns119')
        global mail
        mail = Mail(app)
dao = None
mail = None