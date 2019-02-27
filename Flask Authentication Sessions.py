from flask import Flask, redirect, url_for, request, render_template, jsonify
from Crypto.Hash import SHA512
from pymongo import MongoClient

app = Flask(__name__)

databaseLink = "mongodb://saransh.xyz"
name_of_the_database = "new_database"
client = MongoClient(databaseLink)
db = client[name_of_the_database]
posts = db.posts

@app.route('/auth/login', methods = ['POST'])
def login():
    username = request.form['username'].encode('utf-8')
    password = request.form['password'].encode('utf-8')

    # Checking if the length of the fields are exceeding the limit or not 
    if password.length > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of password exceeded the limit"
        }
        return jsonify(response)

    if username.length > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of username exceeded the limit"
        }
        return jsonify(response)

    result = posts.find_one({"username": username})
    if result != None:
        # The user is successfully found
        hash = SHA512.new(password).hexdigest()
        returned_hash = result['password']
        if hash == returned_hash: 
            # Password matched successfully
            success = True 
            message = "User found. Password does match"
        else:
            # Password doesn't match
            success = False
            message = "User found. Password does not match"
    else:
        # The user doen't exist
        success = False
        message = "User didn't found."

    response = {
        "success"   : success,
        "message"   : message
    }
    return jsonify(response)

@app.route('/auth/register', methods = ['POST'])
def register():
    username = request.form['username'].encode('utf-8')
    password = request.form['password'].encode('utf-8')
    email = request.form['email'].encode('utf-8')

    # Checking if the length of the fields are exceeding the limit or not
    if password.length > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of password exceeded the limit"
        }
        return jsonify(response)

    if username.length > 30 :
        response = {
            "success"   : False,
            "message"   : "Length of username exceeded the limit"
        }
        return jsonify(response)

    if email.length > 30 :
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
        password_hash = SHA512.new(password).hexdigest()
        dictionary = {
            "email"     : email,
            "username"  : username,
            "password"  : password_hash
        }
        result = posts.insert_one(dictionary)
        response = {
            "success": True,
            "message": "User registered successfully"
        }
        return jsonify(dictionary)

@app.route('/auth/email_confirmation', methods = ['POST'])
def email_confirmation():
    return redirect(url_for('hello_world'))

host = "localhost"
port = "9000"
if __name__ == '__main__':
    app.run(host, port)