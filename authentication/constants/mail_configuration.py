from authentication.constants.environment_variables import EMAIL_ID, EMAIL_PASSWORD
from authentication.constants.host_configuration import server
from flask_mail import Mail

server.config['MAIL_SERVER']='smtp.mail.yahoo.com'
server.config['MAIL_PORT'] = 465
server.config['MAIL_USERNAME'] = EMAIL_ID
server.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
server.config['MAIL_USE_TLS'] = False
server.config['MAIL_USE_SSL'] = True
mail = Mail(server)