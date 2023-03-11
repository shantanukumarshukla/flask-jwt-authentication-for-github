from flask_restful import Resource, reqparse
from user_api.app.db_connection import database_access
import yaml
import os
from app.logger import configure_logger
from app.mail_alert import welcome_mail

my_path = os.path.abspath(os.path.dirname(__file__))
file = yaml.safe_load(open(os.path.join(my_path, "config\\" + "application_properties.yaml")))
logging = configure_logger('default', 'logs/app.log')
db_table = file['db_table']

class User():
    TABLE_NAME = db_table
    def __init__(self, _id, username):
        self.id = _id
        self.username = username
    @classmethod
    def find_by_username(cls, username):
        logging.info("finding user from datastore")
        connection = database_access()
        cursor = connection.cursor()
        query = 'SELECT id, username, password FROM {table} WHERE username=%s'.format(table=cls.TABLE_NAME)
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        if row:
            logging.info("user found, returning info")
            user = row
        else:
            logging.error("user not found, please register")
            user = None
        connection.close()
        return user
    @classmethod
    def find_by_id(cls, _id):
        logging.info("finding bu user's id from datastore")
        connection = database_access()
        cursor = connection.cursor()
        query = "SELECT id, username, password FROM {table} WHERE id=%s".format(table=cls.TABLE_NAME)
        cursor.execute(query, (_id,))
        row = cursor.fetchone()
        logging.info(row)
        if row:
            logging.info("id found, returning info")
            user = row
        else:
            logging.error("id not found, please register")
            user = None
        connection.close()
        return user


class UserRegister(Resource):
    TABLE_NAME = db_table
    parser = reqparse.RequestParser()
    parser.add_argument('email_address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('contact_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('dob',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('university_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('location',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            logging.error("User with that username already exists")
            return {"message": "User with that username already exists."}, 400
        connection = database_access()
        cursor = connection.cursor()
        query = "INSERT INTO {table} VALUES (NULL, %s, %s, %s, %s, %s, %s)".format(table=self.TABLE_NAME)
        cursor.execute(query, (data['username'], data['password'], data['email_address'], data['contact_number'], data['dob'], data['university_name']))
        logging.info("inserting username: {} and email: {}".format(data['username'], data['email_address']))
        connection.commit()
        welcome_mail(data['username'], data['email_address'])
        connection.close()
        logging.info("User created successfully")
        return {"message": "User created successfully."}, 201

