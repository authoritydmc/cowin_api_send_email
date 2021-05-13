from cowin_get_email.databases.database import Base, engine, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from cowin_get_email.utility import common_util

print("Session Model is called")
class VaccineSession(Base):
    __tablename__="sessions"
    session_id = Column(String,primary_key=True)
    center_id = Column(Integer)
    min_age = Column(Integer)
    available = Column(Integer)
    slots = Column(String)
    date = Column(String)
    vaccine_name = Column(String)
    lastUpdated=Column(Integer,default=0)



def addSessions(self, sid, cid, min_age, available, slots, date, vaccine_name):
    try:
        session = Session()
        temp=VaccineSession()

        temp.session_id = sid
        temp.center_id = cid
        temp.min_age = min_age
        temp.available = available
        temp.slots = slots
        temp.date = date
        temp.vaccine_name = vaccine_name
        temp.lastUpdated=common_util.getUtcTimeStamp()
        session.add(temp)
        res=session.commit()

        return "Added Seesion->[{}]".format(res),True
    
    except Exception as e:
        return "error {} occured while Adding Sessions of Vaccine for {}".format(e,cid),False
    
    finally:
        session.close()

def getAllSessions():
    try:
        session = Session()
        centers = session.query(VaccineSession).order_by(VaccineSession.lastUpdated).all()
        sessionList = []
        for center in centers:
            sessionList.append(center)

        return sessionList, True

    except Exception as e:
        return "error {} occured while Getting all Sessions ".format(e), False

    finally:
        session.close()

def getSessionByCenter(center_id):
    try:
        session = Session()
        centers = session.query(VaccineSession).filter(VaccineSession.center_id==center_id).order_by(VaccineSession.lastUpdated).all()
        sList = []
        for center in centers:
            sList.append(center)

        return sList, True

    except Exception as e:
        return "error {} occured while Getting Sessions   for {}".format(e, center_id), False

    finally:
        session.close()


Base.metadata.create_all(bind=engine)
    



