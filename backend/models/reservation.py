from . import db
from datetime import datetime

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    vehicle_number = db.Column(db.String(20))
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    parking_cost = db.Column(db.Float, nullable=True)
    is_active = db.Column(db.Boolean, default=True)


    spot = db.relationship('ParkingSpot', backref='reservations')  # now safe!
    # user = db.relationship('User', backref='reservations')
    def __repr__(self):
        return f"<Reservation {self.id} for User {self.user_id} at Spot {self.spot_id}>"