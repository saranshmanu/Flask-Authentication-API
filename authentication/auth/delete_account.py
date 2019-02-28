from authentication.constants.host_configuration import db
from authentication.utils.helper_functions import message_response
from flask import request, Blueprint
from Crypto.Hash import SHA512

delete_account_blueprint = Blueprint("delete_account", __name__)
@delete_account_blueprint.route('/auth/delete_account', methods = ['POST'])
def delete_account():
    user_password = request.form['password']
    user_username = request.form['username']
    hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
    result = db.users.find_one({"username": user_username})
    if result == None:
        return message_response(False, "User doesn't exist")
    if hash == result['password']:
        db.users.delete_one({"uuid": result["uuid"]})
        return message_response(True, "User account deleted")
    else:
        return message_response(False, "Password doesn't match")