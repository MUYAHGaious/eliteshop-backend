#!/usr/bin/env python3
"""
Script to populate the database with sample products
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.product import Product
from datetime import datetime

def seed_database():
    """Seed the database with sample products"""
    sample_products = [
        {
            'name': 'Backpack',
            'description': 'Durable backpack with laptop compartment and multiple pockets. Perfect for travel and daily use.',
            'price': 59.99,
            'category': 'Accessories',
            'stock_quantity': 50,
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'
        },
        {
            'name': 'Running Shoes',
            'description': 'Lightweight running shoes with advanced cushioning and breathable mesh upper.',
            'price': 129.99,
            'category': 'Sports & Fitness',
            'stock_quantity': 30,
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'
        },
        {
            'name': 'Desk Lamp',
            'description': 'LED desk lamp with adjustable brightness and color temperature. USB charging port included.',
            'price': 49.99,
            'category': 'Home & Garden',
            'stock_quantity': 25,
            'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop'
        },
        {
            'name': 'Smartphone Case',
            'description': 'Protective smartphone case with shock absorption and wireless charging compatibility.',
            'price': 19.99,
            'category': 'Electronics',
            'stock_quantity': 100,
            'image_url': 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=400&h=300&fit=crop'
        },
        {
            'name': 'Yoga Mat',
            'description': 'Non-slip yoga mat made from eco-friendly materials. Perfect for yoga, pilates, and fitness.',
            'price': 39.99,
            'category': 'Sports & Fitness',
            'stock_quantity': 40,
            'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop'
        },
        {
            'name': 'Coffee Maker',
            'description': 'Programmable coffee maker with 12-cup capacity and auto-shutoff feature.',
            'price': 79.99,
            'category': 'Kitchen',
            'stock_quantity': 20,
            'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop'
        },
        {
            'name': 'Leather Laptop Bag',
            'description': 'Professional leather laptop bag with multiple compartments. Fits laptops up to 15 inches.',
            'price': 89.99,
            'category': 'Accessories',
            'stock_quantity': 15,
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'
        },
        {
            'name': 'Stainless Steel Water Bottle',
            'description': 'Insulated stainless steel water bottle that keeps drinks cold for 24 hours or hot for 12 hours.',
            'price': 29.99,
            'category': 'Home & Garden',
            'stock_quantity': 60,
            'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=300&fit=crop'
        },
        {
            'name': 'Organic Cotton T-Shirt',
            'description': 'Comfortable and sustainable organic cotton t-shirt. Available in multiple colors and sizes.',
            'price': 24.99,
            'category': 'Clothing',
            'stock_quantity': 100,
            'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop'
        },
        {
            'name': 'Wireless Bluetooth Headphones',
            'description': 'High-quality wireless headphones with noise cancellation and 30-hour battery life. Perfect for music lovers and professionals.',
            'price': 99.99,
            'category': 'Electronics',
            'stock_quantity': 50,
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop'
        }
    ]

    for product_data in sample_products:
        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            category=product_data['category'],
            stock_quantity=product_data['stock_quantity'],
            image_url=product_data['image_url'],
            created_at=datetime.utcnow()
        )
        db.session.add(product)

    db.session.commit()
    print(f"Successfully added {len(sample_products)} products to the database!")

if __name__ == '__main__':
    from src.main import app
    with app.app_context():
        seed_database()

