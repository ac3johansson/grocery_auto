from models import db

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id'), nullable=False)