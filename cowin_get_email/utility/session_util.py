from cowin_get_email.databases import session_model

def addSessions(sid, cid, min_age, available, slots, date, vaccine_name):
    if available>0:
        return  session_model.addSessions(sid, cid, min_age, available, slots, date, vaccine_name)
    else:
        return "Skipped as available is 0",True


def processSessions(sessions,centerID):
    # this receives Sessions json and process it
    # session is list of json object

    print("Processing Center ",centerID)


    for session in sessions:
        res,_=addSessions(session['session_id'],centerID,session['min_age_limit'],session['available_capacity'],session['slots'],session['date'],session['vaccine'])
        print("Session->[{}] response->[{}] isSucess=[{}]".format(session,res,_))
        

def getListofSessionByCenter(centerID):
    x,_= session_model.getSessionByCenter(centerID)
    if _==True:
        return x
    else :
        return []
 