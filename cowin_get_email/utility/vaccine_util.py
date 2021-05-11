from cowin_get_email.databases import vaccine_model,pincode_model,district_model
import requests
from datetime import datetime
from cowin_get_email.utility import common_util,api,pincode_util,district_util
import logging
import json


print('Vaccine Util is Called ')


def addVaccineByDistrict():
    # this method will call addVaccineByPincode for each of the Districts
    allDistricts=district_util.getListofDistrictIds()
    for districtid in allDistricts:

        distToPincodeCnvt(districtid)
    print('*'*80)


def addVaccineByPincode():
    pincodes=pincode_util.getListofPincodesWithoutDistricts()

    print('*'*80)
    for pin in pincodes:
        print("PIN-->",pin)
        response,isSuccess=pincode_util.getCalendarByPincode(pin)
        if isSuccess:
            addVaccine(pin,response['result'])
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
    print("Data from VaccineDataDecryption",end="-->")
    for vaccine in vaccines['vaccines']:
        print(vaccine.pincode,common_util.decodestr(vaccine.res_str))


def distToPincodeCnvt(dist_id):
    pincodes=pincode_util.getListofPincodeBydist_id(dist_id)
    print("All available pincode in dist ",dist_id)
    print(pincodes)
    # now get the calendarbyDistrict()
    dataStorer={}


    response,isSuccess=district_util.getCalendarByDistrict(dist_id)
    if isSuccess:
        # print("Dist UTil response -->",response)
        Allcenters=None
        try:
            Allcenters=response['result']['centers']
        except KeyError:
            print("Exception Occured for {} while Fetching data from server")
            return "Error Fetching Data",False

        print("Type of ",type(Allcenters))
        for center in Allcenters:

            # print("Current Center is ",center)
            # print("Its pincode is ",center['pincode'])
            lst=dataStorer.get(center['pincode'],None)
            if lst==None:
                dataStorer[center['pincode']]=[]
                dataStorer[center['pincode']].append(center)
                # print("Currently No key with Pincode ",center['pincode'])
                # print("Hence Adding to New List")
            else:
                # print("Pincode ",center['pincode'] ,'already Exist hence adding it to existing')

                lst.append(center)
            # print("Currenly Value of ",center['pincode'], " \t",dataStorer[center['pincode']])
            # print("currently  Items cnt ->",len(dataStorer[center['pincode']]))
            # input("Press Key to Continue")
        print("$$"*40)
        print("now printing All Seperated Datas")

        for k,v in dataStorer.items():
            print('&'*100)
            finalPresent={}
            finalPresent['centers']=v
            finalPresent['total']=len(v)
            finalPresent['pincode']=k
            addVaccine(k,finalPresent)
            print('&'*100)

        print("$$"*40)

        return "All District "+dist_id+ "based Vaccine Added",True

