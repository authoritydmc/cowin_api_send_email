import smtplib, ssl
import json
from datetime import datetime

f=open('setup.cred','r')
cred=json.load(f)
smtp_server = "smtp.gmail.com"
port = 587  # For starttlss
print(cred['email'])
sender_email=cred['email']
receiver_email='authoritydmc@gmail.com'
message='Test Mail 77 '
# Create a secure SSL context
context = ssl.create_default_context()
server=None
try:
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, cred['password'])
    server.sendmail(sender_email,receiver_email,message+str(datetime.now))
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    if server!=None:
        server.quit() 
f.close()
