@echo off
title Sketch Simplification
cd /d %~dp0

echo Copying Input...
rmdir /S /Q Output\
xcopy Input Output\ /Y /S

echo.
echo Simplifying Sketches...
for /R Output\ %%F in (*.?*) do (
    convert "%%F" -resize "480x480>" "%%F"
    echo Simplifying "%%~nF%%~xF"...
    python simplify.py --img "%%F" --out "%%F"
)

echo.
echo Done! Press any key to exit...
pause > NUL