@echo off
python build.py -m LPC1768 -tARM -v
python project.py -m LPC1768 -i uvision -b -p 0
