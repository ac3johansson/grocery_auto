from models import db

class Ingredient(db.Model):
    #__tablename__ = 'ingredient'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer())
    unit = db.Column(db.String(5))
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=False)

    unitsWeight = {'g':1, 'hg':100, 'kg':1000} #Valid weight units
    unitsVolume = {'krm':1, 'tsk':5, 'msk':15, 'ml':1, 'cl':10, 'dl':100, 'l':1000} #Valid volume units
    unitsDistinct = ('st', 'knippe')