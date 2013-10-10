import web
import hashlib
from models.model import get
from code import session

def check_user(username, password):
    if username == '' or password == '':
        return False
    where_dict = {'member_username':username, 'member_password':make_password(password)}
    if get('member_info', where=web.db.sqlwhere(where_dict)):
        return True
    else:
        return False

def make_password(password):
    return hashlib.sha1('majianjian-' + password).hexdigest()

def is_user_login():
    if session.login == True and session.username != '':
        return True
    else:
        return False

def is_admin_login():
    if session.login == True and session.username == 'admin':
        return True
    else:
        return False
