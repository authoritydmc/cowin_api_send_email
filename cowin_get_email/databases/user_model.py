from cowin_get_email.databases.database import Base,engine,Session
from sqlalchemy import Column,Integer,String,DateTime
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
    pincode = Column('pincode', Integer, default=0)
    dist_id = Column('dist_id', Integer, default=0)
    dist_name = Column('dist_name', String, default="NA")
    registered = Column('registered', DateTime, default=datetime.now)
    search_by = Column('search_by', String)
    secret_key=Column('secret_key',String,default="NA")

    def __repr__(self):

        returnData={}
        returnData['name']=self.name
        returnData['email']=self.email
        returnData['age']=self.age
        returnData['search_by']=self.search_by
        returnData['dist_id']=self.dist_id
        returnData['pincode']=self.pincode
        return json.dumps(returnData)

def addUser(name, age, email, phone, search_by,pincode ,dist_id=0,dist_name='NA'):
    session=Session()
    
    user = User()
    user.name = name
    user.age = int(age)
    user.phone = phone
    user.email = email
    user.search_by = search_by
    user.pincode = int(pincode) if user.search_by=='pincode' else 0
    user.dist_id = int(dist_id) if user.search_by=='district' else 0
    user.dist_name=dist_name  if user.search_by=='district' else 'NA'
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
        print(datas)

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


def updateUser(name, age, email, phone, search_by,pincode ,dist_id=0,dist_name='NA'):
    session=Session()
    
    user ,_= isUserExist(email)
    if _!=True:
        return "Failed to Update the Details as user doesnt exist",False
    user.name = name
    user.age = int(age)
    user.phone = phone
    user.search_by = search_by
    user.pincode = int(pincode) if user.search_by=='pincode' else -1
    user.dist_id = int(dist_id) if user.search_by=='district' else -1
    user.dist_name=dist_name  if user.search_by=='district' else 'NA'
    session.add(user)
    session.commit()
    session.close()
    return 'Added SuccessFully',True





Base.metadata.create_all(bind=engine)
