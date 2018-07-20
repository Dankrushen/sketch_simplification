@echo off
title Sketch Simplification
cd /d %~dp0

echo Copying Input...
rmdir /S /Q Output\
xcopy Input Output\ /Y /S

echo.
echo Simplifying Sketches...
for /R Output\ %%F in (*.?*) do (
    echo Simplifying "%%~nF%%~xF"...
    python simplifytiled.py --img "%%F" --out "%%F"
)

echo.
echo Done! Press any key to exit...
pause > NUL