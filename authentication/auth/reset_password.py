from authentication.constants.host_configuration import db
from authentication.utils.helper_functions import message_response
from flask import request, Blueprint
from Crypto.Hash import SHA512

reset_password_blueprint = Blueprint("reset_password", __name__)
@reset_password_blueprint.route('/auth/reset_password', methods = ['POST'])
def reset_password():
    user_password = request.form['password']
    user_new_password = request.form['new_password']
    user_username = request.form['username']
    hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
    new_hash = SHA512.new(user_new_password.encode('utf-8')).hexdigest()
    result = db.users.find_one({"username": user_username})
    if result == None:
        return message_response(False, "User doesn't exist")
    if hash == result['password']:
        db.users.update_one(
            {"uuid": result['uuid']},
            {"$set": {"password":new_hash}}
        )
        return message_response(True, "User password changed successfully")
    else:
        return message_response(False, "Password doesn't match")