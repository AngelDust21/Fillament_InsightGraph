@echo off
echo =================================
echo    GitHub Push Script
echo    Fillament InsightGraph
echo =================================
echo.

echo STAP 1: Controleer remote repository
git remote -v | findstr "origin" > nul
if errorlevel 1 (
    echo Remote repository toevoegen...
    git remote add origin https://github.com/AngelDust21/Fillament_InsightGraph.git
) else (
    echo Remote repository bestaat al
)

echo.
echo STAP 2: Voeg alle wijzigingen toe
git add .

echo.
echo STAP 3: Commit wijzigingen
git commit -m "Automatische update via script"

echo.
echo STAP 4: Push naar GitHub
echo Dit kan even duren...
git push -u origin master

if errorlevel 1 (
    echo.
    echo Er is een fout opgetreden bij het pushen!
    echo Controleer of:
    echo 1. Je internetverbinding werkt
    echo 2. Je GitHub credentials correct zijn
    echo 3. Je repository bestaat op GitHub
) else (
    echo.
    echo =================================
    echo    Succesvol gepusht naar GitHub!
    echo =================================
)

pause 