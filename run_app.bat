@echo off
REM Start Climate Change Trends Application

echo Starting Climate Change Trends Application...
echo.

REM Start Backend in a new window
echo Starting Backend (FastAPI) on http://localhost:8000...
start cmd /k "cd /d c:\Users\gowsik\Desktop\climate-change-trends\backend && python run.py"

REM Wait for backend to start
timeout /t 5 /nobreak

REM Start Frontend in a new window
echo Starting Frontend (Streamlit) on http://localhost:8505...
start cmd /k "cd /d c:\Users\gowsik\Desktop\climate-change-trends\frontend && python -m streamlit run app.py"

REM Wait for frontend to start
timeout /t 5 /nobreak

REM Open Browser
echo Opening application in browser...
start http://localhost:8505

echo.
echo Application is starting! Frontend will open in your default browser.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8505
echo.
pause
