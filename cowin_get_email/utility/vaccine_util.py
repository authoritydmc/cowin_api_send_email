from cowin_get_email.databases import vaccine_model,pincode_model,district_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util,api
import logging
import json

print('Vaccine Util is Called ')


def addVaccineByDistrict(dist_id):
    # this method will call addVaccineByPincode for each of the pincodes
    pass

def addVaccineByPincode():
    allPincodes=pincode_model.getAllPincodeWithoutDistricts()

    print('*'*80)
    for pin in allPincodes:
        print("To find for -> ",pin)
    print('*'*80)



def addVaccine(pincode,res_str):
    # final method to add Vaccine
    pass


addVaccineByPincode()