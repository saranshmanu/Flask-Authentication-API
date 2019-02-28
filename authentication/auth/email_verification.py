from authentication.constants.host_configuration import db
from authentication.constants.mail_configuration import mail
from authentication.constants.environment_variables import EMAIL_ID
from authentication.utils.helper_functions import message_response
from flask_mail import Message
from flask import Blueprint

email_confirmation_blueprint = Blueprint("email_confirmation", __name__)
@email_confirmation_blueprint.route('/auth/email_confirmation/<token>', methods = ['GET'])
def email_confirmation(token):
    unique_id = token
    result = db.users.find_one({"uuid": unique_id})
    if result == None:
        return message_response(False, "User not found")
    if result['email_confirmation'] == True:
        return message_response(False, "User already verified the email")
    try:
        # Sending the confirmation email to the user
        email = Message('Email Successfully Confirmed', sender = EMAIL_ID, recipients = [result['email']])
        email.body = "Welcome Sir!"
        mail.send(email)
        # Updating the database that the user has verified the email
        db.users.update_one(
            {"uuid": unique_id},
            {"$set": {"email_confirmation":True}}
        )
        return message_response(True, "Successfully confirmed the email")
    except:
        return message_response(False, "Mail server not responding. Try again after some time")