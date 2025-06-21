@echo off
echo ========================================
echo Database Herbouw Script
echo Met geoptimaliseerd schema voor grote datasets
echo ========================================
echo.

cd /d "%~dp0"

echo WAARSCHUWING: Dit zal de bestaande database vervangen!
echo Een backup wordt automatisch gemaakt.
echo.
echo Wilt u doorgaan? (j/n): 
set /p choice=

if /i "%choice%"=="j" (
    echo.
    echo Starten van database herbouw...
    php database_maintenance.php rebuild
    
    echo.
    echo Database herbouw voltooid!
    echo De database is nu geoptimaliseerd voor grote datasets.
) else (
    echo.
    echo Database herbouw geannuleerd.
)

echo.
echo Druk op een toets om af te sluiten...
pause > nul 