import config
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    """
    Function that creates a Flask application.
    :return: Initialized Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    JWTManager(app)
    api = Api(app)

    # all the resources
    api.add_resource(UserRegistration, '/register')
    api.add_resource(UserLogin, '/auth')
    api.add_resource(UsersResource, '/user')

    return app

from app.resources.users_resource import UserRegistration, UserLogin, UsersResource
