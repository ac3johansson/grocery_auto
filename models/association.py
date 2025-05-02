from models import db

plan_recipe_association = db.Table('plan_recipe',
    db.Column('plan_id', db.Integer, db.ForeignKey('plan.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)