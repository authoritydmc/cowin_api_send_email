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

    database.addUser(name=name, age=age, email=email, phone=phone, pincode=0)

    return "User Added Successfully"
