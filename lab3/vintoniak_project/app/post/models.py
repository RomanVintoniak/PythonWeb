import enum
from app import db
from datetime import datetime
from app.authentication.models import User

class PostTypes(enum.Enum):
    SPORT = 1
    NEWS = 2
    MEMES = 3
    OTHER = 4
    

class Post(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.String(750))
    image = db.Column(db.String(50), nullable=False, default="defaultPostImg.jpg")
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    postType = db.Column(db.Enum(PostTypes), default="OTHER")
    enabled = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship(User, overlaps="author, posts")
    
    def __init__(self, title, text):
        self.title = title
        self.text = text
    
    def __repr__(self):
        return f"id: {self.id} | title: {self.title} | createdAt: \
            {self.createdAt.strftime('%d-%m-%Y %H:%M:%S')}"
    
    
    
    