
# Remove duplicate get_car or get_cars function
# The issue is Flask cannot have two functions with same name
# Make sure only ONE exists, and GET /cars comes BEFORE GET /cars/<id>

# In cars.py, keep ONLY this structure:

# 1. GET /cars (returns all or filtered)
@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    # ... handle both all cars and seller_id filter ...
    pass

# 2. GET /cars/<id> (returns single car)
@cars_bp.route('/cars/<car_id>', methods=['GET'])
def get_car(car_id):
    # ... return single car ...
    pass

# Do NOT have two functions with same name!
# If you see this error, check for:
# - def get_cars() defined twice
# - def get_car() defined twice
