@echo off
echo ==========================================
echo Starting TripGenius Backend and Frontend...
echo ==========================================

REM Start FastAPI Backend
start "TripGenius Backend (FastAPI)" cmd /k "cd /d %~dp0backend && %~dp0.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM Start Next.js Frontend
start "TripGenius Frontend (Next.js)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers have been launched!
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - Docs: http://localhost:8000/docs
echo ==========================================
