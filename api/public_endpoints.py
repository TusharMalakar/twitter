import json

from bson import json_util
from flask import Blueprint
from services.database.DBConn import database

userDB = database.users
tweetDB = database.tweet
public_api = Blueprint('public_api', __name__)


@public_api.route("/all_tweet", methods=['GET'])
def get_all_tweet():
    """"
    http://127.0.0.1:5000/user/all_tweet

    :returns : [
                {
                    "_id": {
                        "$oid": "5da53be70c92978ace45b21a"
                    },
                    "tweet": "this is the tweet",
                    "owner": "testuser1@myhunter.cuny.edu",
                    "comments": [
                        {
                            "commenter": "testuser2@myhunter.cuny.edu",
                            "comment": "comments against tweet"
                        }
                    ]
                }
            ]

    """
    record = list(tweetDB.find())
    return json.dumps(record, default=json_util.default)
