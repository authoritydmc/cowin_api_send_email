from flask import  Flask,jsonify
from cowin_get_email.routes import route1
from cowin_get_email.databases import database

app=Flask(__name__)

print("Calling INIT")
try:
    from cowin_get_email.routes import localRoute
    app.register_blueprint(route1.bp)
    app.register_blueprint(localRoute.bp)

except:
    print('Exception occured while Registering Route')