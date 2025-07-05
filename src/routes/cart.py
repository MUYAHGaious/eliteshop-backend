from flask import Blueprint, request, jsonify, session
from src.models.user import db
from src.models.product import Product, CartItem
import uuid

cart_bp = Blueprint('cart', __name__)

def get_session_id():
    """Get or create a session ID for cart management"""
    if 'cart_session_id' not in session:
        session['cart_session_id'] = str(uuid.uuid4())
    return session['cart_session_id']

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    """Get all items in the current cart"""
    try:
        session_id = get_session_id()
        cart_items = CartItem.query.filter_by(session_id=session_id).all()
        
        total = 0
        items_data = []
        
        for item in cart_items:
            item_data = item.to_dict()
            if item.product:
                subtotal = item.product.price * item.quantity
                item_data['subtotal'] = subtotal
                total += subtotal
            items_data.append(item_data)
        
        return jsonify({
            'items': items_data,
            'total': total,
            'item_count': len(cart_items)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add an item to the cart"""
    try:
        data = request.get_json()
        
        if not data or not data.get('product_id') or not data.get('quantity'):
            return jsonify({'error': 'Product ID and quantity are required'}), 400
        
        product_id = int(data['product_id'])
        quantity = int(data['quantity'])
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        # Check if product exists and is active
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check stock availability
        if product.stock_quantity < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        session_id = get_session_id()
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            session_id=session_id,
            product_id=product_id
        ).first()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            existing_item.quantity = new_quantity
        else:
            # Create new cart item
            cart_item = CartItem(
                session_id=session_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return jsonify({'message': 'Item added to cart successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/update/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    """Update quantity of a cart item"""
    try:
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return jsonify({'error': 'Quantity is required'}), 400
        
        quantity = int(data['quantity'])
        session_id = get_session_id()
        
        cart_item = CartItem.query.filter_by(
            id=item_id,
            session_id=session_id
        ).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            db.session.delete(cart_item)
        else:
            # Check stock availability
            if cart_item.product.stock_quantity < quantity:
                return jsonify({'error': 'Insufficient stock'}), 400
            cart_item.quantity = quantity
        
        db.session.commit()
        return jsonify({'message': 'Cart updated successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/remove/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Remove an item from the cart"""
    try:
        session_id = get_session_id()
        
        cart_item = CartItem.query.filter_by(
            id=item_id,
            session_id=session_id
        ).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Item removed from cart successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/clear', methods=['DELETE'])
def clear_cart():
    """Clear all items from the cart"""
    try:
        session_id = get_session_id()
        
        CartItem.query.filter_by(session_id=session_id).delete()
        db.session.commit()
        
        return jsonify({'message': 'Cart cleared successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/count', methods=['GET'])
def get_cart_count():
    """Get the number of items in the cart"""
    try:
        session_id = get_session_id()
        count = CartItem.query.filter_by(session_id=session_id).count()
        return jsonify({'count': count})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

