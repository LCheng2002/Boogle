@echo off
cd C:\Users\cheng\Desktop\Boogle

title auto pull
git pull origin main

C:\Program Files\Python38\python.exe .\phrase_comment.py

title auto commit
git add .
git commit -m main
git push origin main
exit

