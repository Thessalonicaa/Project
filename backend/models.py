from mongoengine import Document, StringField, ReferenceField, DateTimeField, BooleanField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default='user')  # 'user' หรือ 'seller'
    is_seller = BooleanField(default=False)  # เพิ่มฟิลด์นี้
    meta = {'collection': 'users'}
    
class Seller(Document):
    user = ReferenceField('User')
    username = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    business_name = StringField()
    contact_info = StringField()
    phonenumber = StringField()
    role = StringField(default='seller')
    created_at = DateTimeField()
    meta = {'collection': 'sellers'}

class Note(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    user = ReferenceField(User, required=True)
    checkout = DateTimeField()
    meta = {'collection': 'notes'}