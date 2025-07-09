@echo off
echo 🚀 Starting EliteShop Development Environment...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install backend dependencies
echo 📥 Installing backend dependencies...
pip install -r requirements.txt

REM Set development environment variables
set FLASK_ENV=development
set SECRET_KEY=dev-secret-key

REM Start backend
echo 🔥 Starting Flask backend...
start /B venv\Scripts\python.exe src\main.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Navigate to frontend and install dependencies
echo 📦 Installing frontend dependencies...
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    npm install
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo VITE_API_URL=http://localhost:5000/api > .env
    echo ✅ Created frontend .env file
)

REM Start frontend
echo 🎨 Starting React frontend...
start /B npm run dev

echo.
echo 🎉 EliteShop is starting up!
echo.
echo 📍 Backend:  http://localhost:5000
echo 📍 Frontend: http://localhost:5173
echo 📍 Admin:    http://localhost:5173/admin
echo.
echo Press any key to stop all services...
pause >nul

REM Cleanup
echo.
echo 🛑 Stopping services...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
echo ✅ All services stopped

