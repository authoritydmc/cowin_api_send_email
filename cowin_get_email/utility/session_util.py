from cowin_get_email.databases import session_model

def addSessions(sid, cid, min_age, available, slots, date, vaccine_name):
    return  session_model.addSessions(sid, cid, min_age, available, slots, date, vaccine_name)


def processSessions(sessions,centerID):
    # this receives Sessions json and process it
    # session is list of json object

    print("Processing Center ",centerID)


    for session in sessions:
        res,_=addSessions(session['session_id'],centerID,session['min_age_limit'],session['available_capacity'],session['slots'],session['date'],session['vaccine'])
        print("Session->[{}] response->[{}] isSucess=[{}]".format(session,res,_))
        
