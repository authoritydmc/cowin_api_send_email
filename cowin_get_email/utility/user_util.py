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
        key,user=generateToken(email)
        send_email.sendLoginEmail(user.email,user.name,key)
        return "Sent Login Mail SuccessFully to "+str(user.email),True

    

def generateToken(email):
    user,_=user_model.isUserExist(email)
    if _:
        # generate the s3cetkey
        key=common_util.getToken()
        # store this key
        print("Generated Key->",key)
        msg,isStored=user_pref_model.storeToken(email,key)
        return key,user

def tokenGetter(email):
    usrP,found=user_pref_model.getPreference(email)
    print("$"*80)
    print("For email->",email)
    if found:
        print("Found token ->", usrP.token)
        return usrP.token
    else:
        print("gen new token as it doesnt exist")
        token,user=generateToken(email)
        return token
        