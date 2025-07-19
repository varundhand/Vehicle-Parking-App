from models import db

class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete-orphan") # one-to-many relationship with ParkingSpot
    def __repr__(self):
        return f"<ParkingLot {self.id} - {self.name} at {self.location}>"