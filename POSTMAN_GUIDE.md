# วิธีทดสอบ Register Seller ใน Postman

## ขั้นตอน 1: Import Collection
1. เปิด Postman
2. คลิก "Import" 
3. เลือกไฟล์ `Register_Seller_Postman.json`
4. คลิก "Import"

## ขั้นตอน 2: ตั้งค่า Environment
1. ให้แน่ใจว่า Environment ไฟล์ `Register_Seller_Postman.json` มีตัวแปร:
   - `token` - JWT token จากการ login
   - `user_id` - user ID จากการ login

## ขั้นตอน 3: ทดสอบ API

### 3.1 Login (ขั้นแรก)
```
POST http://localhost:5000/api/login
Content-Type: application/json

{
  "username": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD"
}
```

**Response (สำเร็จ):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": "507f1f77bcf86cd799439011",
  "username": "testuser",
  "role": "user",
  "is_seller": false,
  "is_admin": false
}
```

**คัดลอก token นี้**

---

### 3.2 Register as Seller
```
POST http://localhost:5000/api/auth/register/seller
Content-Type: application/json
Authorization: Bearer YOUR_JWT_TOKEN

{
  "email": "seller@example.com",
  "business_name": "My Shop",
  "contact_info": "123 Main St, City, Country",
  "phonenumber": "0812345678"
}
```

**Response (สำเร็จ - Status 201):**
```json
{
  "message": "Seller registered successfully"
}
```

---

### 3.3 ตัวอย่าง Error Response

**Error 401 - Token invalid:**
```json
{
  "message": "ผู้ใช้ไม่ถูกต้อง หรือ token หมดอายุ"
}
```

**Error 400 - Missing field:**
```json
{
  "message": "Missing field: email"
}
```

**Error 400 - Already registered:**
```json
{
  "message": "User is already registered as a seller"
}
```

**Error 400 - Email already used:**
```json
{
  "message": "Email already registered for a seller"
}
```

---

## ขั้นตอน 4: ดีบัก

### ถ้า Error ให้ตรวจสอบ:
1. ✅ Token มีค่าและไม่หมดอายุ
2. ✅ Headers มี `Authorization: Bearer TOKEN`
3. ✅ Content-Type เป็น `application/json`
4. ✅ Email ไม่ซ้ำกับ seller อื่น
5. ✅ Server Flask กำลังทำงาน (port 5000)
6. ✅ MongoDB เชื่อมต่อได้

### ดูบน Console Backend:
```
Register seller error: ...
```

---

## วิธีใช้ .rest file (VS Code)

ถ้าใช้ VS Code ให้:
1. ติดตั้ง Extension "REST Client"
2. เปิดไฟล์ `test_register_seller.rest`
3. เปลี่ยน `YOUR_JWT_TOKEN_HERE` เป็น token จากการ login
4. คลิก "Send Request" บนแต่ละ endpoint
