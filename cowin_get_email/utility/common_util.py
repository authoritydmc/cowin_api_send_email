from datetime import  datetime
import os,time
from datetime import timezone



def getDate():
    os.environ['TZ'] = 'Asia/Calcutta'
    time.tzset()
    return datetime.today().strftime('%d-%m-%Y')

def getUtcTimeStamp():
    dt = datetime.now(timezone.utc)
    
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    
    return int(utc_timestamp)