from flask import  Flask,jsonify
from cowin_get_email.routes import route1
from cowin_get_email.databases import database

from config import prod_config


app=Flask(__name__)
app.config['SECRET_KEY'] = prod_config.secret_key   

app.register_blueprint(route1.bp)


print("Calling INIT")
try:
    from cowin_get_email.routes import localRoute
    app.register_blueprint(localRoute.bp)

except:
    print('Exception occured while Registering Route')