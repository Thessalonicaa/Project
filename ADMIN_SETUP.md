# วิธีสร้าง Admin User ผ่าน Postman

## 🔧 ตัวเลือกที่ 1: สร้าง Admin ใหม่ (ถ้ายังไม่มี)

### Step 1: เปิด Postman

### Step 2: สร้าง Request ใหม่
- Method: **POST**
- URL: `http://localhost:5000/api/create-admin`
- Headers:
  ```
  Content-Type: application/json
  ```

### Step 3: Body (raw JSON)
```json
{
  "username": "admin",
  "password": "admin123"
}
```

### Step 4: Click Send
ควร response:
```json
{
  "success": true,
  "message": "Admin user created successfully",
  "user_id": "xxx",
  "username": "admin",
  "role": "admin"
}
```

---

## 🔧 ตัวเลือกที่ 2: Upgrade User ที่มีอยู่เป็น Admin

### Step 1: ค้นหา User ID ที่ต้องการ

ถ้ารู้ user_id แล้ว (เช่น `507f1f77bcf86cd799439011`) ไปที่ Step 2 เลย

### Step 2: สร้าง Request
- Method: **POST**
- URL: `http://localhost:5000/api/make-admin/507f1f77bcf86cd799439011`
  (แทน `507f1f77bcf86cd799439011` ด้วย user_id จริง)
- Headers:
  ```
  Content-Type: application/json
  ```
- Body: `{}` (ว่าง)

### Step 3: Click Send
ควร response:
```json
{
  "success": true,
  "message": "User wipa upgraded to admin",
  "user_id": "507f1f77bcf86cd799439011",
  "username": "wipa",
  "role": "admin"
}
```

---

## ✅ ทดสอบการ Login เป็น Admin

### Login ด้วย Admin Account
- Method: **POST**
- URL: `http://localhost:5000/api/login`
- Body:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

ควร response:
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "507f1f77bcf86cd799439011",
  "username": "admin",
  "role": "admin",
  "is_admin": true,
  "is_seller": false
}
```

---

## 🎯 หาก User ID ไม่ทราบ

ใช้ MongoDB Compass หรือ MongoDB Shell:

### MongoDB Shell
```javascript
use MyCarsWed
db.users.find({}, {username: 1, _id: 1})
```

จะได้ผลลัพธ์:
```
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  username: "wipa"
}
```

คัดลอก `_id` มาใช้ในขั้นตอนข้างบน

---

## 📌 สรุป

- ✅ Admin สามารถ login ได้โดยไม่ต้องใส่ password (แต่ยังสามารถใส่ได้)
- ✅ Admin จะ redirect ไปที่ `/admin` หลังจาก login
- ✅ สามารถสร้าง admin ได้หลายคน

