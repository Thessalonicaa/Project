// filepath: e:\ProjectFainal\TROUBLESHOOT.md
# Backend Troubleshooting Guide

## Common Import Errors

### Error 1: `cannot import name 'cars_bp'`
**Cause:** `cars_bp` is not defined in `cars.py`

**Solution:** Add this to the top of `routes/cars.py`:
```python
from flask import Blueprint
cars_bp = Blueprint('cars', __name__)
```

### Error 2: `No module named 'config.db'`
**Cause:** Trying to import from config as a package, but it's a module file

**Solution:** Use direct database import:
```python
# Instead of: from config.db import db
# Use either:
from db_init import db
# or
from database import db
```

### Error 3: `cannot import name 'auth'`
**Cause:** `auth_bp` is not defined in `auth.py`

**Solution:** Add this to the top of `routes/auth.py`:
```python
from flask import Blueprint
auth_bp = Blueprint('auth', __name__)
```

## Setup Steps

### 1. Directory Structure Check
```
backend/
├── app.py              ✓ Main Flask app
├── db_init.py          ✓ Database initialization (if using)
├── database.py         ✓ Existing database setup
├── config.py           ✓ Configuration file
├── routes/
│   ├── __init__.py     ✓ Empty or minimal
│   ├── cars.py         ✓ Has cars_bp defined
│   ├── auth.py         ✓ Has auth_bp defined
│   └── orders.py       ✓ Has orders_bp defined (NEW)
└── models/
    └── car.py          ✓ Car model
```

### 2. Quick Fix - Minimal app.py Structure
```python
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load config
SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key-change-in-production')
app.config['SECRET_KEY'] = SECRET_KEY

# Import blueprints after Flask app is created
try:
    from routes.cars import cars_bp
    from routes.auth import auth_bp
    from routes.orders import orders_bp
    
    app.register_blueprint(cars_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(orders_bp, url_prefix='/api')
except ImportError as e:
    print(f"Warning: Some blueprints could not be loaded: {e}")
    try:
        from routes.cars import cars_bp
        from routes.auth import auth_bp
        app.register_blueprint(cars_bp, url_prefix='/api')
        app.register_blueprint(auth_bp, url_prefix='/api')
    except Exception as e2:
        print(f"Fatal error loading blueprints: {e2}")
        raise

# Health check
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 3. MongoDB Connection Check
```bash
# Check if MongoDB is running
mongod --version

# In another terminal, test connection
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017'); print('Connected!' if client else 'Failed')"
```

### 4. Test Each Blueprint Separately
```bash
# Test cars blueprint only
python -c "from routes.cars import cars_bp; print('cars_bp OK')"

# Test auth blueprint only
python -c "from routes.auth import auth_bp; print('auth_bp OK')"

# Test orders blueprint only
python -c "from routes.orders import orders_bp; print('orders_bp OK')"
```

## Running Backend

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Make sure MongoDB is running
mongod

# 3. Run Flask app
python app.py

# Should see:
# * Running on http://127.0.0.1:5000
# * Debugger is active!
```

## Testing Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Get all cars
curl http://localhost:5000/api/cars

# Get user purchases
curl "http://localhost:5000/api/orders/purchases?username=testuser"
```

## If Still Getting Errors

1. **Delete `__pycache__` folders**
   ```bash
   rm -r __pycache__
   rm -r routes/__pycache__
   rm -r models/__pycache__
   ```

2. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check Python version**
   ```bash
   python --version
   ```

4. **Print imports to debug**
   ```python
   import sys
   print(sys.path)
   print(sys.modules.keys())
   ```
