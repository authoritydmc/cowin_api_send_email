import requests
import json
from cowin_get_email.utility import model


base_url='https://cdn-api.co-vin.in/api'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


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

        for state in res['states']:
            states[state['state_id']]=state['state_name']

        f.close()

    return states




    


