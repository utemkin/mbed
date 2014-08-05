@echo off
python build.py -m LPC1768_MINI_DK2 -tARM -v
python project.py -m LPC1768_MINI_DK2 -i uvision -b -p 0
