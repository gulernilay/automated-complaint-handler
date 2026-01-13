@echo off
setlocal enabledelayedexpansion

:: ==========================================
:: Chef Seasons - Excel Watcher (CLEAN VERSION)
:: ==========================================

chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

:: 🚀 SANAL ORTAM PYTHON
set PYTHON_PATH=C:\Users\nilay\Documents\GitHub\Müşteri_Şikayetleri\venv\Scripts\python.exe

:: 🚀 SCRIPT KLASÖRÜ
set SCRIPT_DIR=C:\Users\nilay\Documents\GitHub\Müşteri_Şikayetleri

cd /d "%SCRIPT_DIR%"

echo ==============================================
echo 📡 Excel Watcher başlatılıyor...
echo Python: %PYTHON_PATH%
echo Script: %SCRIPT_DIR%
echo ==============================================
echo.

:: 🚀 WATCHER'I BAŞLAT
"%PYTHON_PATH%" "%SCRIPT_DIR%\main.py"

echo.
echo 📌 Excel watcher durdu.
pause
