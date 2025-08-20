# ✅ ใช้เฉพาะ Flask เท่านั้น
from flask import Blueprint, request, jsonify
from models import Attendance
from database import get_db
from datetime import datetime

attendance = Blueprint('attendance', __name__)

@attendance.route('/attendance', methods=['GET'])
def get_attendance():
    db = next(get_db())  # ใช้ next เพราะ get_db เป็น generator
    records = db.query(Attendance).order_by(Attendance.timestamp.desc()).all()
    result = []
    for r in records:
        result.append({
            "id": r.id,
            "name": r.name,
            "type": r.type,
            "timestamp": r.timestamp.isoformat()
        })
    return jsonify(result)


@attendance.route('/attendance', methods=['POST'])
def mark_attendance():
    db = next(get_db())
    data = request.get_json()
    name = data.get('name')
    at_type = data.get('type')

    if not name or at_type not in ['in', 'out']:
        return jsonify({'msg': 'Invalid data'}), 400

    new_entry = Attendance(name=name, type=at_type, timestamp=datetime.now())
    db.add(new_entry)
    db.commit()
    return jsonify({
        "id": new_entry.id,
        "name": new_entry.name,
        "type": new_entry.type,
        "timestamp": new_entry.timestamp.isoformat()
    })
