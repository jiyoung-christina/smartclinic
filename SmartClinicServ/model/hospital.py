__author__ = 'lacidjun'

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from SmartClinicServ.model import Base

class Hospital(Base):
    __tablename__ = 'hospitals'
    hosp_name = Column(String(100), primary_key=True)
    hosp_addr = Column(String(120))
    hosp_call = Column(String(50))
    hosp_page = Column(String(100))
    hotels = Column(String(1000))
    price = Column(String(30))
    coupon = Column(String(1000))

    def __init__(self, hosp_name=None, hosp_addr=None, hosp_call=None, hosp_page=None, hotels=None, price=None, coupon=None):
        self.hosp_name = hosp_name
        self.hosp_addr = hosp_addr
        self.hosp_call = hosp_call
        self.hosp_page = hosp_page
        self.hotels = hotels
        self.price = price
        self.coupon = coupon

    def __repr__(self):
        return '<email %r>' % (self.hosp_name)