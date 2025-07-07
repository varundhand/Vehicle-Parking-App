from routes.auth import auth_bp
from routes.admin import admin_bp  # ✅
from routes.user import user_bp
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # 👈

from config import DATABASE_URL, JWT_SECRET_KEY
from models import db
from models.user import User
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation

from routes.auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

CORS(app)  # 👈 enable cross-origin requests

db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

#* before:
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin") 
app.register_blueprint(user_bp, url_prefix="/api/user")
#* after:
# app.register_blueprint(admin_bp, url_prefix="/api/auth")

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(email='admin@admin.com', password=bcrypt.generate_password_hash('admin123').decode('utf-8'), role='admin')
        db.session.add(admin)
        db.session.commit()
        print("Database initialized and admin created!")

    app.run(debug=True)
