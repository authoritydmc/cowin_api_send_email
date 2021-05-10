from cowin_get_email.databases.database import Base, engine, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean,Text
from datetime import datetime
import json
from cowin_get_email.utility import common_util


class Vaccine(Base):
    __tablename__ = 'vaccines'
    id = Column('id', Integer, primary_key=True)
    pincode = Column('pincode', Integer,unique=True)
    res_str=Column(Text)
    lastUpdated=Column(Integer,default=0)



    def __repr__(self):
     response={}
     response['pincode']=self.pincode
     response['last_updated']=self.lastUpdated
     response['res_str']=self.res_str

     return json.dumps(response,indent=4)

     




def addVaccine(pincode,res_str,lastUpdated=''):
    try:
        session=Session()
        temp_v=Vaccine()
        if lastUpdated=='':
            lastUpdated=int(common_util.getUtcTimeStamp())

        temp_v.pincode=int(pincode)
        temp_v.res_str=res_str
        temp_v.lastUpdated=lastUpdated
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
