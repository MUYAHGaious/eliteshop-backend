#!/bin/bash

# EliteShop Development Startup Script

echo "🚀 Starting EliteShop Development Environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📥 Installing backend dependencies..."
pip install -r requirements.txt

# Set development environment variables
export FLASK_ENV=development
export SECRET_KEY=dev-secret-key

# Start backend in background
echo "🔥 Starting Flask backend..."
python src/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Navigate to frontend and install dependencies
echo "📦 Installing frontend dependencies..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    npm install
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "VITE_API_URL=http://localhost:5000/api" > .env
    echo "✅ Created frontend .env file"
fi

# Start frontend
echo "🎨 Starting React frontend..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 EliteShop is starting up!"
echo ""
echo "📍 Backend:  http://localhost:5000"
echo "📍 Frontend: http://localhost:5173"
echo "📍 Admin:    http://localhost:5173/admin"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait

