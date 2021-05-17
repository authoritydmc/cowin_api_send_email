from flask import render_template,redirect,url_for, Blueprint,request

from cowin_get_email.utility import common_util,pincode_util,center_util,district_util,session_util
from cowin_get_email.databases import database
from cowin_get_email.routes import route1

bp = Blueprint('routeDashboard', __name__)




    
@bp.route("/dashboard")
def dashboard():
    logres,logged=route1.isLoggedIn()


    if logged==True:
        data={}
        # get user info here 
        user,_=route1.getUserDetailsfromSession()
        print("LOGGED IN AS -> ",user)
        data['name']=user.name
        data['selectby']=user.search_by
        print("Passing Parameters",data)
        # send center and sessions of users.
        if user.search_by=="pincode":
            data['searchparam']=user.pincode
            allCenters=center_util.getListOfCenterByPincode(user.pincode)
            # get all session for each of centers
            sessionDic={}
            validCenters=[]
            for center in allCenters:
                lsts=session_util.getListofSessionByCenter(center.center_id)
                fmtitr=filter(lambda s: user.age>=s.min_age,lsts)
                lsts=list(fmtitr)
                if len(lsts)>0:
                    validCenters.append(center)
                    sessionDic[center.center_id]=lsts
            print('$'*80)
            print("sessions -> ",sessionDic)
            print('$'*80)
            print("All centers-> ",allCenters)
            print('$'*80)
            data['centers']=validCenters
            data['sessions']=sessionDic
                        
            data['centers']=validCenters

            if len(sessionDic)==0:
                print("Will hide the Details")
                data['hideVaccine']=True
            # get all center and session of this pincode
        else:
            data['searchparam']=user.dist_name
            # get all pincodes and then centers and then sessions of this pincode

            allPincodes=pincode_util.getListofPincodeBydist_id(user.dist_id)
            print("All pincodes->",allPincodes)

            allCenters=[]
            for pin in allPincodes:
                allCenters.extend( center_util.getListOfCenterByPincode(pin))
            # get all session for each of centers
            print("All centers-> ",allCenters)
            sessionDic={}
            validCenters=[]
            for center in allCenters:
                lsts=session_util.getListofSessionByCenter(center.center_id)
                fmtitr=filter(lambda s: user.age>=s.min_age,lsts)
                lsts=list(fmtitr)
                if len(lsts)>0:
                    validCenters.append(center)
                    sessionDic[center.center_id]=lsts
            print('$'*80)
            print("sessions -> ",sessionDic, "total->",len(sessionDic))
            print('$'*80)
            print("All centers-> ",allCenters)
            print('$'*80)
            data['hideVaccine']=False
            data['sessions']=sessionDic

            data['centers']=validCenters

            if len(sessionDic)==0:
                print("Will hide the Details")
                data['hideVaccine']=True



        
        
        
        return render_template('dashboard.html',local=route1.local,data=data,cnvtT=common_util.getSimpleDatenTimeFromtimeStamp)
    
    
    
    else:
        # token verification
        token=request.args.get('token',None)
        email=request.args.get('email',None)
        res=''
        if token!=None and email!=None:
            msg,isTokenValid=database.matchToken(email,token)

            if isTokenValid:
                # setup the session and redirect to homepage for proper landing.
                route1.setupSession(email,token)

        return redirect(url_for('route1.home'))