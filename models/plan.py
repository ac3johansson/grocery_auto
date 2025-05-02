from models import db
from zoneinfo import ZoneInfo
from datetime import datetime
from models import association

class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.Date, default=lambda: datetime.now(ZoneInfo("Europe/Berlin")).date())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    
    recipes = db.relationship('Recipe', secondary=association.plan_recipe_association, backref='plans', lazy=True)
    ingredients = db.relationship('PlanIngredient', backref='plan', lazy=True, cascade="all, delete-orphan")