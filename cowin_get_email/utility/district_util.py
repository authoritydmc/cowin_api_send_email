
from cowin_get_email.databases import district_model,pincode_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util,api
import logging
import json
import config
# sample URL

# https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=654&date=08-05-2021


print('District_util Called')
def getUrl(dist_id):

    if config.TEST_DATA_API==True:
        dist_id=-1
    url='https://n3wq0c30m2.execute-api.ap-south-1.amazonaws.com/default/cowin_gateway?endPoint=calendarByDistrict&data='+str(dist_id)
    
    
    return url

def trackAllPin():
    data,res=district_model.getAllDistWithoutTracked()
    if res:
        for dist_data in data['districts']:
            print( dist_data.district_id)
            trackPinofDist(dist_data.district_id)



def trackPinofDist(dist_id):
    

    try:

        response,_ = getCalendarByDistrict(dist_id)
        logging.info(response)

        _,isSuccess=processDistData(response,dist_id)
        if isSuccess:
            # mark all pin track complete SuccessFul.
            district_model.trackComplete(dist_id)
        else:
            print('Can not Mark All pincode Tracked for ',dist_id)
        print('*'*80)



    except Exception as e:
        logging.error('Exception occured'+str(e))



def processDistData(response,dist_id):
    pincodes=[]
    for center in response['result']['centers']:
                # getting Center as JSON OBJECT..
        # vaccine Details alongwith pincode
        #now only Store Pincodes ..
        pincodes.append(center['pincode'])
    # got all the Pincodes .Now Store it in Pincodes DB
    if len(pincodes)>0:
        for pincode in pincodes:
            pincode_model.addPincode(pincode,dist_id)
            print('*'*80)
            print('Adding ',pincode, ' of ',dist_id)
            print('*'*80)

        return 'All Pincodes Added ',True
    else:
        return 'Pincodes Not Found len(0)',False

def getCalendarByDistrict(dist_id):
    try:
        print("Searching for CalenderByPincode for ",dist_id)
        furl=getUrl(dist_id)
        print("Formed URL->"+furl)
        res = requests.get(furl,headers=api.headers)
        print(res.status_code)
        response = res.json()
        logging.info(response)
        print(response)
 

        return response,True
    except Exception as e:
        return 'Error '+str(e),False
        

       

def getListofDistrictIds():
    # this method will call addVaccineByPincode for each of the Districts
    allDistricts,_=district_model.getAllDistricts()
    lst=[]
    for district in allDistricts['districts']:  
        lst.append(district.district_id)
    return lst