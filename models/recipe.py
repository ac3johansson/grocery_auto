from models import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    #tag = db.relationship('Tag', backref='recipe', lazy=True, cascade="all, delete-orphan")
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True, cascade="all, delete-orphan")

