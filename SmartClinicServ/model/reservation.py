__author__ = 'lacidjun'

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from SmartClinicServ.model import Base

class Reservation(Base):
    __tablename__ = 'reservatons'
    hosp_name = Column(String(100))
    email = Column(String(100))#foreign key add
    reserv_num = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(50))
    time = Column(String(50))
    state = Column(String(20))
    purpose = Column(String(4000))

    #purpose 목적, subj삭제
    def __init__(self, hosp_name=None, hosp_subj=None, email=None, date=None, time=None, state='off', purpose=None):
        self.hosp_name = hosp_name
        self.email = email
        self.date = date
        self.time = time
        self.state = state
        self.purpose = purpose

    def __repr__(self):
        return '<email %r>' % (self.email)


