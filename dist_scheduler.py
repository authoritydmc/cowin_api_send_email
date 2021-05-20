print('Running Dist_scheduler')

print('*'*30,'from  dist scheduler','*'*35)

from cowin_get_email.utility import district_util

# track Every Pincode of A district ,Working Fine ..
district_util.populateDistrictsData()


print('*'*80)

import auto_slots_tracker