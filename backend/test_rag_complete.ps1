# InsureWiz RAG Completeness Test Suite
# PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "InsureWiz RAG Completeness Test Suite" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will test the complete RAG chain" -ForegroundColor Yellow
Write-Host "with your new insurewiz768 index." -ForegroundColor Yellow
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & .venv\Scripts\Activate.ps1
}

Write-Host ""
Write-Host "Starting RAG completeness tests..." -ForegroundColor Green
Write-Host ""

try {
    # Run the complete RAG test
    python test_rag_complete.py
    
    Write-Host ""
    Write-Host "Test completed successfully!" -ForegroundColor Green
    Write-Host "Check the results above to see if your RAG system is complete." -ForegroundColor Yellow
    
} catch {
    Write-Host ""
    Write-Host "Error running tests: $_" -ForegroundColor Red
    Write-Host "Check your Python environment and dependencies." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

