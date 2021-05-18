from cowin_get_email.utility import district_util,pincode_util,common_util,send_email,user_util,center_util,session_util
import json


# send email to all District based Receipeint.

def DistrictMailer():
    # step 1 :Gather All Districts


    allDistricts=district_util.getListofDistrictIds()
    print("All District->",allDistricts)
    # step 2 : for each district gather All Pincodes 
    for districtID in allDistricts:
        print("/\\"*80)
        print("Current Dist_ID->",districtID)
        print("/\\"*80)

        allPincodes=pincode_util.getListofPincodeBydist_id(districtID)

        print("All Pincode for ",districtID,"=",allPincodes)

        ALL_VACCINE_SESSIONS={}
        ALL_CENTER_DATA=[]
        for pincode in allPincodes:
            allCenters=center_util.getListOfCenterByPincode(pincode)
            # print("Current Pincode",pincode ,"Centers->",allCenters   )
            # get All Sessions 
            for center in allCenters:
                te_sessions=session_util.getListofSessionByCenter(center.center_id)
            #    print("Sessions of [{}] of [{}] is -> {}".format(center.center_id,pincode,te_sessions))
                ALL_VACCINE_SESSIONS[center.center_id]=te_sessions
                ALL_CENTER_DATA.append(center)
                print("Processing center {} {} of pincode {}".format(center.center_id,center.center_name,center.pincode))
            
        allUsers=user_util.getUserOfDistId(districtID)

        print("DIST {} centers -> {}\n\n\n\n and users ->{} ".format(districtID,ALL_CENTER_DATA,allUsers))

        send_email.sendDailyReminder(ALL_CENTER_DATA,ALL_VACCINE_SESSIONS,allUsers)




def PincodeBasedUserMailer():
    allUsers=user_util.getAllUsersSearchingByPincode()
    for user in allUsers['users']:
        print("Currenlty for ",user,"\n\n")
        ALL_VACCINE_SESSIONS={}
        allCenters=center_util.getListOfCenterByPincode(user.pincode)
        for center in allCenters:
                print("Processing center {} {} of pincode {}".format(center.center_id,center.center_name,center.pincode))
            
                te_sessions=session_util.getListofSessionByCenter(center.center_id)
               
                ALL_VACCINE_SESSIONS[center.center_id]=te_sessions
            
        # modiy user list so that it matches with District matched Userlist
        allUser={}
        x=[]
        x.append(user)
        allUser['users']=x
        print("ALL CENTERS->{} \n\n\n ALL SESSIONS -> {} \n\n\n ALL USERS->{} ".format(allCenters,ALL_VACCINE_SESSIONS,allUser))
        if len(allCenters)==0:
            # send update detail
            send_email.sendChangeSearchMethod(user)
        else:
            send_email.sendDailyReminder(allCenters,ALL_VACCINE_SESSIONS,allUser)
        