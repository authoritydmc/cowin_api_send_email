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
        slots=",".join(slots)
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
    


def removeOutDatedSession():
    try:
        session = Session()
        allSessions,_=getAllSessions()
        print("$"*80)

        print("Before deletion total ->",len(allSessions))
        print("$"*80)
        
        currentDate_splitted=common_util.getDate().split("-")
        cur_day,cur_mnth=int(currentDate_splitted[0]),int(currentDate_splitted[1])
        print("Current Date->",cur_day,"-",cur_mnth)
        for s in allSessions:
            date_splitted=s.date.split("-")

            session_day,session_mnth=int(date_splitted[0]),int(date_splitted[1])
            print("session Date->",session_day,"-",session_mnth)
                
            if cur_mnth>session_mnth:
                # like cur date  1-06-2021 and session date 31-05-2021 then also remove 
                print("remove this session")
                session.delete(s)
            elif cur_mnth==session_mnth:
                if cur_day-session_day >=1:
                    print("Remove this Session ")
                    session.delete(s)
                else:
                    print("Keep this session")
    except Exception as e: 
        return "Failure to delete outdated Session",False
    finally:
            session.commit()
            session.close()
            lsts,_=getAllSessions()
            print("$"*80)
            print("After deletion total ->",len(lsts))
            print("$"*80)





