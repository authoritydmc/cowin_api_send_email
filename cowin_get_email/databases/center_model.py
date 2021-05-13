from cowin_get_email.databases.database import Base, engine, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from cowin_get_email.utility import common_util
print("Center Model is called")
import json

class Center(Base):
    __tablename__="centers"
    center_name = Column(String)
    center_id = Column(Integer, primary_key=True)
    address = Column(String)
    pincode = Column(Integer)
    fee = Column(String)
    block_name = Column(String)
    lastUpdated = Column(Integer, default=0)

    def __repr__(self):
        data={}
        data['name']=self.center_name
        data['id']=self.center_id
        data['pincode']=self.pincode
        data['fee']=self.fee
        data['address']=self.address
        data['block']=self.block_name
        data['last_updated']=self.lastUpdated


        return json.dumps(data)


def addCenter(cid, cname, caddr, cpin, fee, block_name):
    try:
        session = Session()

        temp = None
        centerobj=session.query(Center).filter(Center.center_id==cid).first()

        if centerobj!=None:
            temp=centerobj
        else:
            temp=Center()
        temp.center_name = cname
        temp.center_id = cid
        temp.address = caddr
        temp.pincode = cpin
        temp.fee = fee
        temp.block_name = block_name
        temp.lastUpdated = common_util.getUtcTimeStamp()
        session.add(temp)
        res = session.commit()

        return "Added Center->[{}]".format(res), True

    except Exception as e:
        return "error {} occured while Adding Center {}  for {}".format(e, cid, cpin), False

    finally:
        session.close()


def getAllCenters():
    try:
        session = Session()
        centers = session.query(Center).order_by(Center.lastUpdated).all()
        centerList = []
        for center in centers:
            centerList.append(center)

        return centerList, True

    except Exception as e:
        return "error {} occured while Getting all Centers ".format(e), False

    finally:
        session.close()

def getCentersByPincode(pincode):
    try:
        session = Session()
        centers = session.query(Center).filter(Center.pincode==pincode).order_by(Center.lastUpdated).all()
        centerList = []
        for center in centers:
            centerList.append(center)

        return centerList, True

    except Exception as e:
        return "error {} occured while Getting Centers   for {}".format(e, cpin), False

    finally:
        session.close()



Base.metadata.create_all(bind=engine)
