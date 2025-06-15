@echo off
echo =================================
echo    GitHub Push Script
echo    H2D Prijs Calculator
echo =================================
echo.

echo STAP 1: Voeg remote repository toe
echo GitHub gebruikersnaam: AngelDust21
echo.
set username=AngelDust21

echo.
echo Remote repository toevoegen...
git remote add origin https://github.com/%username%/bedrijfsleider.git

echo.
echo STAP 2: Push naar GitHub
echo Dit kan even duren...
git push -u origin master

echo.
echo =================================
echo    Klaar! 
echo    Je project staat nu op GitHub!
echo =================================
pause 