import enum
from app import db
from datetime import datetime
from app.category.models import Category

class PostTypes(enum.Enum):
    SPORT = 1
    NEWS = 2
    MEMES = 3
    PUBLICATION = 4
    OTHER = 5
    

class Post(db.Model):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.String(750))
    image = db.Column(db.String(50), nullable=False, default="defaultPostImg.jpg")
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    postType = db.Column(db.Enum(PostTypes), default="PUBLICATION")
    enabled = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    category_id = db.Column(db.Integer, db.ForeignKey('сategories.id', name="category"), nullable=True)
#    category = db.relationship('Category', backref=db.backref('posts', lazy=True))
    
    def __repr__(self):
        return f"id: {self.id} | title: {self.title} | createdAt: \
            {self.createdAt.strftime('%d-%m-%Y %H:%M:%S')}"
    
    
    
    