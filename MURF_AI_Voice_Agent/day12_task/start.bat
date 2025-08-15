@echo off
echo Starting uvicorn main:app --reload --host 0.0.0.0 --port 8008 --reload-include .env
echo.

REM Check if virtual environment exists in parent directory
if not exist "..\venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found in '..\venv'!
    echo Please make sure you have a 'venv' folder in the root project directory.
    pause
    exit /b 1
)

REM Activate virtual environment
call "..\venv\Scripts\activate.bat"
echo [INFO] Virtual environment activated.
echo.

echo [INFO] Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo.

echo [INFO] Starting server...
echo [INFO] Application will be available at: http://localhost:8008
echo [INFO] Press Ctrl+C to stop the server.
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8008

pause
