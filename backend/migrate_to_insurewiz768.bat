@echo off
echo ========================================
echo InsureWiz Index Migration Script
echo ========================================
echo.
echo This script will migrate documents from the old
echo 'insurewiz' index to the new 'insurewiz768' index.
echo.
echo The new index uses 768 dimensions compatible with
echo Google's embedding-001 model.
echo.
echo Press any key to continue...
pause >nul

echo.
echo Starting migration process...
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Run the migration script
python migrate_to_insurewiz768.py

echo.
echo Migration completed!
echo Check the results above to see if it was successful.
echo.
pause

