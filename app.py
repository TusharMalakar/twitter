import os
import json
from flask import Flask
from flask_cors import CORS

from api.endpoints import user_api
from api.AuthorizationAPI import auth_api


app = Flask(__name__)
CORS(app)
#All endpoints in API_1.py are prefixed with the /user route.
app.register_blueprint(user_api, url_prefix='/user')
#All endpoints in Authorization.py are prefixed with the /auth route.
app.register_blueprint(auth_api, url_prefix='/auth')


# Root
@app.route("/", methods=['GET'])
def helloWorld():
    """Generated End-Point Sample
    http://127.0.0.1:5000/
    """
    return json.dumps({"message": "Welcome Hunter Tweeter!"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port, threaded=True, debug=True)
