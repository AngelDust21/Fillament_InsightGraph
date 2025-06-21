@echo off
echo =================================
echo    GitHub Sync Script
echo    Fillament InsightGraph
echo    (Pull + Push in een keer)
echo =================================
echo.

echo STAP 1: Controleer remote repository
git remote -v | findstr "origin" > nul
if errorlevel 1 (
    echo Remote repository toevoegen...
    git remote add origin https://github.com/AngelDust21/Fillament_InsightGraph.git
) else (
    echo Remote repository gevonden
)

echo.
echo STAP 2: Haal eerst updates op van GitHub
echo Dit voorkomt conflicten...
git pull origin master

if errorlevel 1 (
    echo.
    echo FOUT bij pullen! Los eerst eventuele conflicten op.
    pause
    exit /b 1
)

echo.
echo STAP 3: Voeg lokale wijzigingen toe
git add .

echo.
echo STAP 4: Commit lokale wijzigingen
git commit -m "Automatische sync via script"

echo.
echo STAP 5: Push alles naar GitHub
echo Dit kan even duren...
git push origin master

if errorlevel 1 (
    echo.
    echo =================================
    echo    Er is een fout opgetreden!
    echo =================================
    echo Controleer je internetverbinding en GitHub credentials
) else (
    echo.
    echo =================================
    echo    Project volledig gesynchroniseerd!
    echo =================================
    echo Zowel lokaal als op GitHub zijn nu up-to-date
)

echo.
echo Huidige status:
git status -uno

echo.
echo =================================
pause 