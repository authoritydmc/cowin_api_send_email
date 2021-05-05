from flask import render_template,redirect,url_for,Blueprint



bp=Blueprint('route1',__name__)

    
@bp.route('/')
def home():
        testR="Test"
        return render_template('base.html',test=testR)
