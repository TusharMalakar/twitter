import platform, os
from flask import Flask
from flask_cors import CORS
from services.database.DBConn import database


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
@app.route("/", methods=['GET'])
def welcome_page():
    record = userDB.find();
    tweetDB = database.tweet.find()
    if record is not None and tweetDB is not None:
        return "Welocme to twitter api ; server is connected"




if __name__ == "__main__":
    if platform.system() == 'Linux':
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, threaded=True, debug=True)
    else:
        app.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
