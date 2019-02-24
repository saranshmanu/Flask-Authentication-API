from flask import Flask, redirect, url_for, request, render_template, jsonify
app = Flask(__name__)

@app.route('/auth/login', methods = ['POST'])
def login():
    dictionary = {
        "username":request.form['username'],
        "method": "POST",
        "message": "You have requested through POST method"
    }
    return jsonify(dictionary)

@app.route('/auth/resgister', methods = ['POST'])
def register():
   return redirect(url_for('hello_world'))

host = "localhost"
port = "9000"
if __name__ == '__main__':
   # this starts the server on the localhost on the specifiecd port as given
   app.run(host, port)

# # name variable is used from the url to execute the below route is executed
# @app.route('/name/<name>')
# def functionTwo(name):
#    if name == None:
#       name = "Admin"
#    return "Hello %s! Welcome to the development club :)" % name

# @app.route('/protocol',methods = ['POST', 'GET'])
# def functionThree():
#    # print(request.method) this method will tell about the method being used for the network call
#    # if the POST method is called the below is executed
#    if request.method == "POST":
#       dictionary = {
#          "username":request.form['username'],
#          "method": "POST",
#          "message": "You have requested through POST method"
#       }
#       # jsonify function is used to convert the created dictionary into a JSON format
#       return jsonify(dictionary)
#    # if the GET method is called the below is executed
#    elif request.method == "GET":
#       print(request.args.get("argument"))
#       dictionary = {
#          "method":"GET",
#          "message":"You have requested through GET method"
#       }
#       return jsonify(dictionary)
#    # if any other protocol method is used the below is executed
#    else:
#       return "The protocol not recognised"

# # a simple network route created
# @app.route('/')
# def hello_world():
#    return "This will return the result for the given input"