@echo off
cd C:\Users\cheng\Desktop\Boogle

title 
git pull origin main

C:\ProgramData\Anaconda3\python.exe .\phrase_comment.py

title auto commit
git add .
git commit -m main
git push origin main
exit

