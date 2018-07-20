@echo off
title Sketch Simplification
cd /d %~dp0
python simplify.py
echo Press any key to exit...
pause > NUL