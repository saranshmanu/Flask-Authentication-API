from authentication.auth.login import login_blueprint
from authentication.auth.register import register_blueprint
from authentication.auth.delete_account import delete_account_blueprint
from authentication.auth.email_verification import email_confirmation_blueprint
from authentication.auth.reset_password import reset_password_blueprint
from authentication.auth.resend_email_confirmation import resend_email_confirmation_blueprint
from authentication.auth.test import test_blueprint
from authentication.constants.host_configuration import host, port, server

server.register_blueprint(login_blueprint)
server.register_blueprint(register_blueprint)
server.register_blueprint(delete_account_blueprint)
server.register_blueprint(email_confirmation_blueprint)
server.register_blueprint(reset_password_blueprint)
server.register_blueprint(resend_email_confirmation_blueprint)
server.register_blueprint(test_blueprint)

if __name__ == '__main__':
    server.run(host, port, debug=True)