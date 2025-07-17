from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    address = data.get('address')
    pincode = data.get('pincode')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 409

    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed, full_name=full_name, address=address, pincode=pincode)
    db.session.add(new_user)
    db.session.commit()

    # 👇 Add this part to generate token & return user info
    access_token = create_access_token(identity=new_user.id)

    return jsonify({
        "access_token": access_token,
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "role": new_user.role
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity={"id": user.id, "role": user.role})

    return jsonify({"access_token": token, "role": user.role}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])

    return jsonify({
        "message": f"Welcome {user.role}",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }), 200
