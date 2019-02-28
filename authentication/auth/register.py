from authentication.constants.host_configuration import db, host, port
from authentication.constants.environment_variables import EMAIL_ID
from authentication.constants.mail_configuration import mail
from authentication.utils.helper_functions import message_response
from flask import request, Blueprint
from Crypto.Hash import SHA512
from flask_mail import Message
import uuid

register_blueprint = Blueprint("register", __name__)
@register_blueprint.route('/auth/register', methods = ['POST'])
def register():
    user_username = request.form['username']
    user_password = request.form['password']
    user_email = request.form['email']
    success = True

    # Checking if the length of the fields are exceeding the limit or not
    if len(user_password) > 30 :
        message = "Length of password exceeded the limit"
        success = False
    elif len(user_username) > 30 :
        message = "Length of username exceeded the limit"
        success = False
    elif len(user_email) > 30 :
        message = "Length of email exceeded the limit"
        success = False
    if success == False:
        return message_response(success, message)

    # Finding if the user is already registered before
    result = db.users.find_one({"username": user_username})
    if result != None:
        # User already existed
        return message_response(False, "User already registered")
    try:
        # Registering the user
        unique_id = uuid.uuid4().hex
        # Sending the verification email to the user
        email = Message('Confirm the email to continue', sender = EMAIL_ID, recipients = [user_email])
        confirmation_url = 'http://' + host + ":" + port + "/auth/email_confirmation/" + unique_id
        email.html = '<HTML><a href = "' + str(confirmation_url) + '">Press to verify the mail</a></HTML>'
        mail.send(email)
        # Creating the password hash for the user ad storing in the database
        password_hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
        user = {
            "email"     : user_email,
            "username"  : user_username,
            "password"  : password_hash,
            "email_confirmation": False,
            "uuid": unique_id
        }
        db.users.insert_one(user)
        return message_response(True, "User registered successfully. Confirm the mail to continue")
    except:
        return message_response(False, "Mail server not responding. Try again after some time")