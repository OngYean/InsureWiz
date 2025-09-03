@echo off
echo Installing Tavily integration for InsureWiz chatbot...
echo.

echo Installing Python dependencies...
pip install tavily-python

echo.
echo Tavily integration installed successfully!
echo.
echo Next steps:
echo 1. Get your Tavily API key from https://tavily.com/
echo 2. Add TAVILY_API_KEY=your_key_here to your .env file
echo 3. Restart your backend server
echo.
echo New endpoints available:
echo - POST /api/chat/enhanced - Enhanced RAG + Tavily responses
echo - GET /api/chat/tavily-health - Check Tavily service health
echo.
pause

