@echo off
echo ============================================
echo   BESTELLINGEN ANALYSE WEB DASHBOARD
echo ============================================
echo.
echo Controleren of Streamlit is geinstalleerd...

python -m pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Streamlit is niet geinstalleerd!
    echo.
    echo Installeer de vereiste packages met:
    echo   python -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Streamlit gevonden!
echo.
echo Starting web dashboard op http://localhost:8501
echo.
echo Druk op Ctrl+C om te stoppen
echo ============================================
echo.

cd scripts
python -m streamlit run streamlit_app.py

pause 