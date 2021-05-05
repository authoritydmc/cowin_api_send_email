from flask import render_template, redirect, url_for, Blueprint, request
from ..databases import database
from ..utility import api


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

    datas={}
    datas['res']='wrking'
    datas['name']=request.form.get('name')
    datas['phone']=request.form['phone']
    datas['email']=request.form['email']
    datas['selectby']=request.form['selectby']
    datas['age']=request.form['age']
    datas['pincode']=request.form['pincode']
    datas['dist_id']=request.form['dist_id']
    datas['dist_name']=request.form['dist_name']

    return str(datas)

    # database.addUser(name=name, age=age, email=email, phone=phone, pincode=0)

