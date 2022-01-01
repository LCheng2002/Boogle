@echo off
title 
C:\Program Files\Git\bin\git.exe pull origin master

C:\ProgramData\Anaconda3\python.exe phrase_comment.py

set /p commit=commit:
title auto commit
C:\Program Files\Git\bin\git.exe add -A
C:\Program Files\Git\bin\git.exe commit -m %commit%
C:\Program Files\Git\bin\git.exe push origin main
exit

