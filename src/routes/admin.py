from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.product import Product, Order, OrderItem
from src.routes.auth import admin_required
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/products', methods=['GET'])
@admin_required
def get_admin_products():
    """Get all products for admin"""
    try:
        products = Product.query.all()
        return jsonify({
            'products': [{
                'id': p.id,
                'name': p.name,
                'description': p.description,
                'price': float(p.price),
                'category': p.category,
                'stock_quantity': p.stock_quantity,
                'image_url': p.image_url,
                'created_at': p.created_at.isoformat() if p.created_at else None
            } for p in products]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/products', methods=['POST'])
@admin_required
def create_admin_product():
    """Create a new product"""
    try:
        data = request.get_json()
        
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            category=data.get('category', ''),
            stock_quantity=data.get('stock_quantity', 0),
            image_url=data.get('image_url', ''),
            created_at=datetime.utcnow()
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'category': product.category,
                'stock_quantity': product.stock_quantity,
                'image_url': product.image_url
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/products/<int:product_id>', methods=['PUT'])
@admin_required
def update_admin_product(product_id):
    """Update a product"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.category = data.get('category', product.category)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        product.image_url = data.get('image_url', product.image_url)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'category': product.category,
                'stock_quantity': product.stock_quantity,
                'image_url': product.image_url
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_admin_product(product_id):
    """Delete a product"""
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/orders', methods=['GET'])
@admin_required
def get_admin_orders():
    """Get all orders for admin"""
    try:
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return jsonify({
            'orders': [{
                'id': o.id,
                'order_number': o.order_number,
                'customer_name': o.customer_name,
                'customer_email': o.customer_email,
                'shipping_address': o.shipping_address,
                'total_amount': float(o.total_amount),
                'status': o.status,
                'created_at': o.created_at.isoformat() if o.created_at else None,
                'items': [{
                    'id': item.id,
                    'product_id': item.product_id,
                    'product': {
                        'name': item.product.name if item.product else 'Unknown Product',
                        'price': float(item.product.price) if item.product else 0
                    },
                    'quantity': item.quantity,
                    'price': float(item.price)
                } for item in o.items]
            } for o in orders]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/orders/stats', methods=['GET'])
@admin_required
def get_order_stats():
    """Get order statistics for admin dashboard"""
    try:
        # Total revenue
        total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
        
        # Total orders
        total_orders = Order.query.count()
        
        # Recent orders (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_orders_30_days = Order.query.filter(Order.created_at >= thirty_days_ago).count()
        
        return jsonify({
            'total_revenue': float(total_revenue),
            'total_orders': total_orders,
            'recent_orders_30_days': recent_orders_30_days
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/orders/<int:order_id>', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        order.status = data.get('status', order.status)
        db.session.commit()
        
        return jsonify({
            'message': 'Order status updated successfully',
            'order': {
                'id': order.id,
                'order_number': order.order_number,
                'status': order.status
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

