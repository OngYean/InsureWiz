@echo off
echo ========================================
echo InsureWiz RAG Complete Setup Script
echo ========================================
echo.
echo This script will install all required dependencies
echo for the complete RAG system with insurewiz768 index.
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo Virtual environment found. Activating...
    call .venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

echo.
echo Installing/upgrading dependencies...
echo.

REM Upgrade pip
python -m pip install --upgrade pip

REM Install all requirements
pip install -r requirements.txt

echo.
echo Dependencies installed successfully!
echo.
echo You can now run the RAG completeness test:
echo   - test_rag_complete.bat (Windows)
echo   - test_rag_complete.ps1 (PowerShell)
echo   - python test_rag_complete.py (Direct)
echo.
pause

