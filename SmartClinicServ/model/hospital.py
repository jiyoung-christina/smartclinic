__author__ = 'lacidjun'

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from SmartClinicServ.model import Base

class Hospital(Base):
    __tablename__ = 'hospitals'
    hosp_name = Column(String(100), primary_key=True)
    hosp_subj = Column(String(400))
    hosp_addr = Column(String(120))
    hosp_call = Column(String(50))
    hosp_page = Column(String(100))
#hotels. price. 쿠폰 추가 sunj삭제
    def __init__(self, hosp_name=None, hosp_subj=None, hosp_addr=None, hosp_call=None, hosp_page=None):
        self.hosp_name = hosp_name
        self.hosp_subj = hosp_subj
        self.hosp_addr = hosp_addr
        self.hosp_call = hosp_call
        self.hosp_page = hosp_page

    def __repr__(self):
        return '<email %r>' % (self.hosp_name)