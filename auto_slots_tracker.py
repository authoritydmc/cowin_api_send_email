# implement auto mailer whenever any slot is there

# cowin api client side dashboard

# send email when user update.

from cowin_get_email.utility import session_util,pincode_util,center_util,user_util,send_email,district_util

print("--------------------from auto slots tracker------------------------")
ALL_CENTERS={} #key:value = pincode:centerList
ALL_SESSIONS={} #key:value = center_id:sessionList
ALL_PINCODES={} #key:value = dist_id :pincodeList
def dataGatherer():
    for session in session_util.getAutoMailerSessions():
        print(session)
        # print("this session belong to center ->",session.center_id)
        # get pincode of this center .
        center_obj=center_util.getCenterByID(session.center_id)
        pincode_obj=pincode_util.getPincodeByID(center_obj.pincode)
        # print("pincode -> ",pincode_obj)
        # data append 
        if pincode_obj.district_id!=-1:
            print("tis pin has dist ID")
            # strore Dist ID.
            temp_pin=ALL_PINCODES.get(pincode_obj.district_id,None)
            if temp_pin==None:
                x=[]
                x.append(pincode_obj)
                ALL_PINCODES[pincode_obj.district_id]=x
            else:
                temp_pin.append(pincode_obj)

        temp_sess=ALL_SESSIONS.get(session.center_id,None)
        if temp_sess==None:
            x=[]
            x.append(session)
            ALL_SESSIONS[session.center_id]=x
        else:
            temp_sess.append(session)
        
        temp_center=ALL_CENTERS.get(center_obj.pincode,None)
        if temp_center==None:
            x=[]
            x.append(center_obj)
            ALL_CENTERS[center_obj.pincode]=x
        else:
            temp_center.append(center_obj)








def pincodeMailer():
    # for dist_id,pincodeList in ALL_PINCODES.items():
    #     print("dist id -> {} data->{} ".format(dist_id,pincodeList))
    
    # input("Press key")

    for pincode,centersList in ALL_CENTERS.items():
        # print("Pincode {} -> centerList ->{} ".format(pincode,centersList))
    
        pincode_obj=pincode_util.getPincodeByID(pincode)
        usersList=[]
        # if pincode district id ==-1
        usersList.extend(user_util.getListofUserSearchingByPincode(pincode)['users'])

        if len(centersList)>0:
            send_email.autoMailer(centersList,ALL_SESSIONS,usersList," pincode "+str(pincode))
        else:
            print("{} has no center ".format(pincode))
     # now gather which pincode or dist has this center


def dist_mailer():
    print("Dist mailer called ")
    for dist_id ,pincodelist in ALL_PINCODES.items():
        DIST_BASED_ALL_CENTERS=[]
        print("dist ID->{} ,pinList->{}".format(dist_id,pincodelist))
        for pinobj in pincodelist:
            print("\n\nfor pincode ->{} its data->{}".format(pinobj.pincode,ALL_CENTERS[pinobj.pincode]))
            DIST_BASED_ALL_CENTERS.extend(ALL_CENTERS[pinobj.pincode])
        distObj=district_util.getDistrictByID(dist_id)
        print("Final centers ->",DIST_BASED_ALL_CENTERS)

        usersList=user_util.getUserOfDistId(dist_id)['users']

        if len(DIST_BASED_ALL_CENTERS)>0:
            send_email.autoMailer(DIST_BASED_ALL_CENTERS,ALL_SESSIONS,usersList," district "+str(distObj.district_name))
        else:
            print("District {} has no Center".format(dist_id))


dataGatherer()



pincodeMailer()

dist_mailer()
print("--------------------END auto slots tracker------------------------")
