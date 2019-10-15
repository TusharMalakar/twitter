"""
    this api will distribute who should use which api
"""
import json
from flask import Blueprint, request
from services.database.DBConn import database

userDB = database.users
auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/login")
def login():
    """Generated End-Point Sample
    http://127.0.0.1:5000/auth/login?username=testuser1&password=password
    """
    username = request.args.get("username")
    password = request.args.get("password")
    return json.dumps({'username': username, "password": password})


@auth_api.route("/convert", methods=['POST'])
def end_point_converter():
    username = request.args.get("username")
    password = request.args.get("password")
    return json.dumps({'username': username, "password": password})
