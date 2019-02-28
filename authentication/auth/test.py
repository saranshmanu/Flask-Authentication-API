from authentication.constants.environment_variables import JWT_ALGORITHM, JWT_SECRET
from authentication.utils.helper_functions import message_response
from flask import request, Blueprint
import jwt

test_blueprint = Blueprint("test", __name__)
@test_blueprint.route('/test', methods = ['POST'])
def test():
    try:
        decoded_data = jwt.decode(request.form['token'], JWT_SECRET, algorithms= JWT_ALGORITHM)
        decrypted_uuid = decoded_data['uuid']
        return message_response(True, decrypted_uuid)
    except jwt.ExpiredSignatureError:
        return message_response(False, "Token Expired")
    except jwt.DecodeError:
        return message_response(False, "Invalid Token")