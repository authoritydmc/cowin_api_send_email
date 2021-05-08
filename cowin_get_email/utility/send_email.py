import smtplib, ssl
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os
import logging

from config import prod_config,local_config

envrn=prod_config.environment
EMAIL=''
EMAIL_PASSWORD=''

if envrn==None:
    # it is local envrn
    lc=local_config()
    EMAIL=lc.sender_email
    EMAIL_PASSWORD=local_config.password
    logging.info('sendemail.py called in Local environment')

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
        print('Exception occurred',e)
    finally:
        if server!=None:
            server.quit() 

def sendWelcomeEmail(name,rec_email,selectby,pincode,dist_name):
        subject='Welcome '+name
        template = env.get_template('email_welcome.html')
        sdata=pincode if selectby=='pincode' else dist_name
        msg= template.render(name=name,selectby=selectby,search_data=sdata)
        sndEmail(rec_email,subject,msg)


        
