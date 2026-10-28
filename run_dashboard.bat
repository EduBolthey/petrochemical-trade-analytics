@echo off
title Petrochemical Trade Analytics - Web Server
color 0A

echo ============================================================
echo   PETROCHEMICAL TRADE ANALYTICS - DASHBOARD LAUNCHER
echo ============================================================
echo.

set PYTHON_EXE=""

:: 1. Check Python 3.13 in User AppData (where all project dependencies are installed)
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set PYTHON_EXE="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    goto :FOUND
)

:: 2. Check Python 3.13 via py launcher
py -3.13 -c "import streamlit" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXE=py -3.13
    goto :FOUND
)

:: 3. Check default python
python -c "import streamlit" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_EXE=python
    goto :FOUND
)

echo [ERROR] Streamlit could not be found in default Python.
echo Trying Python 3.13 directly...
set PYTHON_EXE="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"

:FOUND
echo Launching Petrochemical Trade Analytics on http://localhost:8501 ...
echo Press Ctrl+C in this window to stop the server.
echo.

%PYTHON_EXE% -m streamlit run app.py --browser.gatherUsageStats false

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Server stopped with error code %ERRORLEVEL%.
    pause
)
