import os
import json
from flask_cors import CORS
from flask import Flask, request
from services.database.DBConn import database
from security.JWT.symmetric import session_cookie

from api.private_endpoints import user_api
from api.public_endpoints import public_api
from api.AuthorizationAPI import auth_api


app = Flask(__name__)
CORS(app)
#All endpoints in API_1.py are prefixed with the /user route.
app.register_blueprint(user_api, url_prefix='/user')
#All endpoints in API_1.py are prefixed with the /public route.
app.register_blueprint(public_api, url_prefix='/public')
#All endpoints in Authorization.py are prefixed with the /auth route.
app.register_blueprint(auth_api, url_prefix='/auth')
userDB = database.users

# Root
@app.route("/", methods=['POST'])
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




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, threaded=True, debug=True)
