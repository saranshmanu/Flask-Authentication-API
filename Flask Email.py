from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
emailID = 'EMAIL'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = emailID
app.config['MAIL_PASSWORD'] = 'PASSWORD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
    msg = Message('Hello', sender = emailID, recipients = ['abcd@abcd.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"

host = "localhost"
port = "9001"

if __name__ == '__main__':
    app.run(host, port)