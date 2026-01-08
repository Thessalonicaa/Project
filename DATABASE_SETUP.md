// filepath: e:\ProjectFainal\DATABASE_SETUP.md
# Database Setup Guide - Sold Out Feature

## Step 1: Run Migration Script

**Run this ONCE to add `sold_out` field to existing cars:**

```bash
cd backend
python migrate_sold_out.py
```

**Expected output:**
```
✓ Migration completed!
  Modified documents: 15
  Total cars in database: 15
  Cars without sold_out field: 0
✓ All cars have sold_out field!
```

## Step 2: Verify MongoDB Collections

**Check if collections exist and have data:**

```bash
# Connect to MongoDB
mongo mongodb://localhost:27017/car_sales

# Or using mongosh
mongosh mongodb://localhost:27017/car_sales
```

**Run these commands in MongoDB:**

```javascript
// Check cars collection
db.cars.countDocuments()
// Should return number of cars

// Check if all cars have sold_out field
db.cars.countDocuments({ sold_out: { $exists: true } })
// Should match total cars count

// View a sample car
db.cars.findOne()
// Should show sold_out: true or false

// Check orders collection
db.orders.countDocuments()
// May be 0 initially
```

## Step 3: Create Indexes for Better Performance

**Run these in MongoDB to create indexes:**

```javascript
// Create indexes for faster queries
db.cars.createIndex({ seller_username: 1 })
db.cars.createIndex({ sold_out: 1 })
db.cars.createIndex({ created_at: -1 })

db.orders.createIndex({ buyer_username: 1 })
db.orders.createIndex({ seller_username: 1 })
db.orders.createIndex({ purchase_date: -1 })

// View created indexes
db.cars.getIndexes()
db.orders.getIndexes()
```

## Step 4: Troubleshooting

### Issue: "Cannot resolve field sold_out"

**Solution 1: Run migration**
```bash
python migrate_sold_out.py
```

**Solution 2: Manual MongoDB fix**
```javascript
// Add sold_out field to ALL cars
db.cars.updateMany(
  { sold_out: { $exists: false } },
  { $set: { sold_out: false } }
)
```

**Solution 3: Delete and recreate cars**
```javascript
// If above doesn't work, delete all cars and re-upload
db.cars.deleteMany({})

// Then re-upload cars from UI
```

### Issue: MongoDB Connection Failed

```bash
# Make sure MongoDB is running
mongod

# Or check if service is running
# Windows: services.msc -> MongoDB Server
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

### Issue: No cars showing after migration

```javascript
// Check if cars collection exists
show collections

// If empty, check cars collection name
db.getCollectionNames()

// If collection has different name, verify in app.py
```

## Collections Schema

### Cars Collection
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
  sold_out: Boolean,        // NEW FIELD
  email: String,
  phonenumber: String,
  contact_info: String,
  created_at: Date
}
```

### Orders Collection
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
  status: String,
  amount: Number
}
```

## Testing After Setup

1. **Mark car as sold**
   - Go to MyListings page
   - Click "Sold" button on any car
   - Should show "SOLD OUT" with stripe

2. **Check database**
   ```javascript
   db.cars.findOne({ sold_out: true })
   // Should show the car you just marked as sold
   ```

3. **Verify auto-delete (after 3 minutes)**
   - Mark a car as sold
   - Wait 3 minutes
   - Car should disappear from listings
   - Check database: `db.cars.count()` should decrease

4. **Check orders tracking**
   - Go to Orders page
   - Should show purchase/sales history
   - Click seller/buyer profile link

## Backup

**Before migration, backup your data:**

```bash
# Export cars collection
mongoexport --uri "mongodb://localhost:27017/car_sales" --collection cars --out cars_backup.json

# Export orders collection
mongoexport --uri "mongodb://localhost:27017/car_sales" --collection orders --out orders_backup.json

# If something goes wrong, restore:
mongoimport --uri "mongodb://localhost:27017/car_sales" --collection cars --file cars_backup.json --drop
```
