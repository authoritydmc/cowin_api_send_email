from cowin_get_email.databases import district_model,pincode_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util,api
import logging
import json
# sample URL

print('Pincode Util is Called ')


def getUrl(pincode):
    url='https://n3wq0c30m2.execute-api.ap-south-1.amazonaws.com/default/cowin_gateway?endPoint=calendarByPincode&data='+str(pincode)
    return url

def getCalendarByPincode(pincode):
    try:
        print("Searching for CalenderByPincode for ",pincode)
        furl=getUrl(pincode)
        print("Formed URL->"+furl)
        res = requests.get(furl,headers=api.headers)
        print(res.status_code)
        response = res.json()
        logging.info(response)
        print('*'*80)
        print('Response from Calender Search of Pincode ',pincode)
        print(response)
        print('*'*80)

        return response,True
    except Exception as e:
        return 'Error '+str(e),False


def getListofPincodeBydist_id(dist_id):
    data,isSuccess=pincode_model.getPincodesByDistID(dist_id)

    pincodes=[]

    for pincode in data['pincodes']:
        pincodes.append(pincode.pincode)

    return pincodes