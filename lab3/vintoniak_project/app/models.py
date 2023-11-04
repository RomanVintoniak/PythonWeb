from app import db
from datetime import datetime


class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

class Review(db.Model):
    __tablename__ = "review"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(100), unique=True)
    content = db.Column(db.String(250))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, email, content):
        self.username = username
        self.email = email
        self.content = content
        

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Colimn(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20),  nullable=False, default="default.jpg")
    password = db.Column(db.String(120), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f"{self.id} -- {self.username} -- {self.email}"