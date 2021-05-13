from cowin_get_email.utility import district_util,pincode_util,common_util,send_email,user_util,center_util,session_util
import json


# send email to all District based Receipeint.

def DistrictMailer():
    # step 1 :Gather All Districts


    allDistricts=district_util.getListofDistrictIds()
    print("All District->",allDistricts)
    # step 2 : for each district gather All Pincodes 
    for districtID in allDistricts:
        allPincodes=pincode_util.getListofPincodeBydist_id(districtID)
        # allPincodes=[273001]
        print("All Pincode for ",districtID,"=",allPincodes)
        ALL_VACCINE_SESSIONS=[]
        ALL_CENTER_DATA={}
        for pincode in allPincodes:
            allCenters=center_util.getListOfCenterByPincode(pincode)
            # print("Current Pincode",pincode ,"Centers->",allCenters)

            # get All Sessions 
            for center in allCenters:
                
               te_sessions=session_util.getListofSessionByCenter(center.center_id)
            #    print("Sessions of [{}] of [{}] is -> {}".format(center.center_id,pincode,te_sessions))
               ALL_VACCINE_SESSIONS.extend(te_sessions)
               ALL_CENTER_DATA[center.center_id]=center
            
        # print("All Sessions->",ALL_VACCINE_SESSIONS)

        # get ALL Valid Users.

        allUsers=user_util.getUserOfDistId(districtID)

        send_email.sendDailyReminder(ALL_CENTER_DATA,ALL_VACCINE_SESSIONS,allUsers)


def PincodeBasedUserMailer():
    allUsers=user_util.getAllUsersSearchingByPincode()
    for user in allUsers['users']:

        ALL_VACCINE_SESSIONS=[]
        ALL_CENTER_DATA={}
        allCenters=center_util.getListOfCenterByPincode(user.pincode)
            # print("Current Pincode",pincode ,"Centers->",allCenters)

            # get All Sessions 
        for center in allCenters:
                
               te_sessions=session_util.getListofSessionByCenter(center.center_id)
            #    print("Sessions of [{}] of [{}] is -> {}".format(center.center_id,pincode,te_sessions))
               ALL_VACCINE_SESSIONS.extend(te_sessions)
               ALL_CENTER_DATA[center.center_id]=center
            
        # modiy user list so that it matches with District matched Userlist
        allUser={}
        allUser['users']=[user]

        send_email.sendDailyReminder(ALL_CENTER_DATA,ALL_VACCINE_SESSIONS,allUsers)
