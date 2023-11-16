from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20),  nullable=False, default="default.jpg")
    password = db.Column(db.String(120), nullable=False)
    aboutMe = db.Column(db.String(500), nullable=True, default="")
    lastSeen = db.Column(db.DateTime, default=datetime.now())
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def __repr__(self):
        return f"{self.id} -- {self.username} -- {self.email}"
    
    def checkPassword(self, pwd):
        return check_password_hash(self.password, pwd)