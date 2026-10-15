@echo off
title DA-Shield - Group 31
cd /d "%~dp0"
set PY=python
%PY% --version >nul 2>&1 || set PY=py
%PY% --version >nul 2>&1 || (
  echo Python was not found. Install Python 3.10+ from https://www.python.org/downloads/
  echo and tick "Add python.exe to PATH" during installation.
  pause
  exit /b 1
)
echo [1/4] Installing libraries...
%PY% -m pip install -r requirements.txt
echo [2/4] Running Modules A, B and C (full evaluation)...
%PY% src\dashield_prototype.py > outputs\run_log.txt
echo       Results saved to outputs\results.json
echo [3/4] Drawing figures...
%PY% src\make_figures.py
echo       Figures saved to outputs\figures
echo [4/4] Opening the interactive demo...
%PY% src\dashield_demo.py
pause
