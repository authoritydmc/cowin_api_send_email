from cowin_get_email.databases.database import Base,engine,Session
from sqlalchemy import Column,Integer,String,DateTime
from datetime import  datetime



class User(Base):
    __tablename__ = "USER"
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


def addUser(name, age, email, phone, search_by,pincode ,dist_id=0,dist_name='NA'):
    session=Session()
    
    user = User()
    user.name = name
    user.age = age
    user.phone = phone
    user.email = email
    user.search_by = search_by
    user.pincode = pincode
    user.dist_id = dist_id
    user.dist_name=dist_name
    _,isExist=isUserExist(email,session)
    if isExist==False:
        session.add(user)
        session.commit()
        session.close()
        return 'Added SuccessFully',True
    else:
        session.close()
        return 'User already exists with Email Id ',False

def isUserExist(email,session=None):
    try:
        if session==None:
            session=Session()
        res= session.query(User).filter(User.email==email).first()
        return '{} {} {}'.format(res.name,res.email,res.age),True
    except Exception as e:
        return 'Not Found e->{}'.format(e),False

def getUser():
    pass

Base.metadata.create_all(bind=engine)
