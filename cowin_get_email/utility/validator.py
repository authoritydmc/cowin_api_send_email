def validUser(userDict):
    try:
        print('*'*80)
        print('Checking ',userDict)
        print('*'*80)
        age = int(userDict.get('age','NA'))
        # age Validator
        if age > 0 and age < 120:
            pass
        else:
            return "invalid Age Error ",False
            
        selectby=userDict.get('selectby',None)
        if selectby!=None and selectby=='district':
            # integer checking of CenterID
            try:
                did = int(userDict.get('dist_id','NA'))
            except :
                return "Please Select Valid District",False
            return 'Validated By District successfully',True
         
        else:
                    # checking by Pincode
            if len(userDict.get('pincode','NA')) == 6:
                return 'Validated User', True
            else:
                return 'Invalid Pincode Error ',False
    except Exception as e:
        return 'Provide Data  Correctly '+str(e), False
