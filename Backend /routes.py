from flask import Flask, request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from models import User  # Ensure models.py contains your User model



routes_bp = Blueprint('routes', __name__)

# Create a new user
@routes_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Get all users
@routes_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{ "id": user.id, "username": user.username, "email": user.email } for user in users])

# Get a single user by ID
@routes_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({ "id": user.id, "username": user.username, "email": user.email })

# Update a user
@routes_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# Delete a user
@routes_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# if __name__ == '__main__':
#     app.run(debug=True)