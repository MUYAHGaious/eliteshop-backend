import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.product import Product, Order, OrderItem, CartItem
from src.models.admin import Admin
from src.routes.user import user_bp
from src.routes.products import products_bp
from src.routes.cart import cart_bp
from src.routes.orders import orders_bp
from src.routes.admin import admin_bp
from src.routes.auth import auth_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///src/database/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for all routes with credentials support
CORS(app, supports_credentials=True)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(products_bp, url_prefix='/api')
app.register_blueprint(cart_bp, url_prefix='/api')
app.register_blueprint(orders_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

# Create tables and seed data
with app.app_context():
    db.create_all()
    
    # Create default admin if none exists
    if Admin.query.count() == 0:
        default_admin = Admin(
            username='admin',
            email='admin@eliteshop.com'
        )
        default_admin.set_password('admin123')  # Change this in production
        db.session.add(default_admin)
        db.session.commit()
        print("Default admin created: username='admin', password='admin123'")
    
    # Seed products if none exist
    if Product.query.count() == 0:
        from src.seed_data import seed_database
        seed_database()

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')

