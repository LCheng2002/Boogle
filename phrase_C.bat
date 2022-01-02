@echo off
cd C:\Users\cheng\Desktop\Boogle

title auto pull
git pull origin main

start C:\ProgramData\Anaconda3\python.exe .\phrase_comment.py

title auto commit
git add .
git commit -m main
git push origin main
exit

