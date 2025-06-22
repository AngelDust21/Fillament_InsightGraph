@echo off
echo ========================================
echo Database Maintenance Script
echo Voor grote datasets (1M+ records)
echo ========================================
echo.

cd /d "%~dp0"

echo Starten van database maintenance...
php database_maintenance.php

echo.
echo Database maintenance voltooid!
echo.

echo Druk op een toets om af te sluiten...
pause > nul 