# 🚀 Render Deployment Guide for EliteShop

This guide will walk you through deploying your e-commerce application on Render with separate backend and frontend services.

## 📋 Prerequisites

- GitHub account
- Render account (free tier available)
- Your code pushed to a GitHub repository

## 🗄️ Step 1: Database Setup (PostgreSQL)

1. **Login to Render**: Go to [dashboard.render.com](https://dashboard.render.com)

2. **Create Database**:
   - Click "New" → "PostgreSQL"
   - **Name**: `eliteshop-database`
   - **Database**: `eliteshop`
   - **User**: `eliteshop_user`
   - **Region**: Choose closest to your target audience
   - **PostgreSQL Version**: 15 (latest)
   - **Datadog API Key**: Leave blank
   - Click "Create Database"

3. **Save Database URLs**:
   - **Internal Database URL**: Used by your backend service
   - **External Database URL**: For external connections (if needed)
   - Copy the **Internal Database URL** - you'll need it for the backend

## 🔧 Step 2: Backend Deployment

1. **Create Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select your repository
   - **Name**: `eliteshop-backend`
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave blank (or specify if your backend is in a subdirectory)

2. **Build & Deploy Settings**:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.main:app`

3. **Environment Variables**:
   Click "Advanced" and add these environment variables:
   ```
   DATABASE_URL = [Your Internal Database URL from Step 1]
   SECRET_KEY = [Generate a secure random string, e.g., use Python: import secrets; secrets.token_hex(32)]
   FLASK_ENV = production
   ```

4. **Instance Type**:
   - **Free Tier**: Good for testing
   - **Starter**: $7/month, better performance
   - **Standard**: $25/month, production-ready

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (usually 2-5 minutes)
   - Your backend will be available at: `https://eliteshop-backend.onrender.com`

## 🎨 Step 3: Frontend Deployment

### Option A: Static Site (Recommended)

1. **Update Frontend Environment**:
   In your local project, create `frontend/.env.production`:
   ```bash
   VITE_API_URL=https://eliteshop-backend.onrender.com/api
   ```

2. **Create Static Site**:
   - Click "New" → "Static Site"
   - Select your repository
   - **Name**: `eliteshop-frontend`
   - **Branch**: `main`
   - **Root Directory**: Leave blank

3. **Build Settings**:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`

4. **Environment Variables**:
   ```
   VITE_API_URL = https://eliteshop-backend.onrender.com/api
   ```

5. **Deploy**:
   - Click "Create Static Site"
   - Your frontend will be available at: `https://eliteshop-frontend.onrender.com`

### Option B: Full-Stack Single Service

If you prefer to serve the frontend from the Flask backend:

1. **Build Frontend Locally**:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   cp -r frontend/dist/* src/static/
   ```

2. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Add built frontend to static files"
   git push
   ```

3. **Deploy as Web Service** (same as backend steps above)
   - Your entire app will be available at: `https://eliteshop-backend.onrender.com`

## 🔧 Step 4: Configuration & Testing

### Backend Configuration

Your Flask app is already configured to:
- Use PostgreSQL in production (via DATABASE_URL)
- Use SQLite in development
- Auto-seed the database with sample products
- Handle CORS for frontend requests

### Frontend Configuration

Make sure your frontend `.env.production` points to your backend:
```bash
VITE_API_URL=https://your-actual-backend-url.onrender.com/api
```

### Testing Your Deployment

1. **Backend Health Check**:
   - Visit: `https://eliteshop-backend.onrender.com/api/products`
   - Should return JSON with product data

2. **Frontend Check**:
   - Visit your frontend URL
   - Test product browsing, cart functionality, and admin panel

3. **Database Check**:
   - Products should load automatically (seeded on first run)
   - Test adding products via admin panel

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**:
   ```bash
   # Check your requirements.txt has all dependencies
   # Ensure Python version compatibility
   ```

2. **Database Connection Errors**:
   ```bash
   # Verify DATABASE_URL is set correctly
   # Check database is in same region as backend
   ```

3. **CORS Errors**:
   ```bash
   # Ensure backend CORS is configured for your frontend domain
   # Check VITE_API_URL is correct
   ```

4. **Frontend Build Issues**:
   ```bash
   # Ensure Node.js version is compatible
   # Check all npm dependencies are available
   ```

### Debugging Tips

1. **Check Logs**:
   - Go to your service dashboard
   - Click "Logs" to see real-time logs
   - Look for error messages

2. **Environment Variables**:
   - Verify all required env vars are set
   - Check for typos in variable names

3. **Database Issues**:
   - Use the External Database URL to connect with a PostgreSQL client
   - Verify tables are created correctly

## 🔄 Continuous Deployment

Render automatically deploys when you push to your connected branch:

1. **Auto-Deploy**: Enabled by default
2. **Manual Deploy**: Use "Manual Deploy" button in dashboard
3. **Deploy Hooks**: Set up webhooks for external triggers

## 💰 Cost Estimation

### Free Tier Limits:
- **PostgreSQL**: 1GB storage, 1 month retention
- **Web Service**: 750 hours/month (sleeps after 15min inactivity)
- **Static Site**: Unlimited bandwidth

### Paid Tiers:
- **Starter Database**: $7/month (10GB, 90-day retention)
- **Starter Web Service**: $7/month (no sleep, better performance)
- **Standard**: $25/month (production-ready)

## 🔒 Security Best Practices

1. **Environment Variables**: Never commit secrets to Git
2. **Database**: Use Internal Database URL for backend connections
3. **HTTPS**: Render provides SSL certificates automatically
4. **CORS**: Configure for your specific frontend domain in production

## 📈 Monitoring & Maintenance

1. **Health Checks**: Render monitors your services automatically
2. **Logs**: Monitor application logs for errors
3. **Metrics**: View performance metrics in dashboard
4. **Alerts**: Set up notifications for service issues

## 🚀 Going Live Checklist

- [ ] Database created and accessible
- [ ] Backend deployed and responding to API calls
- [ ] Frontend deployed and loading correctly
- [ ] Environment variables configured
- [ ] Sample data seeded
- [ ] Admin panel accessible
- [ ] Cart and checkout functionality working
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active
- [ ] Monitoring set up

## 📞 Support

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Community**: [community.render.com](https://community.render.com)
- **Support**: Available for paid plans

---

**Your EliteShop is now live! 🎉**

Remember to test all functionality thoroughly before announcing your launch!

