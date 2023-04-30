from sqlalchemy import Column, VARCHAR,Integer, String, JSON, TIMESTAMP, Float
from app import db

class Actions(db.Model):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(VARCHAR(255))
    page = Column(String)
    version = Column(Integer)
    actions = Column(JSON)
    tstamp = Column(TIMESTAMP)

class Top10(db.Model):
    __tablename__ = 'top10'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(VARCHAR(255))
    topX = Column(JSON)
    pak = Column(Float)
    src = Column(Float)
    mse = Column(Float)
    duration = Column(Integer)
    objectWeight = Column(Float)
    colorWeight = Column(Float)
    poweWeight = Column(Float)
    version = Column(Integer)

