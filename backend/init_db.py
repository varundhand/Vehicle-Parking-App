from flask import Flask
from models import db
from models.user import User
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation
from config import DATABASE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    # Pre-create admin user (no registration needed)
    admin = User(email='admin@admin.com', password='admin123', role='admin')
    db.session.add(admin)
    db.session.commit()
    print("Database initialized and admin created!")