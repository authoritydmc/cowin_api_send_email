print('Running Scheduer')

print('*'*30,'from scheduler','*'*35)

from cowin_get_email.utility import district_util,common_util,vaccine_util


district_util.trackAllPin()


vaccine_util.addVaccineByPincode()

# vaccine_util.addVaccineByDistrict()

print('*'*80)

