import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from .todo.views import todo
from .feedback.views import feedback
from .portfolio.views import portfolio
from .authentication.views import auth
app.register_blueprint(todo)
app.register_blueprint(feedback)
app.register_blueprint(portfolio)
app.register_blueprint(auth)



from app import views