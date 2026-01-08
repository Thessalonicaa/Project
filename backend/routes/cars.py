from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Seller, Car

# Create blueprint
cars_bp = Blueprint('cars', __name__)

# ✅ POST CAR LISTING
@cars_bp.route('/cars', methods=['POST'])
@jwt_required()
def post_car():
    try:
        identity = get_jwt_identity()
        
        user = User.objects(id=identity).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        seller = Seller.objects(user=user).first()
        if not seller:
            return jsonify({"message": "User is not a seller"}), 403

        data = request.get_json() or {}

        # Validate required fields
        required_fields = ['brand', 'model', 'year', 'price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Create car listing
        car = Car(
            seller=seller,
            brand=data.get('brand'),
            model=data.get('model'),
            year=data.get('year'),
            license_plate=data.get('licensePlate', ''),
            description=data.get('description', ''),
            price=float(data.get('price', 0)),
            images=data.get('images', []),
        )
        car.save()

        return jsonify({
            "success": True,
            "message": "Car posted successfully",
            "car_id": str(car.id)
        }), 201

    except Exception as e:
        print(f"Post car error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ✅ GET ALL CARS
@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    try:
        # Get query parameters for filtering
        brand = request.args.get('brand')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        query = {}
        if brand:
            query['brand'] = brand
        
        cars_list = Car.objects(**query).skip((page - 1) * limit).limit(limit)
        total = Car.objects(**query).count()
        
        return jsonify({
            "success": True,
            "cars": [
                {
                    "id": str(car.id),
                    "brand": car.brand,
                    "model": car.model,
                    "year": car.year,
                    "price": car.price,
                    "images": car.images,
                    "description": car.description
                }
                for car in cars_list
            ],
            "total": total,
            "page": page,
            "limit": limit
        }), 200

    except Exception as e:
        print(f"Get cars error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ✅ GET SELLER'S CARS
@cars_bp.route('/cars/seller/<username>', methods=['GET'])
def get_seller_cars(username):
    try:
        from models import Seller, Car
        
        seller = Seller.objects(username=username).first()
        if not seller:
            return jsonify({"message": "Seller not found"}), 404
        
        cars_list = Car.objects(seller=seller)
        
        return jsonify({
            "success": True,
            "cars": [
                {
                    "id": str(car.id),
                    "brand": car.brand,
                    "model": car.model,
                    "year": car.year,
                    "price": car.price,
                    "images": car.images
                }
                for car in cars_list
            ]
        }), 200

    except Exception as e:
        print(f"Get seller cars error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ✅ GET CAR BY ID
@cars_bp.route('/cars/<car_id>', methods=['GET'])
def get_car(car_id):
    try:
        car = Car.objects(id=car_id).first()
        if not car:
            return jsonify({"message": "Car not found"}), 404
        
        return jsonify({
            "success": True,
            "car": {
                "id": str(car.id),
                "brand": car.brand,
                "model": car.model,
                "year": car.year,
                "price": car.price,
                "license_plate": car.license_plate,
                "description": car.description,
                "images": car.images,
                "seller": {
                    "id": str(car.seller.id),
                    "username": car.seller.username,
                    "business_name": car.seller.business_name,
                    "contact_info": car.seller.contact_info
                }
            }
        }), 200

    except Exception as e:
        print(f"Get car error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ✅ DELETE CAR LISTING
@cars_bp.route('/cars/<car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    """Delete a car listing"""
    try:
        identity = get_jwt_identity()
        
        user = User.objects(id=identity).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        seller = Seller.objects(user=user).first()
        if not seller:
            return jsonify({"message": "User is not a seller"}), 403

        # Find the car
        car = Car.objects(id=car_id, seller=seller).first()
        if not car:
            return jsonify({"message": "Car not found or you are not the seller"}), 404
        
        # Delete the car
        car.delete()
        
        return jsonify({
            "success": True,
            "message": "Car deleted successfully"
        }), 200

    except Exception as e:
        print(f"Delete car error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ✅ PATCH CAR SOLD STATUS
@cars_bp.route('/cars/<car_id>/sold', methods=['PATCH'])
@jwt_required()
def update_car_sold_status(car_id):
    """Mark car as sold or active"""
    try:
        identity = get_jwt_identity()
        
        user = User.objects(id=identity).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        seller = Seller.objects(user=user).first()
        if not seller:
            return jsonify({"message": "User is not a seller"}), 403

        data = request.get_json() or {}
        sold_out = data.get('sold_out', False)

        # Find the car
        car = Car.objects(id=car_id, seller=seller).first()
        if not car:
            return jsonify({"message": "Car not found or you are not the seller"}), 404
        
        # Update the car's sold status
        car.update(sold_out=sold_out)
        
        return jsonify({
            "success": True,
            "message": "Car status updated successfully",
            "sold_out": sold_out
        }), 200

    except Exception as e:
        print(f"Update car sold status error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ✅ SEARCH CARS
@cars_bp.route('/cars/search', methods=['GET'])
def search_cars():
    """Search cars by brand, model, or any field"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 1:
            return jsonify([]), 200
        
        # Search in brand, model, description, or license_plate using Q objects
        from mongoengine import Q
        
        results = Car.objects(
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(description__icontains=query) |
            Q(license_plate__icontains=query)
        ).limit(10)
        
        cars_list = [
            {
                "_id": str(car.id),
                "id": str(car.id),
                "brand": car.brand,
                "model": car.model,
                "year": car.year,
                "price": car.price,
                "images": car.images,
                "description": car.description,
                "license_plate": car.license_plate,
                "seller": {
                    "username": car.seller.username,
                    "business_name": car.seller.business_name
                }
            }
            for car in results
        ]
        
        return jsonify(cars_list), 200
        
    except Exception as e:
        print(f"Error searching cars: {str(e)}")
        return jsonify([]), 200