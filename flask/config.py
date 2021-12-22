import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///'+ os.path.join(basedir, 'data.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
#flask_jwt_extended JWT_SECRET_KEY
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-for-dev')
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
