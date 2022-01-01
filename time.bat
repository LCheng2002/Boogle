@echo off
title 
git pull origin master

C:\ProgramData\Anaconda3\python.exe phrase_comment.py

title auto commit
git add -A
git commit -m main
git push origin main
exit

