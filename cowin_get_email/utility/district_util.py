
from cowin_get_email.databases import district_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util
import logging
import json
# sample URL

# https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=654&date=08-05-2021

print('District_util Called')
def getUrl(dist_id):
    date_ = common_util.getDate()


    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}'.format(
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
        res = requests.get(furl)
        response = res.json()
        logging.info(response)

    except Exception as e:
        logging.error('Exception occured'+str(e))



