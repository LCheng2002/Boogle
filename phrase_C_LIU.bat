@echo off
cd C:\Users\86147\Documents\Github\Boogle

title auto pull
git pull origin main

C:\python.exe .\phrase_comment.py

title auto commit
git add .
git commit -m main
git push origin main
exit

