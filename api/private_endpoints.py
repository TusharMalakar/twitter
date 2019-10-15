import json
from flask import Blueprint, request
from services.database.DBConn import database
from bson import json_util, ObjectId  # Trying a PyMongo serializer

userDB = database.users
tweetDB = database.tweet
user_api = Blueprint('user_api', __name__)


@user_api.route("/like_on_tweet", methods=['POST'])
def like_on_tweet():
    """"
    http://127.0.0.1:5000/user/like_on_tweet
    body = {
       "id": "5da54850158ea70cdd95a209",
        "likes"   :  {
                        "liker" : "testuser2@myhunter.cuny.edu",
                        "like"   : "liked"
            }
    }
    """
    data = request.get_json()
    tweet_id = data['id']
    record = tweetDB.find({'_id': ObjectId(tweet_id)})
    if record is None:
        return json.dumps({'error': "No collaborations to update matched id"})
    else:
        try:

            if 'likes' in data and isinstance(data['likes'], object):
                result = tweetDB.update(
                    {"_id": ObjectId(tweet_id)},
                    {
                        '$push': {
                            "likes": data['likes']
                        }
                    }
                )

            return json.dumps({"success": True})
        except Exception as e:
            return json.dumps({"error": "Exception found"})



@user_api.route("/comment_on_tweet", methods=['POST'])
def comment_on_tweet():
    """"
    http://127.0.0.1:5000/user/comment_on_tweet
    body = {
       "id": "5da61dbed78b3b2b10a53582",
        "comments" :  {
                        "commenter" : "testuser2@myhunter.cuny.edu",
                        "comment"   : "comments against tweet : 7"
                      }
    }
    """
    data = request.get_json()
    tweet_id = data['id']
    record = tweetDB.find({'_id': ObjectId(tweet_id)})
    if record is None:
        return json.dumps({'error': "No collaborations to update matched id"})
    else:
        try:
            if 'comments' in data and isinstance(data['comments'], object):
                result = tweetDB.update(
                    {"_id": ObjectId(tweet_id)},
                    {
                        '$push': {
                            "comments": data['comments']
                        }
                    }
                )

            return json.dumps({"success": True})
        except Exception as e:
            return json.dumps({"error": "Exception found"})



@user_api.route("/delete_my_tweet", methods=['DELETE'])
def delete_my_tweet():
    """
    http://127.0.0.1:5000/user/delete_my_tweet
    body = {
        "id" : "5da54850158ea70cdd95a209",              #JSON, required
        "owner" : "testuser1@myhunter.cuny.edu"  #JSON, required
    }

    """
    data = request.get_json()
    tweet_id = data['id']
    record = tweetDB.find({'_id': ObjectId(tweet_id)})
    if record is None:
        return json.dumps({'error': "No tweet to update matched id"})
    else:
        try:
            if 'owner' in data and isinstance(data['owner'], str):
                result = tweetDB.delete_one(
                    {"_id": ObjectId(tweet_id)}

                )
        except Exception as e:
            return json.dumps({"error": "Exception found"})




@user_api.route("/edit_my_tweet", methods=['POST'])
def edit_my_tweet():
    """
    http://127.0.0.1:5000/user/edit_my_tweet
    body = {
        "id" : "5da54850158ea70cdd95a209",       #JSON, required
        "owner" : "testuser1@myhunter.cuny.edu", #JSON, required
        "tweet" : " updated tweet "              # optional
    }

    """
    data = request.get_json()
    tweet_id = data['id']
    record = tweetDB.find({'_id': ObjectId(tweet_id)})
    if record is None:
        return json.dumps({'error': "No tweet to update matched id", 'code': 996})
    else:
        try:
            if 'owner' in data and isinstance(data['owner'], str):
                result = tweetDB.update_one(
                    {"_id": ObjectId(tweet_id)},
                    {
                        "$set": {
                            "tweet": data['tweet']
                        }
                    }

                )
        except Exception as e:
            return json.dumps({"error": "Exception found"})



@user_api.route("/my_tweet", methods=['GET'])
def get_my_tweet():
    """"
    http://127.0.0.1:5000/user/my_tweet?owner=testuser1@myhunter.cuny.edu

    :return : [
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
    owner = request.args.get("owner")
    record = list(tweetDB.find({"owner": owner}))
    return json.dumps(record, default=json_util.default)


@user_api.route("/create_tweet", methods=['PUT'])
def create_tweet():
    """
    http://127.0.0.1:5000/user/create_tweet
    # in the body "tweet" and "owner" are required
    body = {
        "tweet" : "this is the tweet",
        "owner" : "testuser1@myhunter.cuny.edu"
        "likes" : [],
        "comments" : []
    }
    :return: True or False
    """
    content = request.get_json(force=True)
    if not content['tweet']:
        return json.dumps({'error': "tweet parameter was not provided."})
    if not content['owner']:
        return json.dumps({'error': "owner parameter was not provided."})
    record = userDB.find_one({'username': content['owner']})

    if content['owner'] in record['username']:
        response = tweetDB.insert_one(content)
        return json.dumps({"success": True, "message": "Tweet has been created."})
    else:
        return json.dumps({"error": True})
