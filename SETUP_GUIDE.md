# การตั้งค่าและแก้ไข MyCars Project

## ✅ ปัญหาที่แก้ไขแล้ว

1. ✅ **MongoDB Connection Error** - แก้ไข `app.py` ให้ใช้ `.get()` เพื่อหลีกเลี่ยง KeyError
2. ✅ **Duplicate Key Error (E11000)** - แก้ไข User model ให้ email เป็น optional
3. ✅ **JWT Token** - เปลี่ยนจาก simple token เป็น proper JWT token
4. ✅ **Model References** - แก้ไข Seller ให้ใช้ ReferenceField ที่ถูกต้อง
5. ✅ **Frontend fetch** - แก้ไข Register.vue ให้ใช้ fetch API

## 🚀 ขั้นตอนการตั้งค่า

### 1. Cleanup Database (ครั้งแรกเท่านั้น)
```bash
cd e:\ProjectFainal\backend
python cleanup_db.py
```

### 2. Install Dependencies
```bash
# Backend
cd e:\ProjectFainal\backend
pip install -r requirements.txt

# Frontend (หากยังไม่ได้ติดตั้ง)
cd e:\ProjectFainal\frontend
npm install
```

### 3. Run Backend
```bash
cd e:\ProjectFainal\backend
python app.py
```
ควร output:
```
✓ MongoDB connected successfully
 * Running on http://127.0.0.1:5000
```

### 4. Run Frontend (ใน terminal อื่น)
```bash
cd e:\ProjectFainal\frontend
npm run dev
```

## 📝 ทำการทดสอบ

### Register (สมัครสมาชิก)
1. ไปที่ `http://localhost:3000/register`
2. ใส่ username และ password
3. ควรสำเร็จและ redirect ไปที่ login page

### Login
1. ไปที่ `http://localhost:3000/login`
2. ใส่ username และ password ที่สมัครไว้
3. ควร login สำเร็จและเก็บ token ใน localStorage

## 🔧 ไฟล์ที่แก้ไข

### Backend
- ✅ `config.py` - MONGODB_SETTINGS ถูกต้องแล้ว
- ✅ `app.py` - MongoDB connection error fixed
- ✅ `models/user.py` - Email field เป็น optional
- ✅ `models/seller.py` - ใช้ ReferenceField ที่ถูกต้อง
- ✅ `models/car.py` - ถูกต้องแล้ว
- ✅ `routes/auth.py` - ใช้ JWT token แทน simple token
- ✅ `models/__init__.py` - Import models ที่ถูกต้อง

### Frontend
- ✅ `pages/Register.vue` - ใช้ fetch API แทน axios
- ✅ `pages/login.vue` - ถูกต้องแล้ว

## ⚠️ หมายเหตุ

- หากยังมี error หลังจากทำตามขั้นตอน ให้ลบ `e:\ProjectFainal\backend\__pycache__` folder
- Restart browser และ clear localStorage หากยังมี token เก่า
- ตรวจสอบว่า MongoDB กำลัง running

## 📞 ติดต่อหากมีปัญหา

หากยังมี error อื่นๆ กรุณาแชร์ error message ครับ
