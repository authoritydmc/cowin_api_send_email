from cowin_get_email.databases import center_model
from cowin_get_email.utility import session_util

def processCenter(center):
    # this receives center JSON and process it
    print("Processing Center-> ",center)
    res,_=center_model.addCenter(center['center_id'], center['name'], center['address'], center['pincode'], center['fee_type'], center['block_name'])
    print("Result of processing {} is {} ".format(res,_))
    input("Press Key")
    # now process its Session.
    session_util.processSessions(center['sessions'],center['center_id'])
    

    return True

