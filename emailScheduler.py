print("Email Scheduler Called")
from cowin_get_email.utility import district_util,pincode_util,vaccine_util,common_util,user_util,send_email
import json
print('*'*30,'from Email Scheduler','*'*35)

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
        finalAssembledData=[]

        # step 3 :for each pincodes get its Res String Decrypted
        for pincode in allPincodes:
            try:
                finalAssembledData.append(vaccine_util.getResouceStringDecryptedByPincode(pincode))
                

            except:
                print("error in getting Resource String for pincode {}".format(pincode))
        
        # step 4 now got the List ,loop thorough each and send Mail ...

        # print("All Assembled ",finalAssembledData,"its type-> ",type(finalAssembledData))
        formattedDictData=processPincodeData(finalAssembledData)

        # print("Formatted Data-> ",formattedDictData)
        # step 5 get All Users of This Dist_data
        # sample 
        # {'users': [{"name": "xxx", "email": "xys@gmail.com", "age": 24, "selectby": "district", "dist_id": 145, "pincode": 0}], 'total': 1}

        userList=user_util.getUserOfDistId(districtID)

        # step 6 :now we have all pincodes data and list of users  to whom we have to send this

        # pass it to sendEmail Method

        send_email.sendDailyReminder(formattedDictData,userList)




def processPincodeData(pincodeList):

    pincodeFormattedData=[]
    for pincodeData in pincodeList:


        j=common_util.getPythonDictofStr(pincodeData)
        pincodeFormattedData.append(j)

    
    return pincodeFormattedData




DistrictMailer()
print('*'*30,'End Email Scheduler','*'*35)