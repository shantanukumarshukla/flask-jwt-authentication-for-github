import mysql.connector
import yaml
import os

my_path = os.path.abspath(os.path.dirname(__file__))
file = yaml.safe_load(open(os.path.join(my_path, "config\\" + "application_properties.yaml")))
db_user = file['db_user']
db_password = file['db_password']
db_host = file['db_host']
db_name = file['db_name']

def database_access():
    mydb = mysql.connector.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    return mydb