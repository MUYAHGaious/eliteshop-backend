from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.product import Product
from sqlalchemy import or_

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering and pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category = request.args.get('category')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Build query
        query = Product.query.filter_by(is_active=True)
        
        # Apply filters
        if category:
            query = query.filter(Product.category == category)
        
        if search:
            query = query.filter(
                or_(
                    Product.name.contains(search),
                    Product.description.contains(search)
                )
            )
        
        # Apply sorting
        if sort_by == 'price':
            if sort_order == 'asc':
                query = query.order_by(Product.price.asc())
            else:
                query = query.order_by(Product.price.desc())
        elif sort_by == 'name':
            if sort_order == 'asc':
                query = query.order_by(Product.name.asc())
            else:
                query = query.order_by(Product.name.desc())
        else:  # created_at
            if sort_order == 'asc':
                query = query.order_by(Product.created_at.asc())
            else:
                query = query.order_by(Product.created_at.desc())
        
        # Paginate
        products = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page,
            'per_page': per_page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    try:
        product = Product.query.get_or_404(product_id)
        if not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/products/categories', methods=['GET'])
def get_categories():
    """Get all unique product categories"""
    try:
        categories = db.session.query(Product.category).filter(
            Product.is_active == True,
            Product.category.isnot(None)
        ).distinct().all()
        
        category_list = [cat[0] for cat in categories if cat[0]]
        return jsonify({'categories': category_list})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin routes for product management
@products_bp.route('/admin/products', methods=['POST'])
def create_product():
    """Create a new product (Admin only)"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('price'):
            return jsonify({'error': 'Name and price are required'}), 400
        
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            image_url=data.get('image_url', ''),
            category=data.get('category', ''),
            stock_quantity=int(data.get('stock_quantity', 0))
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify(product.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/admin/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product (Admin only)"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = float(data['price'])
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'category' in data:
            product.category = data['category']
        if 'stock_quantity' in data:
            product.stock_quantity = int(data['stock_quantity'])
        if 'is_active' in data:
            product.is_active = bool(data['is_active'])
        
        db.session.commit()
        return jsonify(product.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/admin/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product (Admin only)"""
    try:
        product = Product.query.get_or_404(product_id)
        product.is_active = False  # Soft delete
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/admin/products', methods=['GET'])
def get_all_products_admin():
    """Get all products including inactive ones (Admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        products = Product.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'products': [product.to_dict() for product in products.items],
            'total': products.total,
            'pages': products.pages,
            'current_page': page,
            'per_page': per_page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

