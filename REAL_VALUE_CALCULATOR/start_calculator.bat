@echo off
echo ========================================
echo    3D Print Calculator - Starter
echo ========================================
echo.

REM Check if PHP is installed
php --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PHP is niet geïnstalleerd of niet in PATH
    echo.
    echo Installeer PHP van: https://windows.php.net/download/
    echo Zorg dat PHP in je PATH staat
    echo.
    pause
    exit /b 1
)

echo PHP gevonden! Versie:
php --version
echo.

REM Check if we're in the right directory
if not exist "index.php" (
    echo ERROR: index.php niet gevonden
    echo Zorg dat je dit script uitvoert vanuit de REAL_VALUE_CALCULATOR map
    echo.
    pause
    exit /b 1
)

REM Check if database exists, if not create it
if not exist "database/calculator.db" (
    echo Database niet gevonden. Aanmaken...
    if exist "database/schema.sql" (
        echo Database schema gevonden. Initialiseren...
        REM Create database directory if it doesn't exist
        if not exist "database" mkdir database
        
        REM Initialize database (this will be done by PHP)
        echo Database wordt geïnitialiseerd bij eerste gebruik...
    ) else (
        echo WARNING: schema.sql niet gevonden
    )
)

echo.
echo ========================================
echo    Start 3D Print Calculator...
echo ========================================
echo.
echo Server wordt gestart op: http://localhost:8000
echo.
echo Druk Ctrl+C om te stoppen
echo.

REM Start PHP development server
php -S localhost:8000

echo.
echo Server gestopt.
pause 