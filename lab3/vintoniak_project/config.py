import os
from os import path, environ

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = environ.get('SECRET_KEY') or \
        'mysecretkey'
    FLASK_SECRET = SECRET_KEY


class LocalConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/data.sqlite')

    
config = {
    'local': LocalConfig,
}