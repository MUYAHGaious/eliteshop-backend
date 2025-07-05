# EliteShop - Premium E-commerce MVP

A complete e-commerce platform with a futuristic design, featuring product catalog, shopping cart, checkout, and admin panel.

## 🚀 Features

- **Modern UI/UX**: Futuristic design with animations and gradients
- **Product Catalog**: Browse products with search, filters, and sorting
- **Shopping Cart**: Add/remove items with real-time updates
- **Secure Checkout**: Multi-step checkout process with order confirmation
- **Admin Dashboard**: Comprehensive admin panel with analytics and product management
- **Responsive Design**: Works perfectly on desktop and mobile devices

## 🛠 Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite/PostgreSQL** - Database (SQLite for development, PostgreSQL for production)

### Frontend
- **React** - Frontend framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Lucide React** - Icon library
- **Recharts** - Chart library for admin dashboard
- **shadcn/ui** - UI component library

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **pnpm** (recommended) or npm
- **Git**

## 🏃‍♂️ Local Development Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ecommerce-mvp
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional for development)
export FLASK_ENV=development
export SECRET_KEY=your-secret-key

# Run the backend
python src/main.py
```

The backend will be available at `http://localhost:5000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Create environment file
cp .env.example .env

# Edit .env file and set:
# VITE_API_URL=http://localhost:5000/api

# Start development server
pnpm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Database Setup

The database will be automatically created when you first run the backend. Sample products will be seeded automatically.

To manually seed the database:

```bash
python src/seed_data.py
```

## 🚀 Deployment on Render

### 1. Database Setup (PostgreSQL)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "PostgreSQL"
3. Configure your database:
   - **Name**: `eliteshop-db`
   - **Database**: `eliteshop`
   - **User**: `eliteshop`
   - **Region**: Choose closest to your users
4. Click "Create Database"
5. Note down the **Internal Database URL** and **External Database URL**

### 2. Backend Deployment

1. Push your code to GitHub
2. Go to Render Dashboard
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: `eliteshop-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.main:app`
   - **Instance Type**: Free or Starter
6. Add Environment Variables:
   - `DATABASE_URL`: Your PostgreSQL Internal Database URL
   - `SECRET_KEY`: A secure random string
   - `FLASK_ENV`: `production`
7. Click "Create Web Service"

### 3. Frontend Deployment

1. Update your frontend environment:
   ```bash
   cd frontend
   # Edit .env or create .env.production
   echo "VITE_API_URL=https://your-backend-app.onrender.com/api" > .env.production
   ```

2. Build the frontend:
   ```bash
   pnpm run build
   ```

3. Deploy to Render:
   - Go to Render Dashboard
   - Click "New" → "Static Site"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `eliteshop-frontend`
     - **Build Command**: `cd frontend && pnpm install && pnpm run build`
     - **Publish Directory**: `frontend/dist`
   - Add Environment Variable:
     - `VITE_API_URL`: `https://your-backend-app.onrender.com/api`
   - Click "Create Static Site"

### 4. Alternative: Full-Stack Deployment

You can also deploy the entire application as a single service:

1. Build the frontend:
   ```bash
   cd frontend
   pnpm run build
   cd ..
   cp -r frontend/dist/* src/static/
   ```

2. Deploy to Render as a Web Service with the backend configuration above.

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
SECRET_KEY=your-super-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
FLASK_ENV=production
PORT=5000
```

#### Frontend (.env)
```bash
VITE_API_URL=https://your-backend-app.onrender.com/api
```

## 📁 Project Structure

```
ecommerce-mvp/
├── src/                          # Backend source code
│   ├── models/                   # Database models
│   │   ├── user.py              # User and database setup
│   │   └── product.py           # Product, Order, Cart models
│   ├── routes/                   # API routes
│   │   ├── products.py          # Product endpoints
│   │   ├── cart.py              # Cart endpoints
│   │   ├── orders.py            # Order endpoints
│   │   └── admin.py             # Admin endpoints
│   ├── static/                   # Static files (built frontend)
│   ├── database/                 # SQLite database (development)
│   ├── main.py                   # Flask application entry point
│   └── seed_data.py             # Database seeding script
├── frontend/                     # Frontend source code
│   ├── src/
│   │   ├── components/          # Reusable components
│   │   ├── pages/               # Page components
│   │   ├── context/             # React context (cart state)
│   │   └── App.jsx              # Main app component
│   ├── public/                   # Public assets
│   └── package.json             # Frontend dependencies
├── requirements.txt              # Python dependencies
├── Procfile                      # Render deployment config
└── README.md                     # This file
```

## 🎯 API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get single product

### Cart
- `GET /api/cart` - Get cart items
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/:id` - Update cart item
- `DELETE /api/cart/:id` - Remove cart item
- `DELETE /api/cart` - Clear cart

### Orders
- `POST /api/orders/checkout` - Create order
- `GET /api/orders/:orderNumber` - Get order details

### Admin
- `GET /api/admin/products` - Get all products (admin)
- `POST /api/admin/products` - Create product
- `PUT /api/admin/products/:id` - Update product
- `DELETE /api/admin/products/:id` - Delete product
- `GET /api/admin/orders` - Get all orders
- `GET /api/admin/orders/stats` - Get order statistics

## 🎨 Design Features

- **Futuristic Theme**: Purple/pink gradients with dark backgrounds
- **Animations**: Smooth transitions and hover effects using Framer Motion
- **Responsive**: Mobile-first design that works on all devices
- **Interactive**: Dynamic cart updates, search, filters, and sorting
- **Professional**: Clean, modern interface suitable for premium brands

## 🔒 Security Features

- **CORS Protection**: Configured for cross-origin requests
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **Environment Variables**: Sensitive data stored in environment variables

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the backend CORS is configured correctly
2. **Database Connection**: Check your DATABASE_URL environment variable
3. **Build Failures**: Ensure all dependencies are installed correctly
4. **API Not Found**: Verify the VITE_API_URL is set correctly

### Development Tips

- Use browser developer tools to debug API calls
- Check backend logs for error messages
- Ensure both frontend and backend are running on correct ports
- Verify environment variables are loaded correctly

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support, email support@eliteshop.com or create an issue in the repository.

---

**Happy Coding! 🚀**

