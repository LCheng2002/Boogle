# SJTU EE208

import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
import time

from bs4 import BeautifulSoup

def get_all_links():
    file = open("booksort.txt", 'r', encoding='utf-8')
    content = file.read() # urllib.request.urlopen(req,timeout=3).read().decode("utf-8")
    links = []
    soup = BeautifulSoup(content,"html.parser")
    for i in soup.findAll('div',{'class':"mc"}):
        for j in range(len(i.contents[0].contents)//2):
            file = open("first/{}.txt".format(j), 'w', encoding='utf-8')
            for k in i.contents[0].contents[2*j+1].contents:
                tail = k.contents[0].get("href","").split('/')[-1]
                tail = tail.split('.')[0]
                href = "https://list.jd.com/list.html?cat="+",".join(tail.split('-'))
                file.write(href+'\t'+k.contents[0].string+'\n')
            file.close()

start = time.time()
get_all_links()
end = time.time()
print(end - start)
