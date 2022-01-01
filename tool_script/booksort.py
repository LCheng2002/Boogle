# SJTU EE208

import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
import time
# import threading
# import queue
from bs4 import BeautifulSoup
# from BloomFilter import BloomFilter

# def valid_filename(s):
#     valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
#     s = ''.join(c for c in s if c in valid_chars)
#     return s

# def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
#     index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
#     folder = 'html'  # 存放网页的文件夹
#     filename = valid_filename(page)  # 将网址变成合法的文件名
#     index = open(index_filename, 'a')
#     index.write(page + '\t' + filename + '\n')
#     index.close()
    # if not os.path.exists(folder):  # 如果文件夹不存在则新建
    #     os.mkdir(folder)
    # f = open(os.path.join(folder, filename), 'w')
    # f.write(content)  # 将网页存入文件
    # f.close()

# def get_page(page):
#     try:
#         content = urllib.request.urlopen(page,timeout=3).read()# This function will not be execute more than 3 seconds.
#     except:
#         content=''
#     return content


def get_all_links():
    # url = "https://book.jd.com/"
    # req = urllib.request.Request("https://book.jd.com/")
    # req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0")	
    file = open("booksort.txt", 'r', encoding='utf-8')
    content = file.read() # urllib.request.urlopen(req,timeout=3).read().decode("utf-8")
    # file = open("book", 'w', encoding='utf-8')
    # file.write(content)
    links = []
    # pattern = re.compile('(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')')
    # links = pattern.findall(content)
    soup = BeautifulSoup(content,"html.parser")
    # print(soup)
    index_filename = 'all_book.txt'  # index.txt中每行是'网址 对应的文件名'
    index = open(index_filename, 'a')
    for i in soup.findAll('div',{'class':"mc"}):
        # print(len(i.contents[0].contents))
        for j in range(len(i.contents[0].contents)//2):
            # print(i.contents[0].contents[2*j])
            os.mkdir(str(j))
            index.write(i.contents[0].contents[2*j].contents[0].string+'\t'+"https:"+i.contents[0].contents[2*j].contents[0].get("href","")+'\n')
            print(i.contents[0].contents[2*j+1])
            for k in i.contents[0].contents[2*j+1].contents:
                index.write('\t'+k.contents[0].string+'\t'+"https:"+k.contents[0].get("href","")+'\n')
    # for i in links:
    #     index.write(i[0] + '\t' + i[1] + '\n')
    index.close()

# def working():
#     global count,wrong,max_pages
#     while count < max_pages:
#         page = q.get()
#         if page not in crawled_bloom:
#             content= get_page(page)
#             if content == '':
#                 continue
#             outlinks = get_all_links(content,page)
#             for link in outlinks:
#                 q.put(link)
#             if varLock.acquire():
#                 graph[page] = outlinks
#                 if page not in crawled_bloom:
#                     count += 1
#                     add_page_to_folder(page, content)
#                     crawled_bloom.add(page)
#                     print(page)
#                 varLock.release()
#             q.task_done()

# max_pages = int(sys.argv[1])
start = time.time()
# NUM = 4
# crawled_bloom = BloomFilter(max_pages)
# graph = {}
# varLock = threading.Lock()
# q = queue.Queue()
# count = 0
# q.put('https://www.jd.com')
# for i in range(NUM):
#     t = threading.Thread(target=working)
#     t.setDaemon(True)
#     t.start()
# for i in range(NUM):
#     t.join()
get_all_links()
end = time.time()
print(end - start)
# print(crawled)

#https://blog.csdn.net/m0_46135508/article/details/107241825
#https://blog.csdn.net/qq_34500270/article/details/82899057