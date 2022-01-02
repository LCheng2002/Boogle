@echo off
cd C:\Users\cheng\Desktop\Boogle

git pull origin main

C:\ProgramData\Anaconda3\python.exe .\phrase_comment.py

git add .
git commit -m main
git push origin main
exit

