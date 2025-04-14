from models import db

plan_recipe_association = db.Table('plan_recipe',
    db.Column('plan_id', db.Integer, db.ForeignKey('plan.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

# plan_ingredient_association = db.Table('plan_ingredient',
#     db.Column('plan_id', db.Integer, db.ForeignKey('plan.id'), primary_key=True),
#     db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
# )
