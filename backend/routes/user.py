from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.parking_lot import ParkingLot
from models.parking_spot import ParkingSpot
from models.reservation import Reservation
from models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/reserve', methods=['POST'])
@jwt_required()
def reserve_spot():
    data = request.json
    identity = get_jwt_identity()
    user_id = identity['id']
    lot_id = data.get('lot_id')

    existing = Reservation.query.filter_by(user_id=user_id).first()
    if existing:
        return jsonify({"message": "You already have a reservation"}), 400

    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not available_spot:
        return jsonify({"message": "No spots available"}), 404

    available_spot.status = 'O'
    reservation = Reservation(user_id=user_id, spot_id=available_spot.id)
    db.session.add(reservation)
    db.session.commit()

    return jsonify({"message": "Spot reserved", "spot_id": available_spot.id}), 201

@user_bp.route('/reservation', methods=['GET'])
@jwt_required()
def view_reservation():
    identity = get_jwt_identity()
    user_id = identity['id']
    reservation = Reservation.query.filter_by(user_id=user_id).first()

    if not reservation:
        return jsonify({"message": "No reservation found"}), 404

    return jsonify({
        "spot_id": reservation.spot.id,
        "lot_id": reservation.spot.lot.id,
        "lot_name": reservation.spot.lot.name,
        "status": reservation.spot.status
    })

@user_bp.route('/reservation', methods=['DELETE'])
@jwt_required()
def cancel_reservation():
    identity = get_jwt_identity()
    user_id = identity['id']
    reservation = Reservation.query.filter_by(user_id=user_id).first()

    if not reservation:
        return jsonify({"message": "No active reservation"}), 404

    reservation.spot.status = 'A'
    db.session.delete(reservation)
    db.session.commit()

    return jsonify({"message": "Reservation cancelled"}), 200
