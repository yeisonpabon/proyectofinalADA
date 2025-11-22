@echo off
REM Ejecutar GUI del Sistema de Análisis de Complejidad
REM Haz doble clic en este archivo para ejecutar

setlocal enabledelayedexpansion

REM Obtener la ruta del script
set SCRIPT_DIR=%~dp0

REM Activar virtual environment
call "%SCRIPT_DIR%.venv\Scripts\activate.bat"

REM Ejecutar la GUI
python "%SCRIPT_DIR%GUI.py"

pause
