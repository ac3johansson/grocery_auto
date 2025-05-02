from models import db

class PlanIngredient(db.Model):
    __tablename__ = 'plan_ingredient'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    fromRecipe = db.Column(db.Boolean(), nullable=False)
    #recipe_id = db.Column(db.Integer(), db.ForeignKey('recipe.id', ondelete="CASCADE"), nullable=True)
    plan_id = db.Column(db.Integer(), db.ForeignKey('plan.id', ondelete="CASCADE"), nullable=True)

    unitsWeight = {'g':1, 'hg':100, 'kg':1000} #Valid weight units
    unitsVolume = {'krm':1, 'tsk':5, 'msk':15, 'ml':1, 'cl':10, 'dl':100, 'l':1000} #Valid volume units
    unitsDistinct = {'st':1, 'port':1, 'paket':1}