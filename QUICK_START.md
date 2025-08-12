# 🚀 ZeoVerify 3.0 - Quick Start Guide

## One-Click Startup

### Option 1: PowerShell (Recommended)
1. **Right-click** on `start-zeoverify.ps1`
2. Select **"Run with PowerShell"**
3. Wait for all services to start
4. Your browser will automatically open to `http://localhost:5173`

### Option 2: Batch File
1. **Double-click** on `start-zeoverify.bat`
2. Wait for all services to start
3. Your browser will automatically open to `http://localhost:5173`

## What Happens During Startup

1. **Port Cleanup** - Stops any existing processes on ports 5000 and 5173
2. **Backend Start** - Launches Flask API on port 5000
3. **Frontend Start** - Launches React app on port 5173
4. **Connection Test** - Verifies backend is responding
5. **Browser Launch** - Opens the application automatically

## Service URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## Stopping Services

### Option 1: PowerShell
1. **Right-click** on `stop-zeoverify.ps1`
2. Select **"Run with PowerShell"**

### Option 2: Manual
- Close the terminal windows that opened during startup
- Or use `Ctrl+C` in each terminal

## Troubleshooting

### "Backend Disconnected" Error
1. Make sure no other applications are using port 5000
2. Run the startup script again
3. Check if Python and required packages are installed

### "Port Already in Use" Error
1. Run the startup script again (it will clear ports automatically)
2. Or manually stop processes:
   ```powershell
   netstat -ano | findstr :5000
   taskkill /f /pid [PID_NUMBER]
   ```

### File Upload Issues
1. Ensure backend shows "Backend Connected" status
2. Check browser console for error messages
3. Verify file format (PDF, JPG, PNG, JPEG)
4. File size must be under 5MB

## Manual Startup (Advanced Users)

If you prefer to start services manually:

### Backend
```bash
cd ai-engine/api
python app_simple.py
```

### Frontend
```bash
cd frontend
npm run dev
```

## Requirements

- **Python 3.8+** with required packages
- **Node.js 16+** with npm
- **Windows 10/11** (for batch/PowerShell scripts)

## Support

If you encounter issues:
1. Check the terminal windows for error messages
2. Ensure all required dependencies are installed
3. Try running the startup script again
4. Check the browser console for frontend errors
