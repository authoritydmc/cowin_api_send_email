from cowin_get_email.databases.database import Base, engine, Session
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from cowin_get_email.utility import common_util
from cowin_get_email.databases import user_model


print("District model called")
class District(Base):
    __tablename__ = 'districts'
    district_id = Column(Integer,primary_key=True)
    district_name=Column(String,default='district Name')
    lastUpdated=Column(Integer,default=0)
    isTrackedAllPin=Column(Boolean,default=False)

    def __repr__(self):
        res = {}
        res['district_name'] = self.district_name
        res['district_id'] = self.district_id
        res['lastUpdated']=self.lastUpdated
        res['is_tracked_all_pincode']=self.isTrackedAllPin
        return str(res)


def addDistrict(dist_id, dist_name='districtName',isTracked=False):
    print('*'*80)
    print('Adding District {} with  id {} '.format(dist_name,dist_id))
    print('*'*80)
    lastUpdated=common_util.getUtcTimeStamp()
    try:
        session = Session()
        res, isexist = isDistExist(dist_id)
        if isexist == False:
            print('-'*80)
            print("District ",dist_id,"NOT EXIST IN DB ")
            temp_p = District()
            temp_p.district_name=dist_name
            temp_p.district_id=int(dist_id)
            temp_p.isTrackedAllPin=isTracked
            temp_p.lastUpdated=lastUpdated
            print(temp_p)
            session.add(temp_p)
            session.commit()
            session.close()
            print('-'*80)

            return 'District added SuccessFully', True
        else:
            print("District  ",dist_id,"EXIST IN DB")

            return 'District Exist in DB ', False

    except Exception as e:

        return 'Exception -->{} '.format(e), False

    finally:
        session.close()


def isDistExist(dist_id):
    try:
        session = Session()
        res = session.query(District).filter(District.district_id == dist_id).first()
        if res==None:
            raise Exception
        return res, True
    except Exception as e:
        return 'Not Found e->{}'.format(e), False
    finally:
        session.close()


def getAllDistricts():
    try:
        session = Session()
        districts = session.query(District).order_by(District.lastUpdated).all()
        datas = {}
        lst = []
        for dist in districts:

            lst.append(dist)

        datas['districts'] = lst
        datas['total'] = len(datas['districts'])


        return datas, True

    except Exception as e:
        return "Exception occurred {}".format(e), False

    finally:
        session.close()

def getAllDistWithoutTracked():
    try:
        session = Session()
        districts = session.query(District).filter(District.isTrackedAllPin==False).order_by(District.lastUpdated).all()
        datas = {}
        lst = []
        for dist in districts:
            lst.append(dist)

        datas['districts'] = lst
        datas['total'] = len(datas['districts'])


        return datas, True

    except Exception as e:
        return "Exception occurred {}".format(e), False

    finally:
        session.close()

def trackComplete(dist_id):
    try:
        
        session = Session()
        district = session.query(District).filter(District.district_id==dist_id).first()
        district.lastUpdated=common_util.getUtcTimeStamp()
        district.isTrackedAllPin=True

        session.add(district)
        session.commit()

        return 'Districts All pin tracked successfully',True

    except Exception as e:
        return "Exception occurred {}".format(e), False

    finally:
        session.close()

def updateLastUpdated(dist_id):
    try:
        session = Session()
        Obj = session.query(District).filter(District.district_id == dist_id).first()
        if Obj==None:
            raise Exception
        Obj.lastUpdated=common_util.getUtcTimeStamp()
        session.add(Obj)
        session.commit()
        
        return "Updated LastUpdated Successfully", True
    except Exception as e:
        return 'Not Found e->{}'.format(e), False
    finally:
        session.close()


def removeUnTaggedDistricts():
    try:
        session=Session()
        alldist,_=getAllDistricts()

        print(alldist)

        for dist in alldist['districts']:
            print(dist.district_id)
            allUsers,_=user_model.getUserofDistID(dist.district_id)
            print(allUsers)
            if allUsers['total']<1:
                print("Remove ",dist.district_id, " as no user is tagged to this dist id")
                session.delete(dist)
    except :
        return False
    finally:
        session.commit()
        session.close()




Base.metadata.create_all(bind=engine)
