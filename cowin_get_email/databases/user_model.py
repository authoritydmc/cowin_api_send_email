from cowin_get_email.databases.database import Base,engine,Session
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from datetime import  datetime
import json
from cowin_get_email.utility import common_util
metadata = Base.metadata
# Valid search_by values = pincode or district


class User(Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    phone = Column('phone', String)
    email = Column('email', String, unique=True)
    age = Column('age', Integer, default=0)
    pincode = Column('pincode', Integer, default=-1)
    dist_id = Column('dist_id', Integer, default=-1)
    dist_name = Column('dist_name', String, default="NA")
    registered = Column('registered', DateTime, default=datetime.now)
    search_by = Column('search_by', String)
    secret_key=Column('secret_key',String,default="NA")
    state_id=Column(Integer,default=-1)
    dose_no=Column(Integer,default=1)
    receive_email=Column(Boolean,default=True)
    def __repr__(self):

        returnData={}
        returnData['name']=self.name
        returnData['email']=self.email
        returnData['age']=self.age
        returnData['search_by']=self.search_by
        returnData['dist_id']=self.dist_id
        returnData['state_id']=self.state_id
        returnData['dose_no']=self.dose_no
        returnData['pincode']=self.pincode
        return json.dumps(returnData)

def addUser(name, age, email, phone,dose_no, search_by,pincode,state_id=-1 ,dist_id=-1,dist_name='NA'):
    session=Session()
    
    user = User()
    user.name = name
    user.age = int(age)
    user.phone = phone
    user.email = email
    user.dose_no=dose_no
    user.search_by = search_by
    if user.search_by=='pincode':
        user.pincode = int(pincode)
    else:
        user.dist_id = int(dist_id)
        user.dist_name=dist_name
        user.state_id=int(state_id)

    user.secret_key=common_util.getToken()+common_util.getToken()
    _,isExist=isUserExist(email)
    if isExist==False:
        session.add(user)
        session.commit()
        session.close()
        return 'Added SuccessFully',True
    else:
        session.close()
        return 'User already exists with Email Id ',False

def isUserExist(email):
    try:
        session=Session()
        res= session.query(User).filter(User.email==email).first()
        if res==None:
            return "Not found ",False
        return res,True
    except Exception as e:
        return 'Not Found e->{}'.format(e),False
    finally:
        session.close()

def getUsers():
    try:
        session=Session()
        users=session.query(User)
        datas={}
        userslst=[]
        for user in users:
            userslst.append(user)
            
        datas['users']=userslst
        datas['total']=len(datas['users'])
        print(datas)

        return datas,True



    except Exception as e:
        return "Exception occurred {}".format(e),False
    
    finally:
        session.close()


def getUsersWithPincodeSelectBy():
    try:
        session=Session()
        users=session.query(User).filter(User.search_by=="pincode").all()
        datas={}
        userslst=[]
        for user in users:
            userslst.append(user)
            
        datas['users']=userslst
        datas['total']=len(datas['users'])

        return datas,True



    except Exception as e:
        return "Exception occurred {}".format(e),False
    
    finally:
        session.close()


def getUserofDistID(distID):
    try:
        session=Session()
        users=session.query(User).filter(User.dist_id==distID).all()
        datas={}
        userslst=[]
        for user in users:
            userslst.append(user)
            
        datas['users']=userslst
        datas['total']=len(datas['users'])
    
        return datas,True



    except Exception as e:
        return "Exception occurred {}".format(e),False
    
    finally:
        session.close()


def getUsersofPincode(pincode):
    try:
        session=Session()
        users=session.query(User).filter(User.pincode==pincode).all()
        datas={}
        userslst=[]
        for user in users:
            userslst.append(user)
            
        datas['users']=userslst
        datas['total']=len(datas['users'])
        print(datas)

        return datas,True



    except Exception as e:
        return "Exception occurred {}".format(e),False
    
    finally:
        session.close()


def updateUser(name, age, email, phone,dose_no, search_by,pincode ,state_id=-1,dist_id=-1,dist_name='NA'):
    session=Session()
    
    user ,_= isUserExist(email)
    if _!=True:
        return "Failed to Update the Details as user doesnt exist",False
    user.name = name
    user.age = int(age)
    user.phone = phone
    user.dose_no=dose_no
    user.search_by = search_by
    user.pincode = int(pincode) if user.search_by=='pincode' else -1
    user.dist_id = int(dist_id) if user.search_by=='district' else -1
    user.state_id = int(state_id) if user.search_by=='district' else -1
    user.dist_name=dist_name  if user.search_by=='district' else 'NA'
    session.add(user)
    session.commit()
    session.close()
    return 'Added SuccessFully',True


def stopReceivingMail(email):

    session=Session()
    user ,_= isUserExist(email)
    if _!=True:
        return "Failed to Update the Details as user doesnt exist",False
    user.receive_email=False

    session.add(user)
    session.commit()
    session.close()


def startReceivingMail(email):
    session=Session()
    user ,_= isUserExist(email)
    if _!=True:
        return "Failed to Update the Details as user doesnt exist",False
    user.receive_email=True

    session.add(user)
    session.commit()
    session.close()


Base.metadata.create_all(bind=engine)
