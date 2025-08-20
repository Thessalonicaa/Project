from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime, timedelta

def get_thai_time():
    return datetime.utcnow() + timedelta(hours=7)  # ปรับจาก UTC เป็น UTC+7

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

class Note(Document):
    title = StringField(required=True)
    content = StringField()  # สามารถใช้แสดงอะไรเพิ่มเติมได้ เช่น หมายเหตุ
    created_at = DateTimeField(default=get_thai_time)  # เวลาเข้า
    checkout = DateTimeField()                         # ✅ เวลาออก
    user = ReferenceField(User)