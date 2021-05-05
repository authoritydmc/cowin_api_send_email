import requests
import json
from . import model


base_url='https://cdn-api.co-vin.in/api'

def getStates():
    # returns StateName and StateID
    api_url='/v2/admin/location/states'
    print("Getting All States")
    states={}
    try: 
        # raising Exception to use Local States.json.
        raise Exception
        res=requests.get(base_url+api_url)
        print("Response Code ",res.status_code)
        response=res.json()
        for state in response['states']:
            states[state['state_id']]=state['state_name']

    except Exception as e:
        print('Exception occured While fetching States List ',e)
        f=open('cowin_get_email/utility/states.json','r')
        res=json.load(f)
        print(res)
        for state in res['states']:
            states[state['state_id']]=state['state_name']

        f.close()

    return states




    


