from flask import Blueprint, request, jsonify
from models.car import Car
from models.conversation import Conversation
from models.message import Message
from models import User
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Get all users
@admin_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.objects()
        users_list = []
        for u in users:
            users_list.append({
                '_id': str(u.id),
                'username': u.username,
                'email': getattr(u, 'email', None),
                'role': getattr(u, 'role', 'user'),
                'created_at': getattr(u, 'created_at', None)
            })
        return jsonify({'success': True, 'users': users_list}), 200
    except Exception as e:
        print('Error get users', e)
        return jsonify({'success': False, 'message': 'Error fetching users'}), 500

# Update user
@admin_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        u = User.objects(id=user_id).first()
        if not u:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        for k, v in data.items():
            if hasattr(u, k):
                setattr(u, k, v)
        u.save()
        return jsonify({'success': True, 'user': u.to_mongo().to_dict()}), 200
    except Exception as e:
        print('Error update user', e)
        return jsonify({'success': False, 'message': 'Error updating user'}), 500

# Delete user
@admin_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        u = User.objects(id=user_id).first()
        if not u:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        u.delete()
        return jsonify({'success': True, 'message': 'User deleted'}), 200
    except Exception as e:
        print('Error delete user', e)
        return jsonify({'success': False, 'message': 'Error deleting user'}), 500

# Get all cars
@admin_bp.route('/cars', methods=['GET'])
def get_cars():
    try:
        cars = Car.objects()
        cars_list = []
        for c in cars:
            cars_list.append({
                '_id': str(c.id),
                'brand': c.brand,
                'model': c.model,
                'year': c.year,
                'price': c.price,
                'seller': getattr(c, 'seller', None),
                'license_plate': getattr(c, 'license_plate', None),
                'sold_out': getattr(c, 'sold_out', False),
                'created_at': getattr(c, 'created_at', None),
                'description': getattr(c, 'description', '')
            })
        return jsonify({'success': True, 'cars': cars_list}), 200
    except Exception as e:
        print('Error get cars', e)
        return jsonify({'success': False, 'message': 'Error fetching cars'}), 500

# Update car
@admin_bp.route('/cars/<car_id>', methods=['PUT'])
def update_car(car_id):
    try:
        data = request.get_json()
        c = Car.objects(id=car_id).first()
        if not c:
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        for k, v in data.items():
            if hasattr(c, k):
                setattr(c, k, v)
        c.save()
        return jsonify({'success': True, 'car': c.to_mongo().to_dict()}), 200
    except Exception as e:
        print('Error update car', e)
        return jsonify({'success': False, 'message': 'Error updating car'}), 500

# Delete car
@admin_bp.route('/cars/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    try:
        c = Car.objects(id=car_id).first()
        if not c:
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        c.delete()
        return jsonify({'success': True, 'message': 'Car deleted'}), 200
    except Exception as e:
        print('Error delete car', e)
        return jsonify({'success': False, 'message': 'Error deleting car'}), 500
