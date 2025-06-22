@echo off
setlocal enabledelayedexpansion
echo =================================
echo    GitHub Pull Script
echo    Fillament InsightGraph
echo =================================
echo.

REM Controleer of git beschikbaar is
git --version > nul 2>&1
if errorlevel 1 (
    echo FOUT: Git is niet geïnstalleerd of niet gevonden in PATH!
    pause
    exit /b 1
)

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
echo STAP 3: Controleer op lokale wijzigingen
git diff --quiet
if errorlevel 1 (
    echo.
    echo WAARSCHUWING: Je hebt lokale wijzigingen!
    echo.
    echo Wat wil je doen?
    echo 1. Wijzigingen tijdelijk opslaan (stash) en later terugzetten
    echo 2. Wijzigingen committen voor het pullen
    echo 3. Annuleren
    echo.
    set /p keuze="Maak je keuze (1/2/3): "
    
    if "!keuze!"=="1" (
        echo Wijzigingen worden tijdelijk opgeslagen...
        git stash push -m "Tijdelijke opslag voor pull"
        set stashed=1
    ) else if "!keuze!"=="2" (
        echo.
        set /p commit_msg="Geef een commit bericht: "
        git add .
        git commit -m "!commit_msg!"
    ) else (
        echo Pull geannuleerd.
        pause
        exit /b 0
    )
)

echo.
echo STAP 4: Haal updates op van GitHub
echo Dit kan even duren...
git pull origin master --no-rebase

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
    echo.
    
    REM Als we gestashed hadden, probeer terug te zetten
    if defined stashed (
        echo Probeer gestashte wijzigingen terug te zetten...
        git stash pop
    )
) else (
    echo.
    echo =================================
    echo    Project succesvol bijgewerkt!
    echo =================================
    
    REM Als we gestashed hadden, zet wijzigingen terug
    if defined stashed (
        echo.
        echo Terugzetten van tijdelijk opgeslagen wijzigingen...
        git stash pop
        if errorlevel 1 (
            echo WAARSCHUWING: Conflicten bij terugzetten van wijzigingen!
            echo Gebruik 'git status' om te zien welke bestanden conflicten hebben.
        )
    )
    
    echo.
    echo Nieuwe status:
    git status -uno
)

echo.
echo =================================
pause 