import json
from flask import Blueprint, request
from services.database.DBConn import database
from security.JWT.symmetric import session_cookie

userDB = database.users
auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/create_user", methods=['POST'])
def create_user():
    """Generated End-Point Sample
    http://127.0.0.1:5000/
    body = {
         "username" : "testuser3@myhunter.cuny.edu",
        "password" : "password"
    }
    """
    content = request.get_json(force=True)
    if not content['username']:
        return json.dumps({'error': "username parameter was not provided.", 'code': 1})
    if not content['password']:
        return json.dumps({'error': "Password parameter was not provided.", 'code': 2})
    if len(content['password']) < 6 or len(content['password']) > 52:
        return json.dumps(
            {'error': "Password must be at least 6 characters and less than 52 characters long.", 'code': 3})
    record = userDB.find_one({'username': content['username']})
    if record is None:
        result = userDB.insert_one(content)
        return json.dumps({"success": True, 'message': 'you can log-in now, using usename and password'})
    else:
        return json.dumps({"success": False, 'error': 'User already exist.'})



@auth_api.route("/login", methods=['GET'])
def login():
    """Generated End-Point Sample
    http://127.0.0.1:5000/auth/login?username=testuser1@myhunter.cuny.edu&password=password
    """
    username = request.args.get("username")
    password = request.args.get("password")

    if not username:
        return json.dumps({'error': "Username not provided.", 'success': False, 'code': 66})
    if not password:
        return json.dumps({'error': "Password not provided.", 'success': False, 'code': 67})

    record = userDB.find_one({'username': username})
    if record is None:
        return json.dumps({'error': "User doesn't exist.", 'success': False, 'code': 1})
    else:
        actualPassword = record['password']
        # print(password," = ", actualPassword)
        if password == actualPassword:
            authtoken = session_cookie(username).decode("utf-8")
            return json.dumps({'success': True, 'token': authtoken})
        else:
            return json.dumps({'error': 'Invalid Password', 'code': 2})



