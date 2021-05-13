from cowin_get_email.databases import user_model,user_pref_model
from datetime import datetime
from cowin_get_email.utility import common_util,api,send_email
import logging
import json
import config


def getUserOfDistId(distID):

    x,_= user_model.getUserofDistID(distID)
    return x

def getListofUserSearchingByPincode(pincode):
    x,_=user_model.getUsersofPincode(pincode)
    return x

def getAllUsersSearchingByPincode():
    x,_=user_model.getUsersWithPincodeSelectBy()
    return x

def generateLoginofUser(email):

    user,_=user_model.isUserExist(email)
    if _:
        # generate the s3cetkey
        key=common_util.getToken()
        # store this key
        print("Generated Key->",key)
        msg,isStored=user_pref_model.storeToken(email,key)
        send_email.sendLoginEmail(user.email,user.name,key)
        return "Send Mail SuccessFully",True
    else:
        "Unable to send Mail",False
    
