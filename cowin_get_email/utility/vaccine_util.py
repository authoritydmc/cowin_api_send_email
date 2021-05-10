from cowin_get_email.databases import vaccine_model,pincode_model,district_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util,api,pincode_util
import logging
import json


print('Vaccine Util is Called ')


def addVaccineByDistrict(dist_id):
    # this method will call addVaccineByPincode for each of the pincodes
    pass

def addVaccineByPincode():
    allPincodes,_=pincode_model.getAllPincodeWithoutDistricts()

    print('*'*80)
    for pin in allPincodes['pincodes']:
        print("PIN-->",pin.pincode)
        response,isSuccess=pincode_util.getCalendarByPincode(pin.pincode)
        if isSuccess:
            addVaccine(pin.pincode,response['result'])
    print('*'*80)



def addVaccine(pincode,res_str):
    print('*'*80)
    print('Adding Vaccine for ',pincode)
    print('*'*80)
    # base64 encrypting the result
    ds=common_util.encodestr(str(res_str))

    return vaccine_model.addVaccine(pincode,ds)

def VaccineDataDecrypted():
    vaccines,_=vaccine_model.getAllVaccineRecords()

    for vaccine in vaccines['vaccines']:
        print(vaccine.pincode,common_util.decodestr(vaccine.res_str))
