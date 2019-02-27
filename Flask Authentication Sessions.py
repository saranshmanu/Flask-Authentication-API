from flask import Flask, redirect, url_for, request, render_template, jsonify
from Crypto.Hash import SHA512
from pymongo import MongoClient
from flask import Flask
from flask_mail import Mail, Message
from bson import ObjectId
import uuid


host = "localhost"
port = "9000"

app = Flask(__name__)
emailID = 'saranshmanu@yahoo.co.in'
app.config['MAIL_SERVER']='smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = emailID
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


databaseLink = "mongodb://saransh.xyz"
name_of_the_database = "new_database"
client = MongoClient(databaseLink)
db = client[name_of_the_database]
posts = db.posts

@app.route('/auth/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Checking if the length of the fields are exceeding the limit or not 
    if len(password) > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of password exceeded the limit"
        }
        return jsonify(response)

    if len(username) > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of username exceeded the limit"
        }
        return jsonify(response)

    result = posts.find_one({"username": username})
    if result != None:
        # The user is successfully found
        if result['email_confirmation'] == False:
            response = {
                "success": False,
                "message": "Email hasn't been confirmed"
            }
            return jsonify(response)
        # User has confirmed the email id and now continuing
        hash = SHA512.new(password.encode('utf-8')).hexdigest()
        returned_hash = result['password']
        if hash == returned_hash: 
            # Password matched successfully
            success = True 
            message = "Login Successful"
        else:
            # Password doesn't match
            success = False
            message = "User found. Password does not match"
    else:
        # The user doen't exist
        success = False
        message = "User doesn't found."

    response = {
        "success"   : success,
        "message"   : message
    }
    return jsonify(response)

@app.route('/auth/register', methods = ['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Checking if the length of the fields are exceeding the limit or not
    if len(password) > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of password exceeded the limit"
        }
        return jsonify(response)

    if len(username) > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of username exceeded the limit"
        }
        return jsonify(response)

    if len(email) > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of email exceeded the limit"
        }
        return jsonify(response)

    # Finding if the user is already registered before
    result = posts.find_one({"username": username})
    if result != None:
        # User already existed
        response = {
            "success": False,
            "message": "User already registered"
        }
        return jsonify(response)
    else:
        # Registering the user
        unique_id = uuid.uuid4().hex
        try:
            msg = Message('Confirm the email to continue', sender = emailID, recipients = [email])
            confirmation_url = 'http://' + host + ":" + port + "/auth/email_confirmation/" + unique_id
            msg.html = '<HTML><a href = "' + str(confirmation_url) + '">Press to verify the mail</a></HTML>'
            mail.send(msg)
            password_hash = SHA512.new(password.encode('utf-8')).hexdigest()
            dictionary = {
                "email"     : email,
                "username"  : username,
                "password"  : password_hash,
                "email_confirmation": False,
                "uuid": unique_id
            }
            result = posts.insert_one(dictionary)
            response = {
                "success": True,
                "message": "User registered successfully. Confirm the mail to continue"
            }
            return jsonify(response)
        except:
            response = {
                "success": False,
                "message": "Mail server not responding. Try again after some time"
            }
            return jsonify(response)
        

@app.route('/auth/email_confirmation/<token>', methods = ['GET'])
def email_confirmation(token):
    unique_id = token
    result = posts.find_one({"uuid": unique_id})
    if result == None:
        response = {
            "success": False,
            "message": "User not found"
        }
        return jsonify(response)

    if result['email_confirmation'] == True:
        response = {
            "success": False,
            "message": "User already verified the email"
        }
        return jsonify(response)

    try:
        msg = Message('Email Successfully Confirmed', sender = emailID, recipients = ['saransh.mittal1998@gmail.com'])
        msg.body = "Welcome Sir!"
        mail.send(msg)
        posts.update_one(
            {"uuid": unique_id},
            {"$set": {"email_confirmation":True}}
        )
        response = {
            "success"   : True,
            "message"   : "Successfully confirmed the email"
        }
        return jsonify(response)
    except:
        response = {
            "success"   : False,
            "message"   : "Mail server not responding. Try again after some time"
        }
        return jsonify(response)

@app.route('/auth/logout', methods = ['POST'])
def logout():
    return redirect(url_for('hello_world'))

@app.route('/auth/reset_password', methods = ['POST'])
def reset_password():
    return redirect(url_for('hello_world'))

@app.route('/auth/resend_email_confirmation', methods = ['POST'])
def resend_email_confirmation():
    return redirect(url_for('hello_world'))

@app.route('/auth/delete_account', methods = ['POST'])
def delete_account():
    return redirect(url_for('hello_world'))

if __name__ == '__main__':
    app.run(host, port)