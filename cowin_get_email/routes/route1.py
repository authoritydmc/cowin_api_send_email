from flask import render_template,redirect
from flask import  url_for, Blueprint, request,Response
from flask import jsonify
from cowin_get_email.databases import database
from cowin_get_email.utility import api,validator,send_email
import json

bp = Blueprint('route1', __name__)
print("Calling Routes")


@bp.route('/')
def home():

    testR = "DB CONNECTED"
    data = {}
    data['states'] = api.getStates()


    return render_template('base.html', data=data)


@bp.route('/addUser', methods=['POST', 'GET'])
def addU():

    if request.method == "GET":
        return "Get Method TO be implemented"

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
        return render_template('info.html',info=info)
    else:
       return  render_template('info.html',info=json.dumps(msg))


@bp.route('/pincodes')
def pincodes():

    res,_=database.getAllPincode()
    return  render_template('info.html',info=str(res))
  

@bp.route('/vaccines')
def vaccines():
    d=request.args.get('decrypted',None)
    shdDecrypt=True if d=="true" else False
    res,_=database.getAllVaccines(shdDecrypt)


    return  render_template('info.html',info=str(res))




@bp.route('/vaccine')
def vaccine():
    pincode=request.args.get('pincode')

    if pincode!=None:

        res,_=database.getVaccineByPincode(pincode)

        return  render_template('info.html',info=str(res))

    else:
        return "Expected get Parameter pincode "





@bp.route('/districts')
def districts():

    tracked=request.args.get('isTracked', None)
    if tracked!=None and tracked=='true':
        res,_=database.getAllDistrictWithoutTracked()
        return str(res)
    else:

        res,_=database.getAllDistricts()

    return  render_template('info.html',info=str(res))



@bp.route('/dpd')
def addDumD():

    database.addDistrict(dist_id=123,dist_name='Dummy A',track=True)
    database.addDistrict(dist_id=242,dist_name='Dummy B',track=False)

    database.addDistrict(dist_id=789,dist_name='Dummy C',track=True)
    return 'Dummy districts added to'
