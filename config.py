import os
import json
import logging

class prod_config:
    sender_email=os.environ.get('email',None)
    DB_URI=os.environ.get('sqlite:///dblocal.sqlite3',None)
    password=os.environ.get('password',None)
    environment=os.environ.get('environment',None)


class local_config:
    try:
        import setup
        sender_email=setup.email
        DB_URI="sqlite:///dblocal.sqlite3"
        password=setup.password
        environment='local'
    except:
        logging.error("Error Occured IN Setting Up local env")

ens=prod_config.environment if prod_config.environment!=None else 'Local'
print("Running in ",ens)
