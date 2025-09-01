@echo off
echo 🚀 Starting InsureWiz AI Chatbot Backend...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found
    echo Please copy env.example to .env and add your Google API key
    echo.
    copy env.example .env
    echo 📝 Created .env file. Please edit it with your Google API key before continuing.
    echo 💡 Get your API key from: https://makersuite.google.com/app/apikey
    pause
)

echo.
echo ✅ Backend ready! Starting server...
echo 📡 Server will be available at: http://localhost:8000
echo 🔗 API Documentation: http://localhost:8000/docs
echo 💬 Chat endpoint: http://localhost:8000/api/chat
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python run.py

pause
