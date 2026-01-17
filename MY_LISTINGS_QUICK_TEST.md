# 🧪 My Listings - Quick Test

## Prerequisites

- Backend running: `python app.py` (port 5000)
- Frontend running: `npm run dev` (port 3000)
- User registered and logged in as seller
- At least one car posted

## 5-Minute Test

### Step 1: Login as Seller

```
Go to http://localhost:3000/dashboard
Username: testseller
Password: test123456
```

Should see:
- Account type: "Seller Dashboard"
- Your username displayed
- 3 stat cards (Cars Listed, Orders, Revenue)

### Step 2: Post a Car (if not already posted)

```
1. Click "Post Car" button
2. Fill form:
   - Brand: Toyota
   - Model: Camry
   - Year: 2022
   - Price: 850000
   - Fuel: Petrol
   - Transmission: Automatic
   - Type: Sedan
3. Click "Post Car"
4. Should see success message
```

### Step 3: Check My Listings

```
1. Click "List" button next to "Post Car"
2. Should navigate to /seller/MyListings
3. Should see car(s) you posted
```

### Step 4: Open DevTools (F12)

#### Console Tab:

Watch for logs:
```javascript
Dashboard - Username: testseller
Dashboard - Is Seller: true
Fetching cars for seller: testseller
Seller info response: {success: true, seller: {...}}
Cars response: {success: true, cars: [...]}
Cars loaded: 1
```

#### Network Tab:

Look for requests:
```
GET /api/seller-info/testseller
  Status: 200 ✅
  Response: {seller info}

GET /api/cars?seller_id=507f...
  Status: 200 ✅
  Response: {cars: [...]}
```

### Step 5: Verify MongoDB

```bash
# Terminal
mongo
> use zavora

# Check seller exists
> db.sellers.findOne({username: "testseller"})
# Should return seller document

# Check cars posted
> db.cars.find({seller: ObjectId("...")})
# Should return car document(s)
```

## Success Indicators ✅

All of these must be true:

- [ ] Dashboard loads without errors
- [ ] Is Seller: true shown in console
- [ ] Console shows "Seller info response: {success: true}"
- [ ] Console shows "Cars response: {success: true}"
- [ ] Console shows "Cars loaded: 1" (or more)
- [ ] My Listings section shows car card(s)
- [ ] Car shows brand, model, year
- [ ] Car image displayed
- [ ] Network tab shows 200 responses
- [ ] No 404 errors in console

## Troubleshooting

### Issue: "No cars listed yet" appears

**Check:**
1. Did you actually post a car?
   ```bash
   mongo
   > db.cars.count()
   # Should be > 0
   ```

2. Is car linked to seller?
   ```bash
   > db.cars.findOne({})
   # Should have seller field with ObjectId
   ```

3. Does seller match?
   ```bash
   > db.sellers.findOne({username: "testseller"})
   # Get ID and check it matches car's seller field
   ```

### Issue: Network error "Cannot GET /api/cars/seller"

**Cause:** Old endpoint being used
**Fix:** 
- Clear browser cache (Ctrl+Shift+R)
- Check dashboard.vue is updated
- Restart frontend

### Issue: 404 on /api/cars endpoint

**Cause:** Endpoint not in cars.py
**Fix:**
- Check cars.py has the GET /api/cars endpoint
- Restart backend

### Issue: "Cars response: {success: false}"

**Check:**
1. Seller ID is valid
   ```bash
   mongo
   > db.sellers.findOne({username: "testseller"})
   # Copy the _id
   ```

2. Cars exist for seller
   ```bash
   > db.cars.findOne({seller: ObjectId("...")})
   # Should return a car
   ```

3. Check backend logs for errors

## API Testing with Curl

```bash
# Get seller info
curl http://localhost:5000/api/seller-info/testseller

# Sample response:
# {
#   "success": true,
#   "seller": {
#     "id": "507f1f77bcf86cd799439011",
#     "username": "testseller",
#     ...
#   }
# }

# Get cars by seller_id
curl "http://localhost:5000/api/cars?seller_id=507f1f77bcf86cd799439011"

# Sample response:
# {
#   "success": true,
#   "cars": [
#     {
#       "_id": "...",
#       "brand": "Toyota",
#       "model": "Camry",
#       "year": 2022,
#       ...
#     }
#   ],
#   "total": 1
# }
```

## Expected Timeline

```
0:00 - Dashboard loads
0:01 - Checks if user is seller
0:02 - Fetches seller info
0:03 - Gets seller ID
0:04 - Fetches cars using seller_id
0:05 - Populates My Listings section
0:06 - ✅ Cars display!
```

## Files to Review

- [MY_LISTINGS_FIX.md](./MY_LISTINGS_FIX.md) - Complete fix guide
- dashboard.vue - Frontend changes
- cars.py - Backend endpoint

---

**If all success indicators are true, "My Listings" is working!** 🎉