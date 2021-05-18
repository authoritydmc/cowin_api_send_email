print("Email Scheduler Called")
from cowin_get_email.utility import email_util

print('*'*30,'from Email Scheduler','*'*35)
# send email to all District based Receipeint.


email_util.DistrictMailer()

email_util.PincodeBasedUserMailer()
print('*'*30,'End Email Scheduler','*'*35)