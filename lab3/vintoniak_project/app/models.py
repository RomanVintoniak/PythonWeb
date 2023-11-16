from app import db
from datetime import datetime

class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

class Feedback(db.Model):
    __tablename__ = "feedbacks"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(100), unique=True)
    content = db.Column(db.String(250))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, email, content):
        self.username = username
        self.email = email
        self.content = content
        

