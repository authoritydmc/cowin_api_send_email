from cowin_get_email.databases import district_model,pincode_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util,api,center_util
import logging
import json
import config
# sample URL

print('Pincode Util is Called ')

def getCowinApiUrl(pincode):
    url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'.format(pincode,common_util.getDate())
    return url


def getUrl(pincode):
    if config.TEST_DATA_API==True:
        pincode=-1
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

def getListofPincodesWithoutDistricts():

    data,isSuccess=pincode_model.getAllPincodeWithoutDistricts()
    lst=[]
    if isSuccess:
        for pin in data['pincodes']:
            lst.append(pin.pincode)
    
    return lst

def updateLocalUpdate(pincode):
    print(pincode_model.updateLastUpdated(pincode))


def populatePincodeBased():
    # getALL Pincodes
    x= getListofPincodesWithoutDistricts()

    print("All Pincodes without District ID are-> ",x)

    for pin in x:
        res,isSuccess=getCalendarByPincode(pin)

        if isSuccess:
            # print("Resposne {} ->{}".format(pin,res))

            # now process this data
            for center in res['result']['centers']:
                print("$"*40)
                print(center)
                print("$"*40)
                isProcessed=center_util.processCenter(center)

            # update local Update of this Pincode.
            updateLocalUpdate(pin)

def getPincodeByID(pincode):
    x,_=pincode_model.isPincodeExist(pincode)
    if _:
        return x
    else :
        return None