__author__ = 'lacidjun'

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from SmartClinicServ.model import Base

class User(Base):
    __tablename__ = 'users'
    email = Column(String(100), primary_key=True)
    address = Column(String(50))
    password = Column(String(120))
    user_id = Column(String(50), unique=False)
    department = Column(String(30), unique=False)
    registered_on = Column(DateTime, unique=False)
    activated = Column(Boolean, default=False)
    name = Column(String(30))
    gender = Column(String(10))


    def __init__(self, email=None, address=None, password=None, user_id=None, department=None, registered_on=None, activated=None, name=None, gender=None):
        self.email = email
        self.address = address
        self.password = password
        self.user_id = user_id
        self.department = department
        self.registered_on = registered_on
        self.activated = activated
        self.name = name
        self.gender = gender

    def __repr__(self):
        return '<email %r>' % (self.email)

