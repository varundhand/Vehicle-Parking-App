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
    name = data['name']
    location = data['location']
    price = data.get('price', 10)
    spots_count = data.get('spots', 0)

    lot = ParkingLot(name=name, location=location, price=price)
    db.session.add(lot)
    db.session.commit()

    # Add initial parking spots
    for _ in range(spots_count):
        spot = ParkingSpot(lot_id=lot.id, status='A')
        db.session.add(spot)
    db.session.commit()

    return jsonify({"message": f"Parking lot '{name}' created with {spots_count} spots."}), 201

# Get all parking lots
@admin_bp.route('/parking-lots', methods=['GET'])
@jwt_required()
@admin_required
def get_parking_lots():
    lots = ParkingLot.query.all()
    return jsonify([{"id": lot.id, "name": lot.name, "location": lot.location, "price": lot.price} for lot in lots]), 200

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

# Search user by email
@admin_bp.route('/search-user', methods=['GET'])
@jwt_required()
def search_user_by_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"message": "Email required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "name": user.full_name or "",
        "address": user.address or "",
        "pincode": user.pincode or "",
    }), 200

# Returns total revenue generated per parking lot
@admin_bp.route('/summary/revenue', methods=['GET'])
@jwt_required()
def summary_revenue():
    lots = ParkingLot.query.all()
    result = []

    for lot in lots:
        revenue = sum(
            res.parking_cost or 0
            for spot in lot.spots
            for res in spot.reservations
            if not res.is_active
        )
        result.append({
            "lot": lot.name,
            "revenue": round(revenue, 2)
        })

    return jsonify(result), 200

# Returns total and avaible parking spots per parking lot
@admin_bp.route('/summary/availability', methods=['GET'])
@jwt_required()
def summary_availability():
    lots = ParkingLot.query.all()
    result = []

    for lot in lots:
        total = len(lot.spots)
        occupied = len([s for s in lot.spots if s.status == 'O'])
        available = total - occupied
        result.append({
            "lot": lot.name,
            "total": total,
            "occupied": occupied,
            "available": available
        })

    return jsonify(result), 200

