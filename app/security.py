from werkzeug.security import safe_str_cmp
from user_api.app.user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user[2], password):
        return user


def identity(payload):
    print(payload)
    user_id = payload['identity']
    return User.find_by_id(user_id)