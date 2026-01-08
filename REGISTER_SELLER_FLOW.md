// filepath: e:\ProjectFainal\REGISTER_SELLER_FLOW.md
# Register Seller Flow

## Current Flow ✅

1. **User clicks "Become a Seller"** from profile/dashboard
2. **Fills Register-seller form:**
   - Username (pre-filled from localStorage)
   - Email
   - Shop Name (business_name)
   - Phone Number
   - Address (contact_info)

3. **Clicks "Register as Seller"**
4. **Success Modal appears** with 5-second countdown
5. **Auto-redirects to /login** after 5 seconds
6. **User logs in again** with their credentials
7. **Can now access:**
   - Seller Dashboard (/dashboard) - shows seller stats
   - Post Car (/seller/PostCar) - list cars for sale
   - Profile (/profile) - shows seller info

## Important Notes 📝

- After registration, user MUST log in again (this is normal)
- localStorage clears on logout
- New seller account is created in MongoDB
- All seller info is saved: business_name, email, phonenumber, contact_info

## If Registration Doesn't Work 🔧

**Check Backend Error:**
1. Open DevTools (F12) → Console
2. Check if there's an error message
3. Verify backend is running: `python app.py`
4. Check MongoDB connection

**Common Issues:**
- ❌ Email already exists → use different email
- ❌ Network error → check backend server
- ❌ Missing fields → fill all required fields

## Database Check 🗄️

Check if seller was created:
```python
# In MongoDB
db.seller.find()
# Should show new seller document with:
# - username
# - email
# - business_name
# - phonenumber
# - contact_info
```
