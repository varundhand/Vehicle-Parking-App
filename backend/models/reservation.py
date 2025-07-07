from . import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    parking_time = db.Column(db.DateTime, default=datetime.utcnow)
    release_time = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, default=0.0)