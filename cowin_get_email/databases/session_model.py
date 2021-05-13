from cowin_get_email.databases.database import Base, engine, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from cowin_get_email.utility import common_util
import json

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
    last_avail_cnt=Column(Integer,default=0)

    def __repr__(self):

        data={}
        data['id']=self.session_id
        data['Vaccine_name']=self.vaccine_name
        data['center_id']=self.center_id
        data['min_age']=self.min_age
        data['available']=self.available
        data['onDate']=self.date
        return json.dumps(data)



def addSessions(sid, cid, min_age, available, slots, date, vaccine_name):
    try:
        session = Session()
        slots="<br>".join(slots)
        sid=str(sid)
        cid=int(cid)
        available=int(available)
        date=str(date)
        vaccine_name=str(vaccine_name)
        print("$"*80)
        # whether Session Exist.
        temp=None
        oldRecord=session.query(VaccineSession).filter(VaccineSession.session_id==sid).first()

        print("OLD RECORD-->",oldRecord)
       
        if oldRecord!=None:
            temp=oldRecord
            print("{} {} already Exist hence Updating...".format(sid,vaccine_name))
            temp.last_avail_cnt=oldRecord.available 
        else:
            temp=VaccineSession()
            print("{} {} is New Record".format(sid,vaccine_name))
            temp.last_avail_cnt=available
        
        temp.session_id = sid
        temp.center_id = cid
        temp.min_age = min_age
        temp.available = available
        temp.slots = slots
        temp.date = date
        temp.vaccine_name = vaccine_name
        temp.lastUpdated=common_util.getUtcTimeStamp()
        
        # for the first Time Last available is same as avail.
        session.add(temp)
        res=session.commit()

        return "Added Seesion->[{}]".format(res),True
    
    except Exception as e:
        print("A fatal Exception "+str(e))
        return "error [{}] occured while Adding Sessions of Vaccine for Center[{}]".format(e,cid),False
    
    finally:
        session.close()

def getAllSessions():
    try:
        session = Session()
        sessionsQ = session.query(VaccineSession).order_by(VaccineSession.lastUpdated).all()
        sessionList = []
        for s in sessionsQ:
            sessionList.append(s)

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
    



