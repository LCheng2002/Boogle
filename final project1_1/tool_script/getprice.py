import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
import time

from bs4 import BeautifulSoup

def getprice(index,index_in_txt,url):
    if not os.path.exists("./first/{}".format(index)):
        os.mkdir("./first/{}".format(index))
    if not os.path.exists("./first/{}/{}_{}.txt".format(index,index,index_in_txt)):
        file = open("./first/{}/{}_{}.txt".format(index,index,index_in_txt), 'w', encoding='utf-8')
    else:
        return
    req = urllib.request.Request(url)
    req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0")
    content = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(content)
    for i in soup.findAll('div',{'class':"gl-i-wrap"}):
        try:
            information = ''.join(i.contents[5].contents[1].contents[1].string.split())+'\t'+ \
                        i.contents[3].contents[1].contents[1].string+i.contents[3].contents[1].contents[2].string+'\t'+ \
                        i.contents[7].contents[3].contents[1].string+'\t'+ \
                        i.contents[7].contents[1].contents[1].string+ '\t'+ \
                        "https:"+i.contents[5].contents[1].get("href",'')+'\n'
            file.write(information)
        except:
            continue
    file.close()

for index in range(43,44):
    index_in_txt = 0
    first = open("./first/{}.txt".format(index),'r',encoding='utf-8')
    while True:
        line = first.readline()
        if line:
            url = line.split()[0]
            index_in_txt += 1
            getprice(index,index_in_txt,url)
        else:
            break
    first.close()