from cowin_get_email import app
from cowin_get_email.databases.database import  db

if __name__ == "__main__":
    db.init_app(app)
    