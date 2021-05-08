from datetime import  datetime
import os,time



def getDate():
    os.environ['TZ'] = 'Asia/Calcutta'
    time.tzset()
    return datetime.today().strftime('%d-%m-%Y')
