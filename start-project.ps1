# InsureWiz Project Startup Script
# This script starts both the backend AI server and frontend

Write-Host "🚀 Starting InsureWiz Project..." -ForegroundColor Green
Write-Host ""
Write-Host "This script will start both the backend AI server and frontend" -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 Prerequisites:" -ForegroundColor Cyan
Write-Host "- Python 3.8+ installed"
Write-Host "- Node.js 18+ installed"
Write-Host "- Google AI Studio API key configured"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "✅ Prerequisites check passed!" -ForegroundColor Green
Write-Host ""

# Start backend in a new window
Write-Host "🐍 Starting AI Backend Server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\run.bat" -WindowStyle Normal

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend in a new window
Write-Host "🌐 Starting Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "🎉 Both servers are starting in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "📡 Backend: http://localhost:8000" -ForegroundColor Yellow
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "💡 Tips:" -ForegroundColor Cyan
Write-Host "- Backend window: Press Ctrl+C to stop the AI server"
Write-Host "- Frontend window: Press Ctrl+C to stop the web app"
Write-Host "- Close these windows to stop the servers"
Write-Host ""

Read-Host "Press Enter to exit"
