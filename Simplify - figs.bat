@echo off
title Sketch Simplification
cd /d %~dp0

echo Copying figs...
rmdir /S /Q out\
xcopy figs out\ /Y /S

echo.
echo Simplifying Sketches...
for /R out\ %%F in (*.?*) do (
    echo Simplifying "%%~nF%%~xF"...
    python simplify.py --img "%%F" --out "%%F"
)

echo.
echo Done! Press any key to exit...
pause > NUL