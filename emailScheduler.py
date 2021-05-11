print("Email Scheduler Called")
from cowin_get_email.utility import district_util

print('*'*30,'from Email Scheduler','*'*35)

# send email to all District based Receipeint.


# step 1 :Gather All Districts



print("All District->",district_util.getListofDistrictIds())



print('*'*30,'End Email Scheduler','*'*35)