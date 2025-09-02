@echo off
echo ========================================
echo InsureWiz RAG Completeness Test Suite
echo ========================================
echo.
echo This script will test the complete RAG chain
echo with your new insurewiz768 index.
echo.
echo Press any key to continue...
pause >nul

echo.
echo Starting RAG completeness tests...
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Run the complete RAG test
python test_rag_complete.py

echo.
echo Test completed!
echo Check the results above to see if your RAG system is complete.
echo.
pause

