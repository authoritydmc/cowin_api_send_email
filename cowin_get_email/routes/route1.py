from flask import render_template,redirect,url_for
from flask import  url_for, Blueprint, request,Response
from flask import jsonify
from cowin_get_email.databases import database
from cowin_get_email.utility import api,validator,send_email,user_util
import json
from config import  checkENV

bp = Blueprint('route1', __name__)
print("Calling Routes")
local=False
if checkENV()=="LOCAL":
    local=True


@bp.route('/')
def home():
        return render_template('landing.html',local=local)





@bp.route('/addUser', methods=['POST', 'GET'])
def addU():

    if request.method == "GET":
        data = {}
        data['states'] = api.getStates()
        return render_template('addUser.html', data=data,local=local)

    # below codes are handled by post request
    datas = {}
    
    datas['name'] = request.form.get('name')
    datas['phone'] = request.form['phone']
    datas['email'] = request.form['email']
    datas['selectby'] = request.form['selectby']
    datas['age'] = request.form['age']
    datas['pincode'] = request.form['pincode']
    datas['dist_id'] = request.form['dist_id']
    datas['dist_name'] = request.form['dist_name']

    
    # Valid the Datas

    msg,isValidUser=validator.validUser(datas)

    # check whether user is registered or not
    res,isPresent=database.isUserExist(datas['email'])
    if isPresent:
        print("USER FOUND")
        data={}
        data['email']=res.email
        return  render_template('userExists.html',data=data,local=local)

        # here send email to login /Update Details

    # remove pincode or dist_id and Name based on selectby




    if isValidUser==True:
        if datas['selectby']=='pincode':
            datas['dist_id']=''
            datas['dist_name']=''
            # save this pincode for Tracking...
            database.addPincode(datas['pincode'])
        else:
            datas['pincode']=''
            database.addDistrict(dist_id=datas['dist_id'],dist_name=datas['dist_name'])
            # add pincodes of this Districts
        msg,res=database.addUser(name=datas['name'],
                        age=datas['age'],
                        email=datas['email'],
                        phone=datas['phone'],
                        search_by=datas['selectby'],
                        pincode=datas['pincode'],
                        dist_id=datas['dist_id'],
                        dist_name=datas['dist_name'])
        datas['msg'] = msg
        datas['result']=res
        info=msg
        if res==True:
            send_email.sendWelcomeEmail(datas['name'],datas['email'],datas['selectby'],datas['pincode'],datas['dist_name'])

            info='Thank you for Registering. Please Check your email Inbox [make sure to check SPAM folder too]'
        return render_template('info.html',info=info,local=local)
    else:
       return  render_template('info.html',info=json.dumps(msg),local=local)


@bp.route('/pincodes')
def pincodes():

    res,_=database.getAllPincode()
    return  render_template('info.html',info=str(res),local=local)
  
@bp.route('/districts')
def districts():

    tracked=request.args.get('isTracked', None)
    if tracked!=None and tracked=='true':
        res,_=database.getAllDistrictWithoutTracked()
        return str(res)
    else:

        res,_=database.getAllDistricts()

    return  render_template('info.html',info=str(res),local=local)



@bp.route('/sessions')
def session():
    res,_=database.getAllSessions()

    return  render_template('info.html',info=str(res),local=local)

@bp.route('/centers')
def center():
    res,_=database.getAllCenters()
    
    return  render_template('info.html',info=str(res),local=local)

@bp.route("/login")
def login():

    email=request.args.get('email',None)
    res=''
    if email!=None:
        msg,_=user_util.generateLoginofUser(email)
        res=msg
        res+=" <br> Please goto your email inbox and click on the link to login"
    else:
        res= "Please provide valid Details"

    return  render_template('info.html',info=str(res),local=local)
    
@bp.route("/dashboard")
def dashboard():
    token=request.args.get('token',None)
    email=request.args.get('email',None)
    res=''
    if token!=None and email!=None:
        msg,isTokenValid=database.matchToken(email,token)

        if isTokenValid:
            res='Valid User wow ',msg
        else:
            res="Invalid User ..boohooo"+msg

    else:
        return redirect(url_for('route1.home'))

    return  render_template('info.html',info=str(res),local=local)
    