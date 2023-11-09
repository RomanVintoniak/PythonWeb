import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'mysecretkey'

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'app/data.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False