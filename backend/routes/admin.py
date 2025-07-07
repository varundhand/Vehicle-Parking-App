from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.user import User
from models.reservation import Reservation

admin_bp = Blueprint('admin', __name__)

# Middleware to allow only admin
def admin_required(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity or identity.get("role") != "admin":
            return jsonify({"message": "Admins only!"}), 403
        return fn(*args, **kwargs)

    return wrapper

# Create new parking lot
@admin_bp.route('/parking-lots', methods=['POST'])
@jwt_required()
@admin_required
def create_parking_lot():
    data = request.json
    lot = ParkingLot(name=data['name'], location=data['location'])
    db.session.add(lot)
    db.session.commit()
    return jsonify({"message": "Parking lot created"}), 201

# Get all parking lots
@admin_bp.route('/parking-lots', methods=['GET'])
@jwt_required()
@admin_required
def get_parking_lots():
    lots = ParkingLot.query.all()
    return jsonify([{"id": lot.id, "name": lot.name, "location": lot.location} for lot in lots]), 200

# Get all the users
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "address": user.address,
            "pincode": user.pincode
        }
        for user in users
    ]), 200

# Add parking spots to a parking lot
@admin_bp.route('/parking-spots', methods=['POST'])
@jwt_required()
@admin_required
def add_parking_spots():
    data = request.json
    lot_id = data.get('lot_id')
    count = data.get('count', 0)

    lot = ParkingLot.query.get(lot_id)
    if not lot:
        return jsonify({"message": "Parking lot not found"}), 404

    for i in range(count):
        spot = ParkingSpot(lot_id=lot.id, status='A')
        db.session.add(spot)

    db.session.commit()
    return jsonify({"message": f"{count} spots added to parking lot {lot.name}"}), 201
