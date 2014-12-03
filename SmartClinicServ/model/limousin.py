__author__ = 'lacidjun'

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from SmartClinicServ.model import Base

class Limousin(Base):
    __tablename__ = 'limousins'
    limousin_num = Column(Integer, primary_key=True, autoincrement=True)
    airport = Column(String(50))
    aircraft = Column(String(50))
    depart_date = Column(String(50))
    depart_time = Column(String(50))
    name = Column(String(50))
    email = Column(String(50))

    def __init__(self, airport=None, aircraft=None, depart_date=None, depart_time=None, name=None, email=None):
        self.airport = airport
        self.aircraft = aircraft
        self.depart_date = depart_date
        self.depart_time = depart_time
        self.name = name
        self.email = email

    def __repr__(self):
        return '<email %r>' % (self.limousin_num)