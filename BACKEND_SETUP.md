// filepath: e:\ProjectFainal\BACKEND_SETUP.md
# Backend Setup Guide - Sold Out Feature

## Database Schema Updates

### Cars Collection
Add `sold_out` field to existing cars:
```javascript
{
  _id: ObjectId,
  brand: String,
  model: String,
  year: Number,
  price: Number,
  description: String,
  license_plate: String,
  images: [String],
  seller_username: String,
  business_name: String,
  sold_out: Boolean (default: false),  // NEW FIELD
  created_at: Date
}
```

### Orders Collection (NEW)
Track all purchases and sales:
```javascript
{
  _id: ObjectId,
  car_id: ObjectId,
  buyer_username: String,
  seller_username: String,
  car: {
    brand: String,
    model: String,
    year: Number,
    price: Number,
    images: [String],
    license_plate: String
  },
  seller: {
    username: String,
    business_name: String,
    email: String,
    phonenumber: String
  },
  buyer: {
    username: String
  },
  purchase_date: Date,
  sale_date: Date,
  status: String (completed/pending/cancelled),
  amount: Number
}
```

## API Endpoints

### 1. Update Car Sold Status
**Endpoint:** `PATCH /api/cars/{car_id}/sold`
**Headers:** `Authorization: Bearer {token}`
**Body:**
```json
{
  "sold_out": true
}
```
**Response:**
```json
{
  "success": true,
  "message": "Car status updated successfully",
  "sold_out": true
}
```

### 2. Delete Car Listing
**Endpoint:** `DELETE /api/cars/{car_id}`
**Headers:** `Authorization: Bearer {token}`
**Response:**
```json
{
  "success": true,
  "message": "Car deleted successfully"
}
```

### 3. Get User Purchases
**Endpoint:** `GET /api/orders/purchases?username={username}`
**Response:**
```json
{
  "success": true,
  "orders": [
    {
      "_id": "...",
      "car": { brand, model, year, price, images, license_plate },
      "seller": { username, business_name },
      "purchase_date": "2025-01-01",
      "status": "completed"
    }
  ]
}
```

### 4. Get Seller Sales
**Endpoint:** `GET /api/orders/sales?username={username}`
**Response:**
```json
{
  "success": true,
  "orders": [
    {
      "_id": "...",
      "car": { brand, model, year, price, images, license_plate },
      "buyer": { username },
      "sale_date": "2025-01-01",
      "amount": 999999,
      "status": "completed"
    }
  ]
}
```

### 5. Create Order (When Car is Sold)
**Endpoint:** `POST /api/orders`
**Headers:** `Authorization: Bearer {token}`
**Body:**
```json
{
  "car_id": "...",
  "seller_username": "..."
}
```
**Response:**
```json
{
  "success": true,
  "message": "Order created successfully",
  "order_id": "..."
}
```

## Backend Files Created/Updated

✅ `routes/cars.py` - Added PATCH endpoint for sold status
✅ `routes/orders.py` - NEW: Orders endpoints
✅ `models/car.py` - Updated Car model with sold_out field
✅ `app.py` - Registered orders blueprint

## MongoDB Migration

Run this to add sold_out field to existing cars:
```javascript
db.cars.updateMany(
  { sold_out: { $exists: false } },
  { $set: { sold_out: false } }
)

// Create orders collection
db.createCollection("orders")

// Create indexes for better performance
db.orders.createIndex({ buyer_username: 1 })
db.orders.createIndex({ seller_username: 1 })
db.orders.createIndex({ purchase_date: -1 })
```

## Auto-Delete Feature

Frontend handles auto-delete after 3 minutes:
1. User marks car as "Sold"
2. Car shows SOLD OUT with stripe overlay
3. After 3 minutes, frontend sends DELETE request
4. Backend verifies seller ownership and deletes
5. Car removed from listings

## Testing Checklist

- [ ] Mark car as Sold → status changes to SOLD OUT
- [ ] Sold car shows diagonal red stripe
- [ ] Price shows as strikethrough
- [ ] Button changes to "Active"
- [ ] Click Active → reverts to Active status
- [ ] Wait 3 minutes → car auto-deletes
- [ ] Purchase creates order record
- [ ] Orders page shows purchase history
- [ ] Sales page shows sale history (seller only)
- [ ] Profile links work from orders page
