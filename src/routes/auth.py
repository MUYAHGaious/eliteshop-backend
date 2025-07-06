from flask import Blueprint, request, jsonify, session
from src.models.user import db
from src.models.admin import Admin
from datetime import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        
        admin = Admin.query.get(session['admin_id'])
        if not admin or not admin.is_active:
            session.pop('admin_id', None)
            return jsonify({'error': 'Invalid or inactive admin'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password) and admin.is_active:
            session['admin_id'] = admin.id
            admin.update_last_login()
            
            return jsonify({
                'message': 'Login successful',
                'admin': admin.to_dict()
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/admin/logout', methods=['POST'])
@admin_required
def admin_logout():
    """Admin logout endpoint"""
    try:
        session.pop('admin_id', None)
        return jsonify({'message': 'Logout successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/admin/check-auth', methods=['GET'])
def check_admin_auth():
    """Check if admin is authenticated"""
    try:
        if 'admin_id' not in session:
            return jsonify({'authenticated': False}), 200
        
        admin = Admin.query.get(session['admin_id'])
        if not admin or not admin.is_active:
            session.pop('admin_id', None)
            return jsonify({'authenticated': False}), 200
        
        return jsonify({
            'authenticated': True,
            'admin': admin.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/admin/create-default', methods=['POST'])
def create_default_admin():
    """Create default admin (for development/setup)"""
    try:
        # Check if any admin exists
        if Admin.query.count() > 0:
            return jsonify({'error': 'Admin already exists'}), 400
        
        # Create default admin
        admin = Admin(
            username='admin',
            email='admin@eliteshop.com'
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'message': 'Default admin created successfully',
            'credentials': {
                'username': 'admin',
                'password': 'admin123'
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

