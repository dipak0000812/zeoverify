# ZeoVerify 3.0 - Startup Script (PowerShell)
# This script ensures proper startup of all services

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    ZEOVERIFY 3.0 - STARTUP SCRIPT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to kill processes on specific ports
function Stop-ProcessOnPort {
    param([int]$Port)
    try {
        $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        foreach ($process in $processes) {
            if ($process.OwningProcess) {
                Stop-Process -Id $process.OwningProcess -Force -ErrorAction SilentlyContinue
                Write-Host "✓ Stopped process on port $Port" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "No processes found on port $Port" -ForegroundColor Yellow
    }
}

# Step 1: Stop existing processes
Write-Host "[1/4] Stopping existing processes..." -ForegroundColor Yellow
Stop-ProcessOnPort 5000
Stop-ProcessOnPort 5173

# Kill any existing Python and Node processes
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "✓ Ports cleared" -ForegroundColor Green

# Wait for ports to be released
Start-Sleep -Seconds 3

# Step 2: Start Flask API Backend
Write-Host "[2/4] Starting Flask API Backend..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "ai-engine\api"
Start-Process -FilePath "python" -ArgumentList "app_simple.py" -WorkingDirectory $backendPath -WindowStyle Normal -PassThru | Out-Null

# Wait for backend to start
Write-Host "Waiting for backend to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 6

# Test backend connection
Write-Host "Testing backend connection..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend is running on http://localhost:5000" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Backend may still be starting up..." -ForegroundColor Yellow
}

# Step 3: Start React Frontend
Write-Host "[3/4] Starting React Frontend..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory $frontendPath -WindowStyle Normal -PassThru | Out-Null

# Wait for frontend to start
Write-Host "Waiting for frontend to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Step 4: Final status check
Write-Host "[4/4] Final status check..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    SERVICE STATUS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend API: http://localhost:5000" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Backend API: Not responding" -ForegroundColor Red
}

# Check frontend
$frontendPort = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($frontendPort) {
    Write-Host "✓ Frontend: http://localhost:5173" -ForegroundColor Green
} else {
    Write-Host "✗ Frontend: Not responding" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    ZEOVERIFY IS READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "Backend:  http://localhost:5000" -ForegroundColor White
Write-Host ""

# Open frontend in default browser
Write-Host "Opening application in browser..." -ForegroundColor Cyan
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Application opened in browser!" -ForegroundColor Green
Write-Host "Keep the terminal windows open while using ZeoVerify." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this startup script..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
