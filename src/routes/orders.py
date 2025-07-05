from flask import Blueprint, request, jsonify, session
from src.models.user import db
from src.models.product import Product, CartItem, Order, OrderItem
import uuid
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

def get_session_id():
    """Get session ID for cart management"""
    return session.get('cart_session_id')

def generate_order_number():
    """Generate a unique order number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = str(uuid.uuid4())[:8].upper()
    return f"ORD-{timestamp}-{random_suffix}"

@orders_bp.route('/orders/checkout', methods=['POST'])
def checkout():
    """Process checkout and create an order"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Order data is required'}), 400
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'shipping_address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        session_id = get_session_id()
        if not session_id:
            return jsonify({'error': 'No cart session found'}), 400
        
        # Get cart items
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total and validate stock
        total_amount = 0
        order_items_data = []
        
        for cart_item in cart_items:
            product = cart_item.product
            if not product or not product.is_active:
                return jsonify({'error': f'Product {cart_item.product_id} is no longer available'}), 400
            
            if product.stock_quantity < cart_item.quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
            
            item_total = product.price * cart_item.quantity
            total_amount += item_total
            
            order_items_data.append({
                'product_id': product.id,
                'quantity': cart_item.quantity,
                'price': product.price
            })
        
        # Create order
        order = Order(
            order_number=generate_order_number(),
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            shipping_address=data['shipping_address'],
            total_amount=total_amount,
            status='confirmed'
        )
        
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Create order items and update stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            db.session.add(order_item)
            
            # Update product stock
            product = Product.query.get(item_data['product_id'])
            product.stock_quantity -= item_data['quantity']
        
        # Clear cart
        CartItem.query.filter_by(session_id=session_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order placed successfully',
            'order': order.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<order_number>', methods=['GET'])
def get_order(order_number):
    """Get order details by order number"""
    try:
        order = Order.query.filter_by(order_number=order_number).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify(order.to_dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/email/<email>', methods=['GET'])
def get_orders_by_email(email):
    """Get all orders for a customer email"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        orders = Order.query.filter_by(customer_email=email).order_by(
            Order.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page,
            'per_page': per_page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin routes for order management
@orders_bp.route('/admin/orders', methods=['GET'])
def get_all_orders():
    """Get all orders (Admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = Order.query
        
        if status:
            query = query.filter_by(status=status)
        
        orders = query.order_by(Order.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'orders': [order.to_dict() for order in orders.items],
            'total': orders.total,
            'pages': orders.pages,
            'current_page': page,
            'per_page': per_page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/admin/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status (Admin only)"""
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'error': 'Invalid status'}), 400
        
        order = Order.query.get_or_404(order_id)
        order.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order status updated successfully',
            'order': order.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/admin/orders/stats', methods=['GET'])
def get_order_stats():
    """Get order statistics (Admin only)"""
    try:
        total_orders = Order.query.count()
        total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
        
        # Orders by status
        status_counts = db.session.query(
            Order.status,
            db.func.count(Order.id)
        ).group_by(Order.status).all()
        
        status_stats = {status: count for status, count in status_counts}
        
        # Recent orders (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_orders = Order.query.filter(Order.created_at >= thirty_days_ago).count()
        
        return jsonify({
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'status_breakdown': status_stats,
            'recent_orders_30_days': recent_orders
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

