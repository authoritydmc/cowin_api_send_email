from cowin_get_email.databases.database import Base,engine,Session
from sqlalchemy import Column,Integer,String,DateTime
from datetime import  datetime



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

    def __repr__(self):
        sbl=''
        if self.search_by=='pincode':
            sbl=self.pincode
        else:
            sbl=self.dist_name
        return '<div style="border:1px solid green;padding:10px;"> <b>{}</b> residing at  <b>{} </b> , aged <b>{}</b> and email <b>{}</b> is searching by <b>{}</b> </div>'.format(self.name,sbl,self.age,self.email,self.search_by)


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
        return '{} {} {}'.format(res.name,res.email,res.age),True
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


    pass



Base.metadata.create_all(bind=engine)
