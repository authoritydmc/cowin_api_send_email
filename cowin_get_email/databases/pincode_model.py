from cowin_get_email.databases.database import Base,engine,Session
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from datetime import  datetime


class Pincode(Base):
    __tablename__='pincode'
    id=Column('id',Integer,primary_key=True)
    pincode=Column('pincode', Integer)
    vaccine=Column('vaccine',String)
    min_age=Column('min_age',Integer)
    fee=Column('fee',String)
    available_vac_cap=Column('available_vaccine_cap',Integer)
    center_id=Column('center_id',Integer)
    center_name=Column('center_name',String)
    center_address=Column('center_address',String)
    prev_cap=Column('prev_cap',Integer)


Base.metadata.create_all(bind=engine)
