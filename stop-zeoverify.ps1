# ZeoVerify 3.0 - Stop Script (PowerShell)
# This script cleanly stops all ZeoVerify services

Write-Host "========================================" -ForegroundColor Red
Write-Host "    ZEOVERIFY 3.0 - STOP SCRIPT" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# Function to stop processes on specific ports
function Stop-ProcessOnPort {
    param([int]$Port)
    try {
        $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        foreach ($process in $processes) {
            if ($process.OwningProcess) {
                $processName = (Get-Process -Id $process.OwningProcess).ProcessName
                Stop-Process -Id $process.OwningProcess -Force -ErrorAction SilentlyContinue
                Write-Host "✓ Stopped $processName on port $Port" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "No processes found on port $Port" -ForegroundColor Yellow
    }
}

Write-Host "Stopping all ZeoVerify services..." -ForegroundColor Yellow

# Stop processes on specific ports
Stop-ProcessOnPort 5000  # Backend API
Stop-ProcessOnPort 5173  # Frontend

# Stop any remaining Python and Node processes
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    $pythonProcesses | Stop-Process -Force
    Write-Host "✓ Stopped Python processes" -ForegroundColor Green
}

$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    $nodeProcesses | Stop-Process -Force
    Write-Host "✓ Stopped Node processes" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "    ALL SERVICES STOPPED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
