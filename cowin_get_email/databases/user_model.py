from . import database
print("USER MODEL INIT")
db=database.getDB()
class User(db.Model):
    id=db.column('user_id',db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    age = db.Column(db.Integer(3))

    def __init__(self,name,age,email,phone="NA"):
        self.name = name
        self.email = email
        self.age = age
        self.phone = phone

    def getUser(self):
        return self
    
    def getUserName(self):
        return self.name
    
    def getUserAge(self):
        return self.age
    
    def getUserEmail(self):
        return self.email
    
    def getUserPhone(self):
        return self.phone

    def setUserName(self,name):
        self.name=name

    def setUserAge(self,age):
        self.age=age
    
    def setUserEmail(self,email):
        self.email=email
    
    def setUserPhone(self,ph):
        self.phone=ph

    
db.create_all()