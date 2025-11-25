@echo off
echo ========================================
echo   Clear Face Database and Start Fresh
echo ========================================
echo.
echo This will:
echo 1. Delete the current face database
echo 2. Start the application with stricter matching
echo.
echo The new threshold (0.25) prevents false matches
echo between different people.
echo.
pause

venv\Scripts\python.exe clear_faces.py
echo.
echo Starting application...
echo.
venv\Scripts\python.exe src/main.py
pause
