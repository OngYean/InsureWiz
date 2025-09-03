Write-Host "Installing Tavily integration for InsureWiz chatbot..." -ForegroundColor Green
Write-Host ""

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install tavily-python

Write-Host ""
Write-Host "Tavily integration installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Get your Tavily API key from https://tavily.com/" -ForegroundColor White
Write-Host "2. Add TAVILY_API_KEY=your_key_here to your .env file" -ForegroundColor White
Write-Host "3. Restart your backend server" -ForegroundColor White
Write-Host ""
Write-Host "New endpoints available:" -ForegroundColor Cyan
Write-Host "- POST /api/chat/enhanced - Enhanced RAG + Tavily responses" -ForegroundColor White
Write-Host "- GET /api/chat/tavily-health - Check Tavily service health" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to continue"

