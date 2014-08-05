@echo off
set PYTHONPATH=%~dp0
echo %PYTHONPATH%
python ..\workspace_tools\build.py -m LPC1768_MINI_DK2 -tARM -v
python ..\workspace_tools\project.py -m LPC1768_MINI_DK2 -i uvision -b -p 0
