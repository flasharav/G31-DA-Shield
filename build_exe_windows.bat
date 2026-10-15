@echo off
title Build DA-Shield-Demo.exe
cd /d "%~dp0"
set PY=python
%PY% --version >nul 2>&1 || set PY=py
echo Installing libraries and PyInstaller...
%PY% -m pip install -r requirements.txt pyinstaller
echo Building the .exe (this takes a few minutes)...
%PY% -m PyInstaller --onefile --console --name DA-Shield-Demo --paths src ^
  --exclude-module matplotlib --exclude-module pandas --exclude-module tkinter --exclude-module PIL ^
  --exclude-module IPython --exclude-module pytest --exclude-module pyarrow --exclude-module sympy --exclude-module numba ^
  src\dashield_demo.py
if not exist exe mkdir exe
move /y dist\DA-Shield-Demo.exe exe\DA-Shield-Demo.exe
rmdir /s /q build dist
del DA-Shield-Demo.spec
echo.
echo Done. The program is at exe\DA-Shield-Demo.exe
pause
