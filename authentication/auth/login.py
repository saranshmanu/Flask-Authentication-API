from authentication.constants.host_configuration import db
from authentication.constants.environment_variables import JWT_SECRET, JWT_EXPIRATION_DURATION
from authentication.utils.helper_functions import message_response
from flask import request, jsonify, Blueprint
from Crypto.Hash import SHA512
import jwt, datetime

login_blueprint = Blueprint("login", __name__)
@login_blueprint.route('/auth/login', methods = ['POST'])
def login():
    user_username = request.form['username']
    user_password = request.form['password']
    success = True
    # Checking if the length of the fields are exceeding the limit or not 
    if len(user_password) > 30 :
        message = "Length of password exceeded the limit"
        success = False
    elif len(user_username) > 30 :
        message = "Length of username exceeded the limit"
        success = False
    if success == False:
        return message_response(success, message)
    result = db.users.find_one({"username": user_username})
    if result == None:
        # The user doen't exist
        return message_response(False, "User doesn't found.")
    # The user is successfully found
    if result['email_confirmation'] == False:
        return message_response(False, "Email hasn't been confirmed")
    # User has confirmed the email id and now continuing
    hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
    returned_hash = result['password']
    if hash == returned_hash: 
        # Password matched successfully
        encrypted_uuid = result['uuid']
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_DURATION)
        jwt_payload = jwt.encode({
            "exp" : expiration_time,
            "uuid": encrypted_uuid
        }, JWT_SECRET)
        return jsonify({
            "success"   : success,
            "message"   : "User signed in successfully",
            "token"     : jwt_payload
        })
    else:
        return message_response(False, "User found. Password does not match")