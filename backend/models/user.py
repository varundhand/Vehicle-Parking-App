from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    pincode = db.Column(db.String(10))
    role = db.Column(db.String(10), nullable=False, default='user')  # 'admin' or 'user' # allows us to distinguish between admin and user roles

    reservations = db.relationship('Reservation', backref='user', lazy=True) # one-to-many relationship with Reservation