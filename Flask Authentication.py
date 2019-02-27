from flask import Flask, redirect, url_for, request, render_template, jsonify
from Crypto.Hash import SHA512
from pymongo import MongoClient
from flask_mail import Mail, Message
from bson import ObjectId
import uuid
import jwt
import datetime

host = "localhost"
port = "9000"

# --------------------------------------ENVIRONMENT VARIABLES---------------------------------------------

EMAIL_ID = 'saranshmanu@yahoo.co.in'
EMAIL_PASSWORD = 'password'
JWT_SECRET = "THIS_IS_THE_JWT_SECRET"
JWT_ALGORITHM = ['HS256']
JWT_EXPIRATION_DURATION = 1000
DATABASE_LINK = "mongodb://saransh.xyz"
NAME_OF_THE_DATABASE = "USER_DATABASE"

# --------------------------------------MAIL VARIABLE CONFIGURATION----------------------------------------

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = EMAIL_ID
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

client = MongoClient(DATABASE_LINK)
db = client[NAME_OF_THE_DATABASE]

@app.route('/test', methods = ['POST'])
def test():
    try:
        decoded_data = jwt.decode(request.form['token'], JWT_SECRET, algorithms= JWT_ALGORITHM)
        decrypted_uuid = decoded_data['uuid']
        return jsonify({
            "success":  True,
            "uuid"   :  decrypted_uuid
        })
    except jwt.ExpiredSignatureError:
        return jsonify({
            "success":  False,
            "message":  "Token Expired"
        })
    except jwt.DecodeError:
        return jsonify({
            "success":  False,
            "message":  "Invalid Token"
        })

@app.route('/auth/login', methods = ['POST'])
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
        return jsonify({
            "success"   : False,
            "message"   : message
        })

    result = db.users.find_one({"username": user_username})
    if result != None:
        # The user is successfully found
        if result['email_confirmation'] == False:
            return jsonify({
                "success": False,
                "message": "Email hasn't been confirmed"
            })
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
            # Password doesn't match
            success = False
            message = "User found. Password does not match"
    else:
        # The user doen't exist
        return jsonify({
            "success": False,
            "message": "User doesn't found."
        })

@app.route('/auth/register', methods = ['POST'])
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
        return jsonify({
            "success"   : False,
            "message"   : message
        })

    # Finding if the user is already registered before
    result = db.users.find_one({"username": user_username})
    if result != None:
        # User already existed
        return jsonify({
            "success": False,
            "message": "User already registered"
        })
    else:
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
            return jsonify({
                "success": True,
                "message": "User registered successfully. Confirm the mail to continue"
            })
        except:
            return jsonify({
                "success": False,
                "message": "Mail server not responding. Try again after some time"
            })
        

@app.route('/auth/email_confirmation/<token>', methods = ['GET'])
def email_confirmation(token):
    unique_id = token
    result = db.users.find_one({"uuid": unique_id})
    if result == None:
        return jsonify({
            "success": False,
            "message": "User not found"
        })

    if result['email_confirmation'] == True:
        return jsonify({
            "success": False,
            "message": "User already verified the email"
        })

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
        return jsonify({
            "success"   : True,
            "message"   : "Successfully confirmed the email"
        })
    except:
        return jsonify({
            "success"   : False,
            "message"   : "Mail server not responding. Try again after some time"
        })

@app.route('/auth/delete_account', methods = ['POST'])
def delete_account():
    user_password = request.form['password']
    user_username = request.form['username']
    hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
    result = db.users.find_one({"username": user_username})
    if result == None:
        return jsonify({
            "success"   : False,
            "message"   : "User doesn't exist"
        })
    if hash == result['password']:
        db.users.delete_one({"uuid": result["uuid"]})
        return jsonify({
            "success"   : True,
            "message"   : "User account deleted"
        })
    else:
        return jsonify({
            "success"   : False,
            "message"   : "Password doesn't match"
        })

@app.route('/auth/reset_password', methods = ['POST'])
def reset_password():
    user_password = request.form['password']
    user_new_password = request.form['new_password']
    user_username = request.form['username']
    hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
    new_hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
    result = db.users.find_one({"username": user_username})
    if result == None:
        return jsonify({
            "success"   : False,
            "message"   : "User doesn't exist"
        })
    if hash == result['password']:
        db.users.update_one(
            {"uuid": result['uuid']},
            {"$set": {"password":new_hash}}
        )
        return jsonify({
            "success"   : True,
            "message"   : "User password changed successfully"
        })
    else:
        return jsonify({
            "success"   : False,
            "message"   : "Password doesn't match"
        })

@app.route('/auth/resend_email_confirmation', methods = ['POST'])
def resend_email_confirmation():
    user_password = request.form['password']
    user_username = request.form['username']
    hash = SHA512.new(user_password.encode('utf-8')).hexdigest()
    result = db.users.find_one({"username": user_username})
    if result == None:
        return jsonify({
            "success"   : False,
            "message"   : "User doesn't exist"
        })
    if hash == result['password']:
        # Sending the verification email to the user
        email = Message('Confirm the email to continue', sender = EMAIL_ID, recipients = [result['email']])
        confirmation_url = 'http://' + host + ":" + port + "/auth/email_confirmation/" + result['uuid']
        email.html = '<HTML><a href = "' + str(confirmation_url) + '">Press to verify the mail</a></HTML>'
        mail.send(email)
        return jsonify({
            "success"   : True,
            "message"   : "Verification email sent to the user"
        })
    else:
        return jsonify({
            "success"   : False,
            "message"   : "Password doesn't match"
        })

@app.route('/auth/logout', methods = ['POST'])
def logout():
    return redirect(url_for('hello_world'))

if __name__ == '__main__':
    app.run(host, port)