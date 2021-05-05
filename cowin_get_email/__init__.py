from flask import  Flask
from .routes import route1
from .databases import database

app=Flask(__name__)

print("Calling INIT")
app.register_blueprint(route1.bp)
