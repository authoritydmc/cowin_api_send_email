from flask import  Flask,jsonify
from cowin_get_email.routes import route1
from cowin_get_email.databases import database

app=Flask(__name__)

print("Calling INIT")
app.register_blueprint(route1.bp)
