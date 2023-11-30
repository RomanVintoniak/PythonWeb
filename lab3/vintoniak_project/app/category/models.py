from app import db

class Category(db.Model):
    __tablename__ = "сategories"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    posts = db.relationship('Post', backref='category', lazy=True)