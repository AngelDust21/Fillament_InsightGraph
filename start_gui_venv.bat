@echo off
echo =================================
echo    H2D Price Calculator GUI
echo    Met Virtual Environment
echo =================================
echo.

echo Starting GUI met virtual environment...
echo Let op: Sluit dit venster NIET tijdens gebruik!
echo.

REM Start de GUI met de juiste Python
.venv\Scripts\python.exe start_gui.py

echo.
echo GUI is afgesloten.
pause 