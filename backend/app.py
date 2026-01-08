from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

try:
    from routes.cars import cars_bp
    from routes.auth import auth_bp
    from routes.orders import orders_bp
    from routes.messages import messages_bp  # Import messages blueprint
    HAS_ORDERS = True
except ImportError as e:
    print(f"Warning: Could not import all blueprints: {e}")
    try:
        from routes.cars import cars_bp
        from routes.auth import auth_bp
        from routes.messages import messages_bp  # Import messages blueprint
        HAS_ORDERS = False
    except ImportError as e2:
        print(f"Error importing core blueprints: {e2}")
        raise

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)  # ✅ รองรับ credential และ preflight

JWTManager(app)

# เชื่อมต่อ MongoDB ด้วย mongoengine โดยตรง
connect(
    db=app.config["MONGODB_SETTINGS"]["db"],
    host=app.config["MONGODB_SETTINGS"]["host"],
    port=app.config["MONGODB_SETTINGS"]["port"]
)

# Register Blueprints
app.register_blueprint(cars_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(messages_bp)  # Register messages blueprint

if HAS_ORDERS:
    app.register_blueprint(orders_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)

