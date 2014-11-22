__author__ = 'lacidjun'

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from SmartClinicServ.model import Base

class User(Base):
    __tablename__ = 'users'
    email = Column(String(100), primary_key=True)
    address = Column(String(50))
    password = Column(String(120))
    name = Column(String(30))
    gender = Column(String(10))

    def __init__(self, email=None, address=None, password=None, name=None, gender=None):
        self.email = email
        self.address = address
        self.password = password
        self.name = name
        self.gender = gender

    def __repr__(self):
        return '<email %r>' % (self.email)
