from cowin_get_email.databases.database import Base, engine, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
import json


class Vaccine(Base):
    __tablename__ = 'vaccine'
    id = Column('id', Integer, primary_key=True)
    pincode = Column('pincode', Integer)
    vaccine = Column('vaccine', String)
    min_age = Column('min_age', Integer)
    fee = Column('fee', String)
    available_vac_cap = Column('available_vaccine_cap', Integer)
    center_id = Column('center_id', Integer)
    center_name = Column('center_name', String)
    center_address = Column('center_address', String)
    date_avail=Column('date_available', String)
    prev_cap = Column('prev_cap', Integer, default=-1)


    def __repr__(self):
     response={}
     response['vaccine_name']=self.vaccine
     response['pincode']=self.pincode
     response['min_age']=self.min_age
     response['fee']=self.fee
     response['available_capacity']=self.available_vac_cap
     response['previous_capacity']=self.prev_cap
     response['center_id']=self.center_id
     response['center_name']=self.center_name
     response['center_address']=self.center_address
     response['date_available']=self.date_avails
     return json.dumps(response,indent=4)

     




def addVaccine(vaccine,pincode, min_age, fee, available_vaccine_cap, center_id, center_name, center_address,date_avail,previous_cap):
    try:
        session=Session()
        temp_v=Vaccine()
        temp_v.vaccine=vaccine
        temp_v.pincode=pincode
        temp_v.min_age=min_age
        temp_v.fee=fee
        temp_v.available_vac_cap=available_vaccine_cap
        temp_v.center_id=center_id
        temp_v.center_name=center_name
        temp_v.center_address=center_address 
        temp_v.prev_cap=previous_cap
        temp_v.date_avail=date_avail
        session.add(temp_v)
        session.commit()
        return 'Vaccine Added successfully',True
        


    except Exception as e:

        return 'Exception Occured {} '.format(e),False
    finally:
        session.close()




def getVaccineByPincode(pincode):
    try:
        session = Session()
        vaccines = session.query(Vaccine).filter(Vaccine.pincode==pincode).all()
        datas = {}
        lst = []
        for vaccine in vaccines:
            lst.append(vaccine)

        datas['vaccines'] = lst
        datas['total'] = len(datas['vaccines'])
        datas['filter_by']='pincode'
        datas['filter_param']=pincode
        # print(datas)

        return json.dumps(datas), True

    except Exception as e:
        return "Exception occurred {}".format(e), False

    finally:
        session.close()

    


def getAllVaccineRecords():
    try:
        session = Session()
        vaccines = session.query(Vaccine)
        datas = {}
        lst = []
        for vaccine in vaccines:
            lst.append(vaccine)

        datas['vaccines'] = lst
        datas['total'] = len(datas['vaccines'])
        print(datas)

        return datas, True

    except Exception as e:
        return "Exception occurred {}".format(e), False

    finally:
        session.close()


Base.metadata.create_all(bind=engine)
