from cowin_get_email.databases import vaccine_model,pincode_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util,api
import logging
import json

print('Vaccine Util is Called ')


def addVaccineByDistrict(dist_id):
    # this method will call addVaccineByPincode for each of the pincodes
    pass

def addVaccineByPincode(pincode,res_str):
    pass
# this method will populate Vaccine Data with Pincode ,res_str

