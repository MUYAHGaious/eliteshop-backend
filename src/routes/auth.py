from flask import Blueprint, request, jsonify, session
from src.models.user import db
from src.models.admin import Admin
from functools import wraps
import os

auth_bp = Blueprint('auth', __name__)

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({'error': 'Admin authentication required'}), 401
        
        admin = Admin.query.get(session['admin_id'])
        if not admin or not admin.is_active:
            session.pop('admin_id', None)
            return jsonify({'error': 'Invalid admin session'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/auth/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password) and admin.is_active:
            session['admin_id'] = admin.id
            admin.update_last_login()
            
            return jsonify({
                'message': 'Login successful',
                'admin': admin.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/admin/logout', methods=['POST'])
@admin_required
def admin_logout():
    """Admin logout endpoint"""
    try:
        session.pop('admin_id', None)
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/admin/check', methods=['GET'])
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
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

