from cowin_get_email.databases.database import Base, engine, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from cowin_get_email.utility import common_util
from cowin_get_email.databases import user_model

print("pincode model called")
class Pincode(Base):
    __tablename__ = 'pincodes'
    id = Column(Integer, primary_key=True)
    pincode = Column(Integer, unique=True)
    district_id = Column(Integer, default=-1)
    lastUpdated=Column(Integer,default=0)

    def __repr__(self):
        res = {}
        res['pincode'] = self.pincode
        res['district_id'] = self.district_id
        res['lastUpdated']=self.lastUpdated

        return str(res)


def addPincode(pincode, district_id=-1):
    print('*'*80)
    print('Adding Pincode {} with dist id {} '.format(pincode,district_id))
    print('*'*80)
    lastUpdated=common_util.getUtcTimeStamp()
    try:
        session = Session()
        res, isexist = isPincodeExist(pincode)
        if isexist == False:
            print('-'*80)
            print("PINCODE ",pincode,"NOT EXIST IN DB ")
            temp_p = Pincode()
            temp_p.pincode=int(pincode)
            temp_p.district_id=int(district_id)
            temp_p.lastUpdated=lastUpdated
            print(temp_p)
            session.add(temp_p)
            session.commit()
            session.close()
            print('-'*80)

            return 'pincode added SuccessFully', True
        else:
            print("PINCODE ",pincode,"EXIST IN DB")

            # pincode exist..
            # now check whether it has District ID or not

            if district_id != -1 and res.district_id==-1:
                    print('-+'*40)
                    print("Updating Pincode {} District id with {} where old dist id was {}".format(pincode,district_id,res.district_id))

                    # queried district id is not provided i.e it is -1
                    res.district_id = int(district_id)
                    res.lastUpdated=lastUpdated
                    session.add(res)
                    session.commit()
                    print('-+'*40)

                    # updated Pincode with District Id

            # else pincode already exist and no modification is going to be done .

            return 'Pincode Exists[no modification done]', False

    except Exception as e:

        return 'Exception -->{} '.format(e), False

    finally:
        session.close()


def isPincodeExist(pincode):
    try:
        session = Session()
        res = session.query(Pincode).filter(Pincode.pincode == pincode).first()
        if res==None:
            raise Exception
        return res, True
    except Exception as e:
        return 'Not Found e->{}'.format(e), False
    finally:
        session.close()


def getAllPincodes():
    try:
        session = Session()
        pincodes = session.query(Pincode).order_by(Pincode.lastUpdated)
        datas = {}
        lst = []
        for pincode in pincodes:
            lst.append(pincode)

        datas['pincodes'] = lst
        datas['total'] = len(datas['pincodes'])
        print(datas)

        return datas, True

    except Exception as e:
        return "Exception occurred {}".format(e), False

    finally:
        session.close()

def getAllPincodeWithoutDistricts():
    try:
        session = Session()
        pincodes = session.query(Pincode).filter(Pincode.district_id==-1).order_by(Pincode.lastUpdated).all()
        datas = {}
        lst = []
        for pincode in pincodes:
            lst.append(pincode)

        datas['pincodes'] = lst
        datas['total'] = len(datas['pincodes'])
        print(datas)

        return datas, True

    except Exception as e:
        return "Exception occurred {}".format(e), False

    finally:
        session.close()


def getPincodesByDistID(dist_id):
    try:
        session = Session()
        pincodes = session.query(Pincode).filter(Pincode.district_id==dist_id).order_by(Pincode.lastUpdated).all()
        datas = {}
        lst = []
        for pincode in pincodes:
            lst.append(pincode)

        datas['pincodes'] = lst
        datas['total'] = len(datas['pincodes'])
        return datas, True

    except Exception as e:
        return "Exception occurred {}".format(e), False

    finally:
        session.close()

def updateLastUpdated(pincode):
    try:
        session = Session()
        pinObj = session.query(Pincode).filter(Pincode.pincode == pincode).first()
        if pinObj==None:
            raise Exception
        pinObj.lastUpdated=common_util.getUtcTimeStamp()
        session.add(pinObj)
        session.commit()
        
        return "Updated LastUpdated Successfully", True
    except Exception as e:
        return 'Not Found e->{}'.format(e), False
    finally:
        session.close()

def removeunTaggedPincode():
    try:
        session = Session()
        pincodes,_=getAllPincodeWithoutDistricts()
        print("All pincodes without dist id ",pincodes['pincodes'])
        for pin in pincodes['pincodes']:
            print("Current Pin-> ",pin)
            usersLst,_=user_model.getUsersofPincode(pin.pincode)
            print("total Users of this pincode-> ",usersLst['total'])
            if usersLst['total']<1:
                print("remove pincode ",pin.pincode ," as no user is tagged to this pincode")
                session.delete(pin)

    except :
        return "Failed to remove untagged Pincode",False
    finally:
        session.commit()
        session.close()



Base.metadata.create_all(bind=engine)
