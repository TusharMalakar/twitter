import json
from flask import Blueprint, request
from services.database.DBConn import database
from security.JWT.symmetric import session_cookie
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
                        "like"   : "lived"
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
       "id": "5da53be70c92978ace45b21a",
        "comments" :  {
                        "commenter" : "testuser2@myhunter.cuny.edu",
                        "comment"   : "comments against tweet : 7"
                      },
        "lives"   :  {
                        "commenter" : "testuser2@myhunter.cuny.edu",
                        "live"   : "lived"
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
    http://127.0.0.1:5000/user/edit_my_tweet
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



@user_api.route("/all_tweet", methods=['GET'])
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
        'tweet' : "this is the tweet",
        'owner' : "testuser1@myhunter.cuny.edu",
        'comments' : [
                      {
                        'commenter' : "testuser2@myhunter.cuny.edu",
                        'comment'   : "comments against tweet"
                      }
        ]
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


@user_api.route("/login", methods=['GET'])
def login():
    """Generated End-Point Sample
    http://127.0.0.1:5000/user/login?username=testuser1@myhunter.cuny.edu&password=password
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




@user_api.route("/create_user", methods=['PUT'])
def create_user():
    """
    http://127.0.0.1:5000/user/create_user
    body = {
         'username' : "testuser3@myhunter.cuny.edu",
        'password' : "password"
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
