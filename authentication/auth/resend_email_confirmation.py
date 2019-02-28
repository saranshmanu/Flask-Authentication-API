from authentication.constants.host_configuration import db, host, port
from authentication.constants.environment_variables import EMAIL_ID
from authentication.constants.mail_configuration import mail
from authentication.utils.helper_functions import message_response
from flask import request, Blueprint
from Crypto.Hash import SHA512
from flask_mail import Message


resend_email_confirmation_blueprint = Blueprint("resend_email_confirmation", __name__)
@resend_email_confirmation_blueprint.route('/auth/resend_email_confirmation', methods = ['POST'])
def resend_email_confirmation():
    user_password = request.form['password']
    user_username = request.form['username']
    hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
    result = db.users.find_one({"username": user_username})
    if result == None:
        return message_response(False, "User doesn't exist")
    if hash == result['password']:
        # Sending the verification email to the user
        email = Message('Confirm the email to continue', sender = EMAIL_ID, recipients = [result['email']])
        confirmation_url = 'http://' + host + ":" + port + "/auth/email_confirmation/" + result['uuid']
        email.html = '<HTML><a href = "' + str(confirmation_url) + '">Press to verify the mail</a></HTML>'
        mail.send(email)
        return message_response(True, "Verification email sent to the user")
    else:
        return message_response(False, "Password doesn't match")