@echo off
echo ========================================
echo InsureWiz RAG System Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found: 
python --version

echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!

echo.
echo Creating .env file...
if not exist .env (
    copy env.example .env
    echo Created .env file from template
    echo Please edit .env file with your API keys
) else (
    echo .env file already exists
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run: python test_rag.py
echo 3. Start server: python run.py
echo.
echo For help, see RAG_INTEGRATION.md
echo.
pause

