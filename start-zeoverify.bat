@echo off
echo ========================================
echo    ZEOVERIFY 3.0 - STARTUP SCRIPT
echo ========================================
echo.

:: Kill any existing processes on ports 5000 and 5173
echo [1/4] Stopping existing processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do taskkill /f /pid %%a >nul 2>&1
)
netstat -ano | findstr :5173 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do taskkill /f /pid %%a >nul 2>&1
)
echo ✓ Ports cleared

:: Wait a moment for ports to be released
timeout /t 2 /nobreak >nul

:: Start Flask API Backend
echo [2/4] Starting Flask API Backend...
cd ai-engine\api
start "ZeoVerify Backend" cmd /k "python app_simple.py"
cd ..\..

:: Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

:: Test backend connection
echo Testing backend connection...
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend is running on http://localhost:5000
) else (
    echo ⚠ Backend may still be starting up...
)

:: Start React Frontend
echo [3/4] Starting React Frontend...
cd frontend
start "ZeoVerify Frontend" cmd /k "npm run dev"
cd ..

:: Wait for frontend to start
echo Waiting for frontend to start...
timeout /t 8 /nobreak >nul

:: Final status check
echo [4/4] Final status check...
echo.
echo ========================================
echo    SERVICE STATUS
echo ========================================
echo.

:: Check backend
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend API: http://localhost:5000
) else (
    echo ✗ Backend API: Not responding
)

:: Check frontend
netstat -ano | findstr :5173 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend: http://localhost:5173
) else (
    echo ✗ Frontend: Not responding
)

echo.
echo ========================================
echo    ZEOVERIFY IS READY!
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:5000
echo.
echo Press any key to open the application...
pause >nul

:: Open frontend in default browser
start http://localhost:5173

echo.
echo Application opened in browser!
echo Keep these terminal windows open while using ZeoVerify.
echo.
echo Press any key to exit this startup script...
pause >nul
