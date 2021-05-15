import os
import json
import logging


# Keep it FALSE FOR PRODUCTION
# while testing Use as True

TEST_DATA_API=True 

class prod_config:
    sender_email=os.environ.get('sender_email',None)
    # DB_URI=os.environ.get('DATABASE_URL',None)
    DB_URI=os.environ.get('DB_URL',None)
    secret_key=os.environ.get('secret_key','23s%#34232')
    password=os.environ.get('password',None)
    environment=os.environ.get('environment',None)
    


class local_config:
    try:
        import setup
        sender_email=setup.email
        DB_URI=setup.DATABASE_URL
        password=setup.password
        environment='local'
    except:
        logging.error("Error Occured IN Setting Up local env")

ens=prod_config.environment if prod_config.environment!=None else 'LOCAL'
print("Running in ",ens)

def checkENV():
    return prod_config.environment if prod_config.environment!=None else 'LOCAL'


