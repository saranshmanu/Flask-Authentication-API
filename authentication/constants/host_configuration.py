from authentication.constants.environment_variables import NAME_OF_THE_DATABASE, DATABASE_LINK
from pymongo import MongoClient
from flask import Flask, Blueprint

host = "localhost"
port = "9000"
client = MongoClient(DATABASE_LINK)
db = client[NAME_OF_THE_DATABASE]

server = Flask(__name__)
