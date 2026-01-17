
# ⚠️ DUPLICATE ROUTE DETECTED IN cars.py
# 
# Error: "View function mapping is overwriting an existing endpoint function: cars.get_car"
#
# This means there are TWO functions with the same name or same route
# 
# SOLUTION:
# 
# 1. Open backend/routes/cars.py
# 2. Search for: def get_car(
# 3. DELETE the SECOND occurrence (keep only one)
# 4. OR search for: @cars_bp.route('/cars/<car_id>'
# 5. Make sure it only appears ONCE
#
# The file should have:
# @cars_bp.route('/cars', methods=['GET'])
# def get_cars():  ← ONE definition
#
# @cars_bp.route('/cars/<car_id>', methods=['GET'])  
# def get_car(car_id):  ← ONE definition (NOT duplicated)
#
# If you see it twice, DELETE the duplicate!
