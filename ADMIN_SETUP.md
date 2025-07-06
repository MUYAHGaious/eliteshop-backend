# 🔐 Admin Panel Setup Guide

## Overview
This updated version of EliteShop includes a secure admin panel with authentication. Users no longer need to create accounts - the system is designed for guest checkout only.

## Admin Access

### Default Admin Credentials
- **Username:** `admin`
- **Password:** `admin123`

### Admin Login URL
- **Local Development:** `http://localhost:5173/admin/login`
- **Production:** `https://your-domain.com/admin/login`

## Security Features

### 1. Admin Authentication
- Session-based authentication with Flask sessions
- Password hashing using Werkzeug security
- Admin-only access to management endpoints
- Automatic logout on session expiry

### 2. Protected Routes
All admin endpoints require authentication:
- `/api/admin/products` - Product management
- `/api/admin/orders` - Order management
- `/api/admin/orders/stats` - Dashboard statistics

### 3. Frontend Protection
- Admin pages redirect to login if not authenticated
- Authentication state managed with both server sessions and localStorage
- Automatic logout functionality

## Admin Panel Features

### Dashboard
- Total revenue statistics
- Order count and recent orders (30 days)
- Product inventory count
- Interactive charts (sales overview, category distribution)

### Product Management
- Add new products with full details
- Edit existing products
- Delete products with confirmation
- Real-time inventory tracking

### Order Management
- View all customer orders
- Order details with item breakdown
- Order status updates
- Customer information display

## User Experience Changes

### Removed Features
- User registration system
- User login requirements
- User account management

### Guest Checkout
- Customers can shop without creating accounts
- Checkout requires only shipping and contact information
- Order confirmation via email (no account needed)

## Production Security Notes

### Important: Change Default Credentials
Before deploying to production, create a new admin user:

1. Access your production database
2. Update the admin password:
   ```python
   from src.models.admin import Admin
   admin = Admin.query.filter_by(username='admin').first()
   admin.set_password('your-secure-password')
   db.session.commit()
   ```

### Environment Variables
Set these in your production environment:
- `SECRET_KEY` - Strong secret key for session security
- `DATABASE_URL` - PostgreSQL connection string

### Additional Security Recommendations
- Use HTTPS in production
- Implement rate limiting for login attempts
- Consider adding two-factor authentication
- Regular security audits and updates

## Troubleshooting

### Admin Can't Login
1. Check if admin user exists in database
2. Verify password is correct
3. Check browser console for errors
4. Ensure cookies are enabled

### Session Issues
1. Clear browser cookies and localStorage
2. Check CORS configuration
3. Verify `supports_credentials=True` in Flask-CORS

### Database Issues
1. Ensure admin table is created
2. Check database connectivity
3. Verify admin user exists with correct credentials

