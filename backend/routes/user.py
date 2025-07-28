# import datetime
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation
from models.user import User
from redis_client import redis_client
import json

user_bp = Blueprint('user', __name__)

@user_bp.route('/reserve', methods=['POST'])
@jwt_required()
def reserve_spot():
    # json body stored from post request
    data = request.json

    # extract user identity from JWT
    identity = get_jwt_identity()

    # extract user ID from identity so we can use it to query the database
    user_id = identity['id']

    # extract lot_id from the request data
    lot_id = data.get('lot_id')

    # checks if the user already has a reservation
    existing = Reservation.query.filter_by(user_id=user_id,is_active=True).first()
    
    #  to prevent multiple reservations by the same user
    #  even tho database allows one to many relationship of user to reservation, but the business logic requires only one reservation per user
    if existing:
        return jsonify({"message": "You already have a reservation"}), 400

    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not available_spot:
        return jsonify({"message": "Spot not available"}), 404

    available_spot.status = 'O'

    reservation = Reservation(user_id=user_id, spot_id=available_spot.id)
    db.session.add(reservation)
    db.session.commit()

    # Update the Redis cache to remove the reserved spot
    redis_client.delete("user:parking_lots")
    
    # Invalidate all user search cache
    for key in redis_client.scan_iter("user:search:*"):
        redis_client.delete(key)

    return jsonify({"message": "Spot reserved", "spot_id": available_spot.id}), 201

# Retrieve user's current reservation
@user_bp.route('/reservation', methods=['GET'])
@jwt_required()
def view_reservation():
    identity = get_jwt_identity()
    print("indentity: ",identity['id'])
    user_id = identity['id']
    reservation = Reservation.query.filter_by(user_id=user_id,is_active=True).first()

    
    if not reservation:
        return jsonify({"reservation": None}), 200

    return jsonify({
        "reservation":{
            "spot_id": reservation.spot.id,
            "lot_id": reservation.spot.lot.id,
            "lot_name": reservation.spot.lot.name,
            "status": reservation.spot.status
        }
    })

# Cancel user's reservation and update the cost 
@user_bp.route('/reservation', methods=['DELETE'])
@jwt_required()
def cancel_reservation():
    identity = get_jwt_identity()
    user_id = identity['id']
    reservation = Reservation.query.filter_by(user_id=user_id, is_active=True).first()

    if not reservation:
        return jsonify({"message": "No active reservation"}), 404

    reservation.spot.status = 'A'
    reservation.is_active = False
    reservation.leaving_timestamp = db.func.now()

    # ✅ Calculate duration in hours (rounded up)
    start = reservation.parking_timestamp
    end = datetime.utcnow()
    duration_in_hours = (end - start).total_seconds() / 3600
    duration_in_hours = max(1, round(duration_in_hours))  # Minimum 1 hour

    # ✅ Use lot's hourly rate if available, else default ₹10/hr
    rate = reservation.spot.lot.price or 10
    reservation.parking_cost = round(duration_in_hours * rate, 2)

    db.session.commit()

    # ❌ Invalidate parking lot cache
    redis_client.delete("user:parking_lots")

    # Invalidate all user search cache
    for key in redis_client.scan_iter("user:search:*"):
        redis_client.delete(key)



    return jsonify({
        "message": "Reservation cancelled",
        "duration_hours": duration_in_hours,
        "cost": reservation.parking_cost
    }), 200

    
# Get reservation history for the user
@user_bp.route('/reservations/history', methods=['GET'])
@jwt_required()
def reservation_history():
    identity = get_jwt_identity()
    user_id = identity['id']
    
    history = Reservation.query.filter_by(user_id=user_id).order_by(Reservation.parking_timestamp.desc()).all()

    result = []
    for r in history:
        result.append({
            "id": r.id,
            "location": r.spot.lot.location,
            "vehicle_number": r.vehicle_number,
            "timestamp": r.parking_timestamp.strftime('%Y-%m-%d %H:%M'),
            "is_active": r.is_active
        })
    
    return jsonify(result), 200

# Returns user's reservation count per lot 
@user_bp.route('/summary/history', methods=['GET'])
@jwt_required()
def user_summary():
    user_id = get_jwt_identity()['id']

    reservations = (
        db.session.query(ParkingLot.name, db.func.count(Reservation.id))
        .join(ParkingSpot, ParkingSpot.id == Reservation.spot_id)
        .join(ParkingLot, ParkingLot.id == ParkingSpot.lot_id)
        .filter(Reservation.user_id == user_id)
        .group_by(ParkingLot.name)
        .all()
    )

    result = [{"lot": lot, "count": count} for lot, count in reservations]
    return jsonify(result), 200


# Get all parking lots for the user
@user_bp.route('/parking-lots', methods=['GET'])
@jwt_required()
def get_parking_lots_for_user():
    cache_key = "user:parking_lots"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return jsonify(json.loads(cached_data)), 200

    lots = ParkingLot.query.all()
    response = [
        {
            "id": lot.id,
            "name": lot.name,
            "location": lot.location,
            "price": lot.price
        }
        for lot in lots
    ]

    # ⏱ Set cache with 5 minutes expiry
    redis_client.setex(cache_key, 300, json.dumps(response))

    return jsonify(response), 200


# Update user profile
@user_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()['id']
    data = request.json

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.full_name = data.get('full_name', user.full_name)
    user.address = data.get('address', user.address)
    user.pincode = data.get('pincode', user.pincode)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

# Search parking lots by location or lot name
@user_bp.route('/search-lots', methods=['GET'])
@jwt_required()
def search_lots():
    location = request.args.get('location')
    name = request.args.get('name')

    if not location and not name:
        return jsonify({"message": "Search query is required"}), 400

    cache_key = f"user:search:{location or ''}:{name or ''}".lower()
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return jsonify(json.loads(cached_data)), 200

    query = ParkingLot.query
    if location:
        query = query.filter(ParkingLot.location.ilike(f"%{location}%"))
    elif name:
        query = query.filter(ParkingLot.name.ilike(f"%{name}%"))

    lots = query.all()
    result = []

    for lot in lots:
        total_spots = len(lot.spots)
        available_spots = len([s for s in lot.spots if s.status == 'A'])

        result.append({
            "id": lot.id,
            "name": lot.name,
            "location": lot.location,
            "total_spots": total_spots,
            "available_spots": available_spots,
        })

    # ✅ Cache the result for 3 minutes
    redis_client.setex(cache_key, 180, json.dumps(result))

    return jsonify(result), 200
