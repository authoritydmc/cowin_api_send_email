from cowin_get_email import app
from config import prod_config
if __name__ == "__main__":
    app.config['SECRET_KEY'] = prod_config.secret_key   
    app.run()