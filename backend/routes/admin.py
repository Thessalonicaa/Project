from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models import User, Seller

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# GET ALL USERS
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        identity = get_jwt_identity()
        user = User.objects(id=identity).first()
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        users = User.objects()
        users_data = []
        
        for u in users:
            user_data = {
                '_id': str(u.id),
                'username': u.username,
                'role': u.role,
                'created_at': str(u.created_at) if hasattr(u, 'created_at') else None
            }
            users_data.append(user_data)
        
        return jsonify({'success': True, 'users': users_data}), 200
    except Exception as e:
        print(f'Get all users error: {str(e)}')
        return jsonify({'error': str(e)}), 500


# UPDATE USER (PUT)
@admin_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        identity = get_jwt_identity()
        admin = User.objects(id=identity).first()
        
        if not admin or admin.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json() or {}
        
        # Update role
        if 'role' in data:
            old_role = user.role
            user.role = data['role']
            # Update is_seller flag based on role
            user.is_seller = (data['role'] == 'seller')
            
            # If changing from seller to non-seller, delete seller record
            if old_role == 'seller' and data['role'] != 'seller':
                seller = Seller.objects(user=user).first()
                if seller:
                    seller.delete()
        
        user.save()
        
        # Handle seller-specific updates
        if data.get('role') == 'seller':
            seller = Seller.objects(user=user).first()
            
            if seller:
                # Update existing seller
                if 'email' in data:
                    seller.email = data['email']
                if 'business_name' in data:
                    seller.business_name = data['business_name']
                if 'phonenumber' in data:
                    seller.phonenumber = data['phonenumber']
                if 'address' in data:
                    seller.address = data['address']
                seller.save()
            else:
                # Create new seller if doesn't exist
                if 'email' in data and 'business_name' in data:
                    new_seller = Seller(
                        user=user,
                        username=user.username,
                        email=data.get('email'),
                        password=user.password,
                        business_name=data.get('business_name'),
                        phonenumber=data.get('phonenumber', ''),
                        contact_info=data.get('address', '')
                    )
                    new_seller.save()
        
        return jsonify({'success': True, 'message': 'User updated successfully'}), 200
    except Exception as e:
        print(f'Update user error: {str(e)}')
        return jsonify({'error': str(e)}), 500


# DELETE USER (DELETE)
@admin_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        identity = get_jwt_identity()
        admin = User.objects(id=identity).first()
        
        if not admin or admin.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete related seller if exists
        seller = Seller.objects(user=user).first()
        if seller:
            seller.delete()
        
        # Delete user
        user.delete()
        
        return jsonify({'success': True, 'message': 'User deleted successfully'}), 200
    except Exception as e:
        print(f'Delete user error: {str(e)}')
        return jsonify({'error': str(e)}), 500


# CREATE USER (POST)
@admin_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    try:
        identity = get_jwt_identity()
        admin = User.objects(id=identity).first()
        
        if not admin or admin.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json() or {}
        
        # Validate required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        # Check if username exists
        if User.objects(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        # Create user
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            username=data['username'],
            password=hashed_password,
            role=data.get('role', 'user'),
            is_seller=(data.get('role') == 'seller')
        )
        new_user.save()
        
        # If seller, create seller record
        if data.get('role') == 'seller':
            if not data.get('email') or not data.get('business_name'):
                return jsonify({'error': 'Email and business name required for sellers'}), 400
            
            new_seller = Seller(
                user=new_user,
                username=new_user.username,
                email=data['email'],
                password=hashed_password,
                business_name=data['business_name'],
                phonenumber=data.get('phonenumber', ''),
                contact_info=data.get('address', '')
            )
            new_seller.save()
        
        return jsonify({'success': True, 'message': 'User created successfully', 'user_id': str(new_user.id)}), 201
    except Exception as e:
        print(f'Create user error: {str(e)}')
        return jsonify({'error': str(e)}), 500
