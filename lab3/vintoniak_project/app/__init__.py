from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import config


db = SQLAlchemy()
login_manager = LoginManager()
basic_auth = HTTPBasicAuth(scheme='Bearer')
ma = Marshmallow()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Test application"
    },
)

def create_app(config_name: str):
    #Construct the core application.
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    
    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    with app.app_context():
        # Imports
        from .todo.views import todo
        from .feedback.views import feedback
        from .portfolio.views import portfolio
        from .authentication.views import auth
        from .cookie.views import cookie_bp
        from .post.views import post
        from .category.views import category
        from .api import api_bp
        from .user_api import users_api
        app.register_blueprint(todo)
        app.register_blueprint(feedback)
        app.register_blueprint(portfolio)
        app.register_blueprint(auth)
        app.register_blueprint(cookie_bp)
        app.register_blueprint(post)
        app.register_blueprint(category)
        app.register_blueprint(api_bp)
        app.register_blueprint(users_api)
        app.register_blueprint(swaggerui)
        
        from app import views
        
        return app
