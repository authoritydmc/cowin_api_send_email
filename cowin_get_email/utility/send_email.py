import smtplib, ssl
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os



f=open('setup.cred','r')
cred=json.load(f)
f.close()

print("Loading env")
patht='%s/email_templates/' % os.path.dirname(__file__)
print("PATH-->",patht)
env = Environment(loader=FileSystemLoader(patht))

smtp_server = "smtp.gmail.com"
port = 587  # For starttlss
# print(cred['email'])
sender_email=cred['email']
testReceiver_email=cred['testreceiver']
def sndEmail(rec_email,subject,body):


    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    print("Sending Email to ",recipient_email)
    # Create a secure SSL context
    context = ssl.create_default_context()
    server=None
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, cred['password'])

        msgc = MIMEText(body, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(msgc)


        server.sendmail(sender_email,rec_email,message.as_string())
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


        
