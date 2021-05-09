
from cowin_get_email.databases import district_model,pincode_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util,api
import logging
import json
# sample URL

# https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=654&date=08-05-2021


print('District_util Called')
def getUrl(dist_id):
    date_ = common_util.getDate()


    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}'.format(
        dist_id, date_)
    return url

def trackAllPin():
    data,res=district_model.getAllDistWithoutTracked()
    if res:
        for dist_data in data['districts']:
            print( dist_data.district_id)
            trackPinofDist(dist_data.district_id)



def trackPinofDist(dist_id):
    print('*'*80)
    furl = getUrl(dist_id)
    print(furl)
    print('*'*80)

    try:
        res = requests.get(furl,headers=api.headers)
        print(res.status_code)
        response = res.json()
        logging.info(response)
        print('*'*80)
        print('Response from Calender Search of District')
        print(response)
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
    for center in response['centers']:
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



        

       

