import os
import json
import setup
class prod_config:
    sender_email=os.environ.get('email',None)
    DB_URI=os.environ.get('sqlite:///dblocal.sqlite3',None)
    password=os.environ.get('password',None)
    environment=os.environ.get('environment',None)


class local_config:
        sender_email=setup.email
        DB_URI="sqlite:///dblocal.sqlite3"
        password=setup.password
        environment='local'



print(local_config.sender_email)
