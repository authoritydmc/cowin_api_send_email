from datetime import  datetime
import os,time
from datetime import timezone
import base64
import secrets
import random


def getDate():
    os.environ['TZ'] = 'Asia/Calcutta'
    time.tzset()
    return datetime.today().strftime('%d-%m-%Y')

def getUtcTimeStamp():
    dt = datetime.now(timezone.utc)
    
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    
    return int(utc_timestamp)

def encodestr(dd):
    db=dd.encode('ascii')
    fd=base64.b64encode(db)

    return fd.decode('ascii')

def decodestr(ed):
    eb=ed.encode('ascii')
    fd=base64.b64decode(ed)
    fd=fd.decode('ascii')
    return fd


def getPythonDictofStr(x):
    x="{"+x[1:-1]+"}"

        # j=json.loads(x)
    j=eval(x)

    return j


def getSimpleDatenTimeFromtimeStamp(timeStamp):
    os.environ['TZ'] = 'Asia/Calcutta'
    time.tzset()
    x=datetime.fromtimestamp(timeStamp)
    return x.strftime('%d-%m-%Y %I:%M:%S %p')

def getToken():
    numbers="0123456789"
    seq=""
    for i in range(6):
        seq+=random.choice(numbers)
    return secrets.token_urlsafe()+str(seq)

