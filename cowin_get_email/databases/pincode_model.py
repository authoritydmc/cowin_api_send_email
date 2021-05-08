from cowin_get_email.databases.database import Base, engine, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

print("pincode model called")
class Pincode(Base):
    __tablename__ = 'pincodes'
    id = Column(Integer, primary_key=True)
    pincode = Column(Integer, unique=True)
    district_id = Column(Integer, default=-1)

    def __repr__(self):
        res = {}
        res['pincode'] = self.pincode
        res['district_id'] = self.district_id
        return str(res)


def addPincode(pincode, district_id=-1):
    print('*'*80)
    print('Adding Pincode {} with dist id {} '.format(pincode,district_id))
    print('*'*80)
    try:
        session = Session()
        res, isexist = isPincodeExist(pincode)
        if isexist == False:
            print('-'*80)
            print("PINCODE ",pincode,"NOT EXIST IN DB ")
            temp_p = Pincode()
            temp_p.pincode=pincode
            temp_p.district_id=district_id
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
                    res.district_id = district_id
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
        pincodes = session.query(Pincode)
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


Base.metadata.create_all(bind=engine)
