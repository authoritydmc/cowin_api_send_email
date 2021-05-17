from cowin_get_email.databases.database import Base,engine,Session
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from datetime import  datetime
import json

# Valid search_by values = pincode or district


class UserPref(Base):
    __tablename__ = "users_pref"
    email = Column(String,primary_key=True )
    lastLogin=Column(Integer,default=0)
    token=Column(String,default="NA")
    login_attempt_cnt=Column(Integer,default=0)
    
    


    def __repr__(self):

        returnData={}
        returnData['email']=self.email

        return json.dumps(returnData)



def getPreference(email):
    try:
        session=Session()
        res= session.query(UserPref).filter(UserPref.email==email).first()
        if res==None:
            return None,False
        return res,True
    except Exception as e:
        return 'Not Found e->{}'.format(e),False
    finally:
        session.close()


def storeToken(email,newToken):
    try:
        session=Session()
        user,isExist=getPreference(email)
        if isExist==False:
            user=UserPref()
        user.token=newToken
        user.email=email
        session.add(user)
        session.commit()
        print("Stored key in db->",newToken)
        return "token added Successfully",True
    except Exception as e:
        return "error occured While saving token "+str(e),False
    finally:
        session.close()

def matchToken(email,tokenfromUser):
    try:
        session=Session()
        user,isExist=getPreference(email)
        if isExist==False:
            return "User Doesnot Exist",False
        
        if user.email==email and user.token==tokenfromUser and user.token!="NA":
            return "Validated Successfully ",True
        else:
            return "Failure to Validate Token",False
    except Exception as e:
        return "error occured While saving token "+str(e),False
    finally:
        session.close()







Base.metadata.create_all(bind=engine)
