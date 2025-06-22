@echo off
echo =================================
echo    GitHub Pull Script
echo    Fillament InsightGraph
echo =================================
echo.

echo STAP 1: Controleer remote repository
git remote -v | findstr "origin" > nul
if errorlevel 1 (
    echo FOUT: Geen remote repository gevonden!
    echo Voer eerst push_to_github.bat uit om repository in te stellen
    pause
    exit /b 1
) else (
    echo Remote repository gevonden
)

echo.
echo STAP 2: Controleer huidige status
echo Huidige status van je project:
git status -uno

echo.
echo STAP 3: Haal updates op van GitHub
echo Dit kan even duren...
git pull origin master

if errorlevel 1 (
    echo.
    echo =================================
    echo    Er is een fout opgetreden!
    echo =================================
    echo Mogelijke oorzaken:
    echo 1. Geen internetverbinding
    echo 2. Merge conflicten
    echo 3. Repository bestaat niet
    echo.
    echo Bij merge conflicten:
    echo - Los de conflicten op in je bestanden
    echo - Gebruik: git add .
    echo - Gebruik: git commit -m "Conflicten opgelost"
) else (
    echo.
    echo =================================
    echo    Project succesvol bijgewerkt!
    echo =================================
    echo.
    echo Nieuwe status:
    git status -uno
)

echo.
echo =================================
pause 