from flask import render_template, redirect, url_for, Blueprint, request
from cowin_get_email.databases import database
from cowin_get_email.utility import api


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