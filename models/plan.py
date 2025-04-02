from models import db
from zoneinfo import ZoneInfo
from datetime import datetime

class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.Date, default=lambda: datetime.now(ZoneInfo("Europe/Berlin")).date())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)