from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import prod_config,local_config,checkENV


DB_URL=''
if checkENV()=='LOCAL':
    # it is local envrn
    lc=local_config()
    DB_URL=lc.DB_URI
    print('database.py called in Local environment '+str(DB_URL))

else:
    pc=prod_config()
    DB_URL=pc.DB_URI

    print('database.py called in Prod environment URL->'+str(DB_URL))


engine = create_engine(DB_URL, echo=True,connect_args={'check_same_thread':False})


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

def addPincode(pin,dist_id=-1):
    from cowin_get_email.databases.pincode_model import addPincode

    return addPincode(pin,dist_id)

def isPincodeExist(pincode):
    from cowin_get_email.databases.pincode_model import isPincodeExist
    return isPincodeExist(pincode)

def getAllPincode():
    from cowin_get_email.databases.pincode_model import getAllPincodes
    return getAllPincodes()

def addVaccine(vaccine,pincode, min_age, fee, available_vaccine_cap, center_id, center_name, center_address,date_avail,previous_cap=-1):
    from cowin_get_email.databases.vaccine_model import  addVaccine

    return addVaccine(vaccine,pincode, min_age, fee, available_vaccine_cap, center_id, center_name, center_address,date_avail,previous_cap)

def getVaccineByPincode(pincode):
    from cowin_get_email.databases.vaccine_model import  getVaccineByPincode

    return getVaccineByPincode(pincode)

def getAllVaccines():
    from cowin_get_email.databases.vaccine_model import  getAllVaccineRecords
    return getAllVaccineRecords()


def addDistrict(dist_id,dist_name,track=False):
    from cowin_get_email.databases.district_model import addDistrict
    return addDistrict(dist_id=dist_id,dist_name=dist_name,isTracked=track)

def getAllDistrictWithoutTracked():
    from cowin_get_email.databases.district_model import getAllDistWithoutTracked
    return getAllDistWithoutTracked()

def getAllDistricts():
    from cowin_get_email.databases.district_model import getAllDistricts
    return getAllDistricts()


    




