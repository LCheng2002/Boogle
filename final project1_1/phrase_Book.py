import requests
import json
import numpy as np

import sqlite3
from requests.exceptions import RequestException

import re
import os


def push_to_DB(product_id,title,price,publisher,author,url,src):
    connect = sqlite3.connect('./jingdong_book.db')
    cursor = connect.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jingdong_book(
            id INTEGER PRIMARY KEY,
            product_id TEXT,
            title TEXT,     
            price TEXT,
            publisher TEXT,
            author TEXT,
            url TEXT,
            src TEXT     
        );
    """)

    cursor.execute("""INSERT INTO jingdong_book (product_id,title,price,publisher,author,url,src)VALUES (?,?,?,?,?,?,?);""",[product_id,title,price,publisher,author,url,src])

    connect.commit()

    cursor.close()
    connect.close()

ID_list = np.array([])
for index in range(53):
    index_in_txt = 1
    a = "./first/{}/{}_{}.txt".format(index,index, index_in_txt)
    reg= re.compile(r"(?<=/)[0-9]*(?=\.)") 
    while os.path.exists("./first/{}/{}_{}.txt".format(index,index, index_in_txt)):
        file = open("./first/{}/{}_{}.txt".format(index,index, index_in_txt),'r',encoding='utf-8')
        while True:
            line = file.readline()
            if line:
                try:
                    title, price, publisher, author, url, src = line.split()
                    product_id = reg.findall(url)[0]
                    push_to_DB(product_id=product_id,title=title,price=price,publisher=publisher,author=author,url=url,src=src)
                    ID_list = np.append(ID_list,product_id)
                except:
                    continue
            else:
                break
        file.close()
        index_in_txt += 1

np.save("ID_list.npy",ID_list)
