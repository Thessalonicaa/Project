# ปัญหา: มี function get_car ซ้ำใน cars.py ทำให้ Flask บ่น
# 
# วิธีแก้: 
# 1. เปิด backend/routes/cars.py
# 2. หา line ที่มี: def get_car(car_id):
# 3. ลบ block นี้ออกทั้งหมด (หลังจาก return jsonify({'error': str(e)}), 500 ตัวแรก):
#
# ❌ DELETE THIS (DUPLICATE):
# ```
# #  GET SINGLE CAR BY ID
# @cars_bp.route('/cars/<car_id>', methods=['GET'])
# def get_car(car_id):
#     """Get single car by ID"""
#     try:
#         from models.car import Car
#         car = Car.objects(id=car_id).first()
#         ...
#         return jsonify({'error': str(e)}), 500
# ```
#
# ✅ KEEP ONLY THIS (ONE TIME):
# ```
# @cars_bp.route('/cars/<car_id>', methods=['GET'])
# def get_car(car_id):
#     ...
# ```
#
# หลังลบแล้ว restart:
# python app.py
