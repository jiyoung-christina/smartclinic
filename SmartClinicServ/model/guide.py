__author__ = 'lacidjun'

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from SmartClinicServ.model import Base

class Guide(Base):
    __tablename__ = 'guides'
    guide_num = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(30))
    period = Column(String(50))
    party = Column(String(50))
    name = Column(String(50))
    email = Column(String(50))

    def __init__(self, language=None, period=None, party=None, name=None, email=None):
        self.language = language
        self.period = period
        self.party = party
        self.name = name
        self.email = email

    def __repr__(self):
        return '<email %r>' % (self.guide_num)