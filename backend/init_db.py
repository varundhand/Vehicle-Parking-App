from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask import jsonify
from flask_mail import Mail

from config import (
    DATABASE_URL, JWT_SECRET_KEY, redis_client,
    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, 
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
)
from models import db
from models.user import User
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation

# Import Blueprints
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# Configure Flask-Mail
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

# ✅ CORS setup (allow requests from Vue dev server)
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5180",
    "http://localhost:5187",
    "http://localhost:5188", 
    "http://localhost:5189", 
    "http://localhost:5190", 
    "http://localhost:5191", 
    "http://localhost:5192", 
    "http://localhost:5193", 
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5180",
    "http://127.0.0.1:5187",
    "http://127.0.0.1:5188",
    "http://127.0.0.1:5189",
    "http://127.0.0.1:5190",
    "http://127.0.0.1:5191",
    "http://127.0.0.1:5192",
    "http://127.0.0.1:5193",
])

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
mail = Mail(app)  # Initialize Flask-Mail

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(user_bp, url_prefix="/api/user")

# ✅ Optional: CORS test route
@app.route("/api/test", methods=["OPTIONS"])
def test_options():
    return "OK", 200

# ✅ Test Redis connection
def test_redis():
    try:
        redis_client.ping()
        print("✅ Redis connection successful!")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")

# ✅ Run and initialize DB
if __name__ == "__main__":
    with app.app_context():
        # Test Redis connection
        test_redis()
        
        db.drop_all()
        db.create_all()

        # Create default admin user
        admin = User(
            email='admin@admin.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

        print("✅ Database initialized and admin created!")

    # Run server
    app.run(debug=True)