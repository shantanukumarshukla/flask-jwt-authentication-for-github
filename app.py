from flask import Flask
from flask_restful import Api
from app.user import UserRegister
from app.logger import configure_logger
import os,sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

logging = configure_logger('handlers', 'logs/app.log')
app = Flask(__name__)
app.secret_key = 'zarurat'
api = Api(app)
api.add_resource(UserRegister, '/register')



if __name__ == '__main__':
    app.run(debug=True)

