@echo off
echo Testing AI Chatbot Functionality...
echo.

cd /d "%~dp0"
python test_ai_chatbot.py

echo.
echo Test completed. Press any key to exit.
pause >nul

