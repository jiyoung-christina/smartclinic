__author__ = 'lacidjun'

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from SmartClinicServ.model import Base

class Operator(Base):
    __tablename__ = 'operators'
    email = Column(String(100), primary_key=True)
    password = Column(String(120))
    hospital = Column(String(70))
    subject = Column(String(50))
#name, language(전문) suj삭제
    def __init__(self, email=None, password=None, hospital=None, subject=None):
        self.email = email
        self.password = password
        self.hospital = hospital
        self.subject = subject

    def __repr__(self):
        return '<email %r>' % (self.email)

