from cowin_get_email.databases import center_model
from cowin_get_email.utility import session_util

def processCenter(center):
    # this receives center JSON and process it
    print("Processing Center-> ",center)
    res,_=center_model.addCenter(center['center_id'], center['name'], center['address'], center['pincode'], center['fee_type'], center['block_name'])
    print("Result of processing {} is {} ".format(res,_))
    # now process its Session.
    session_util.processSessions(center['sessions'],center['center_id'])
    

    return True

def getListOfCenterIDSByPincode(pincode):
    x,isSuc=center_model.getCentersByPincode(pincode)
    lst=[]

    if isSuc:
        for center in x:
            lst.append(center.center_id)
    
    return lst


def getListOfCenterByPincode(pincode):
    x,isSuc=center_model.getCentersByPincode(pincode)
    if isSuc:
        return x
    else:
        return []
