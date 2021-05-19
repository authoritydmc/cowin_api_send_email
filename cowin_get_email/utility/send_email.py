import smtplib, ssl
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os
import logging
from cowin_get_email.utility import common_util,pincode_util,district_util,user_util,session_util
from cowin_get_email.databases import user_pref_model
from config import prod_config,local_config,checkENV

envrn=prod_config.environment
EMAIL=''
EMAIL_PASSWORD=''
baseURL='https://cowin-track.herokuapp.com/'
if checkENV()=='LOCAL':
    # it is local envrn
    lc=local_config()
    EMAIL=lc.sender_email
    EMAIL_PASSWORD=local_config.password
    logging.info('sendemail.py called in Local environment')
    baseURL="http://127.0.0.1:5000/"

else:
    EMAIL=prod_config.sender_email
    EMAIL_PASSWORD=prod_config.password

    logging.info('sendemail.py called in Prod environment')



print("Loading env")
patht='%s/email_templates/' % os.path.dirname(__file__)
print("PATH-->",patht)
env = Environment(loader=FileSystemLoader(patht))

smtp_server = "smtp.gmail.com"
port = 587  


def sndEmail(rec_email,subject,body):


    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = EMAIL
    message["To"] = rec_email

    print("Sending Email to ",rec_email)
    # Create a secure SSL context
    context = ssl.create_default_context()
    server=None
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(EMAIL, EMAIL_PASSWORD)

        msgc = MIMEText(body, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(msgc)


        server.sendmail(EMAIL,rec_email,message.as_string())
        print("Mail sent ")
    except Exception as e:
        # Print any error messages to stdout
        print('Exception occurred while sending Mail',e)
    finally:
        if server!=None:
            server.quit() 

def sendWelcomeEmail(user):
        subject='Welcome '+user.name
        template = env.get_template('email_welcome.html')
        sdata=user.pincode if user.search_by=='pincode' else user.dist_name
        token=user_util.tokenGetter(user.email)
        msg= template.render(name=user.name,selectby=user.search_by,search_data=sdata,email=user.email,token=token,dose_no=user.dose_no)
        sndEmail(user.email,subject,msg)

def sendChangeSearchMethod(user):
        subject='Important [change your search method] '+user.name
        template = env.get_template('noCenterDetail.html')
        sdata=user.pincode if user.search_by=='pincode' else user.dist_name
        token=user_util.tokenGetter(user.email)
        msg= template.render(name=user.name,selectby=user.search_by,search_data=sdata,email=user.email,token=token)
        sndEmail(user.email,subject,msg)


def sendDailyReminder(centerLst,sessionList,UserList):
    

    print("Called sendDaiilyReminder ")

    subject='Daily Slots [{}] '.format(common_util.getDate())
    template = env.get_template('daily_reminder.html')

   
    print("@"*80)
    print(UserList)
    print("@"*80)


    for user in UserList['users']:
        emailData={}
        emailData['centers']=centerLst
        emailData['date']=common_util.getDate()
        emailData['name']=user.name
        emailData['age']=user.age
        search_data=user.pincode if user.search_by=="pincode" else user.dist_name
        emailData['search_by']=user.search_by
        emailData['search_data']=search_data
        emailData['email']=user.email
        emailData['url']=''
        if user.search_by=="pincode":
            emailData['url']=pincode_util.getCowinApiUrl(search_data)
        else:
            emailData['url']=district_util.getCowinApiUrl((user.dist_id))
        
        emailData['token']=user_util.tokenGetter(user.email)
        validSession={}
        print("Currently Working to Send Mail to ->{} of age {}".format(user.email,user.age))
        print('%'*80)

        print(sessionList)
        print('%'*80)

        for center_id,center_data in sessionList.items():
            # only Valid Vaccines Are which has more than 0 available cap and age > min_age
            # print("{} has Vaccine avilable to {} and its cap->{}".format(sdata.session_id,sdata.min_age,sdata.available))
            print("For center ->",center_id,"its data->",center_data)
            for sdata in center_data:
                print("for data->",sdata)
                if user.age>sdata.min_age and sdata.available>0:
                    print("Its valid session".upper())
                    session_util.updatePrevCnt(sdata.session_id)

                    # TODO : change this or to and in PROD 
                    # valid Vaccine Add it to Valid sessions
                    sls=validSession.get(center_id,None)
                    if sls==None:
                        print("No prior list item found")
                        validSession[center_id]=[sdata]
                    else:
                        validSession[center_id].append(sdata)
                else:
                    print("Its not valid session".upper())
        
            # print("Final result of processed center->",validSession)
        
        print("Valid Sessions are -> ",validSession)

        emailData['session']=validSession

        print('!'*80)

        print(validSession)
        print('!'*80)

        emailData['total']=len(validSession)

        msg= template.render(data=emailData,cnvrtutcLocal=common_util.getSimpleDatenTimeFromtimeStamp)
        if len(validSession)==0:
            temp_subject=subject+" [No Slots Available]"
        else:
            temp_subject=subject+" [Slots Available]"


        # send the mail
        sndEmail(user.email,temp_subject,msg)






def sendLoginEmail(rec_email,name,key):
        subject='Login @ Cowin Slot Tracker '+name
        print("Sending key->",key)
        template = env.get_template('login_email.html')
    
        msg= template.render(name=name,key=key,baseurl=baseURL,email=rec_email)
        sndEmail(rec_email,subject,msg)

  


def autoMailer(centerList,SessionDic,usersList,pincode):

    print("Called AutoMailer ")

    subject='Slots Available at : [{}] '.format(pincode)
    template = env.get_template('auto_reminder.html')
    # remove duplicate centerDetails:
    centerDIC={}
    print("centerList at -> ",centerList)
    for center in centerList:
        print("center -> ",center.center_id)
        centerDIC[center.center_id]=center

        print("NEW CENTERS---->",centerDIC)

    newCenterList=[]
    for cid,cdata in centerDIC.items():
        newCenterList.append(cdata)



   
    print("@"*80)
    print(usersList)
    print("@"*80)
       
    print("@"*80)
    print("\n\n CenterList->",centerList)
    print("@"*80)

    print("@"*80)
    print("\n\n\n sessionDic->",SessionDic)
    print("@"*80)

    for user in usersList:
        emailData={}
        emailData['centers']=newCenterList
        emailData['date']=common_util.getDate()
        emailData['name']=user.name
        emailData['age']=user.age
        search_data=user.pincode if user.search_by=="pincode" else user.dist_name
        emailData['search_by']=user.search_by
        emailData['search_data']=search_data
        emailData['email']=user.email
        emailData['url']=''
        if user.search_by=="pincode":
            emailData['url']=pincode_util.getCowinApiUrl(search_data)
        else:
            emailData['url']=district_util.getCowinApiUrl((user.dist_id))
        
        emailData['token']=user_util.tokenGetter(user.email)
        validSession={}
        print("Currently Working to Send Mail to ->{} of age {}".format(user.email,user.age))
        print('%'*80)

        for center_id,center_data in SessionDic.items():
            # only Valid Vaccines Are which has more than 0 available cap and age > min_age
            # print("{} has Vaccine avilable to {} and its cap->{}".format(sdata.session_id,sdata.min_age,sdata.available))
            print("\n\nFor center ->",center_id,"its data->",center_data)
            for sdata in center_data:
                print("for data->",sdata)
                if user.age>sdata.min_age and sdata.available>0:
                    print("Its valid session".upper())
                    # TODO : uncomment below line in production
                    session_util.updatePrevCnt(sdata.session_id)

                    # TODO : change this or to and in PROD 
                    # valid Vaccine Add it to Valid sessions
                    sls=validSession.get(center_id,None)
                    if sls==None:
                        print(" list item found")
                        validSession[center_id]=[sdata]
                    else:
                        validSession[center_id].append(sdata)
                else:
                    print("Its not valid session".upper())
        
            # print("Final result of processed center->",validSession)
        
        print("\n\nValid Sessions are -> ",validSession)

        emailData['session']=validSession

        print('!'*80)

        print(validSession)
        print('!'*80)

        emailData['total']=len(validSession)

        msg= template.render(data=emailData,cnvrtutcLocal=common_util.getSimpleDatenTimeFromtimeStamp)
        if emailData['total']>0:
            # send the mail
            sndEmail(user.email,subject,msg)


