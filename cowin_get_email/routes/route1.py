from flask import render_template,redirect
from flask import  url_for, Blueprint, request,Response
from flask import jsonify
from cowin_get_email.databases import database
from cowin_get_email.utility import api,validator
import json

bp = Blueprint('route1', __name__)
print("Calling Routes")


@bp.route('/')
def home():

    testR = "DB CONNECTED"
    data = {}
    data['states'] = api.getStates()

    print("From Main", data['states'])

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

    if datas['selectby']=='pincode':
        datas['dist_id']=''
        datas['dist_name']=''
        # save this pincode for Tracking...
        database.addPincode(datas['pincode'])
    else:
        datas['pincode']=''
        database.addDistrict(dist_id=datas['dist_id'],dist_name=datas['dist_name'])
        # add pincodes of this Districts


    if isValidUser==True:
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
        return str(datas)
    else:
       return  json.dumps(msg)


@bp.route('/user')
def user():
    email=request.args.get('email',None)
    res='No User Found'
    if email!=None:
        res=database.isUserExist(email)

    return str(res)

@bp.route('/users')
def users():

    res,_=database.getAllUser()

    return str(res)

@bp.route('/pincodes')
def pincodes():

    res,_=database.getAllPincode()

    return str(res)

@bp.route('/vaccines')
def vaccines():

    res,_=database.getAllVaccines()

    return str(res)

@bp.route('/vaccine')
def vaccine():
    pincode=request.args.get('pincode')

    if pincode!=None:

        res,_=database.getVaccineByPincode(pincode)

        return str(res)
    else:
        return "Expected get Parameter pincode "


@bp.route('/dpa')
# ################# Sample Pincode Entry
def addPincode():

    database.addPincode(224513,235)
    database.addPincode(502301,777)

    database.addPincode(235124,1245)
    return 'dummy pincode Added'

@bp.route('/dpv')
# ################# Sample Vaccine Entry
def addVaccine():

    database.addVaccine(vaccine='Covaxin'
    ,pincode='251523',min_age=45,fee='0',
    available_vaccine_cap=74,center_id=2341,center_name='CenterA',center_address='Place1')

    database.addVaccine(vaccine='Covishield'
    ,pincode='101010',min_age=18,fee='0',
    available_vaccine_cap=74,center_id=2341,center_name='Center Excellance',center_address='Place2')

    return 'dummy Vaccine Added'


@bp.route('/districts')
def districts():

    tracked=request.args.get('isTracked', None)
    if tracked!=None and tracked=='true':
        res,_=database.getAllDistrictWithoutTracked()
        return str(res)
    else:

        res,_=database.getAllDistricts()

        return str(res)


@bp.route('/dpd')
def addDumD():

    database.addDistrict(dist_id=123,dist_name='Dummy A',track=True)
    database.addDistrict(dist_id=242,dist_name='Dummy B',track=False)

    database.addDistrict(dist_id=789,dist_name='Dummy C',track=True)
    return 'Dummy districts added to'
