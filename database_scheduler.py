print("database Scheduler / fixer")



from cowin_get_email.databases import session_model

from cowin_get_email.databases import user_model,district_model,pincode_model

# remove old records of sessions

session_model.removeOutDatedSession()

# remove untagged dist_id and pincodes based on user count

pincode_model.removeunTaggedPincode()

district_model.removeUnTaggedDistricts()



