from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name: str):
    #Construct the core application.
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
    
    db.init_app(app)
    Migrate(app, db)
    
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
        app.register_blueprint(todo)
        app.register_blueprint(feedback)
        app.register_blueprint(portfolio)
        app.register_blueprint(auth)
        app.register_blueprint(cookie_bp)
        app.register_blueprint(post)
        app.register_blueprint(category)
        
        from app import views
        
        return app