from . import db

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # A = Available, O = Occupied
    def __repr__(self):
        return f"<ParkingSpot {self.id} in Lot {self.lot_id} - Status: {self.status}>"
    # No direct reservation relationship needed here

    # reservation = db.relationship('Reservation', backref='spot', uselist=False) # one-to-one relationship with Reservation