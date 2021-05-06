from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

print('database.py called')
dbv='database.py var'
engine = create_engine("sqlite:///db.sqlite3", echo=True,connect_args={'check_same_thread':False})


Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()


def addUser(name, age, email, phone, search_by,pincode ,dist_id=0,dist_name='NA'):
    from cowin_get_email.databases.user_model import addUser
    
    
    return addUser(name, age, email, phone, search_by,pincode ,dist_id,dist_name)

def isUserExist(email):
    from cowin_get_email.databases.user_model import isUserExist

    return  isUserExist(email)

def getAllUser():
    from cowin_get_email.databases.user_model import getUsers
    return getUsers()