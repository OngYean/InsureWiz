@echo off
echo 🚀 Starting InsureWiz Project...
echo.
echo This script will start both the backend AI server and frontend
echo.
echo 📋 Prerequisites:
echo - Python 3.8+ installed
echo - Node.js 18+ installed
echo - Google AI Studio API key configured
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 18+ and try again
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!
echo.

REM Start backend in a new window
echo 🐍 Starting AI Backend Server...
start "InsureWiz Backend" cmd /k "cd backend && run.bat"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window
echo 🌐 Starting Frontend...
start "InsureWiz Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo 🎉 Both servers are starting in separate windows!
echo.
echo 📡 Backend: http://localhost:8000
echo 🌐 Frontend: http://localhost:3000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 💡 Tips:
echo - Backend window: Press Ctrl+C to stop the AI server
echo - Frontend window: Press Ctrl+C to stop the web app
echo - Close these windows to stop the servers
echo.
pause
