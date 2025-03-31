from models import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    recipes = db.relationship('Recipe', backref='user', lazy=True, cascade="all, delete-orphan")  # One-to-Many
