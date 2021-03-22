from flask import Flask
from flask_restful import Api
from .classes.UsersResource import UsersResource


app = Flask(__name__)
api = Api(app)


