# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, jieba,re
from push_to_history import push_to_history
import sqlite3

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

def get_comment_DB(product_id):
    connect = sqlite3.connect('./jingdong_comment.db')
    cursor = connect.cursor()

    # sql = "select product_id from jingdong_comment"
    sql = "select name,comment from jingdong_comment where jingdong_comment.product_id = {}".format(product_id)
    cursor.execute(sql)
    comments = cursor.fetchall() 

    cursor.close()
    connect.close()

    return comments

def run(searcher, analyzer, search_content):
    # while True:
    # print()
    # print ("Hit enter with no input to quit.")
    # command = input("Query:")
    command = search_content
    seg_list = jieba.cut(command)
    command = (" ".join(seg_list))
    if command == '':
        return

    # print()
    # print ("Searching for:", command)
    query = QueryParser("title", analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    # print ("%s total matching documents." % len(scoreDocs))
    Matching_num = len(scoreDocs)
    Searching_result = []
    
    for i, scoreDoc in enumerate(scoreDocs):
        doc = searcher.doc(scoreDoc.doc)
        Match = {}
        Match['title'] = doc.get("title")
        Match['author'] = doc.get("author")
        Match['price'] = doc.get("price")
        Match['publisher'] = doc.get("publisher")
        Match['url'] = doc.get("url")
        Match['src'] = doc.get("src")

        product_id = doc.get("product_id")
        comments = get_comment_DB(product_id)
        Match['comments'] = comments

        Searching_result.append(Match)
        # print ('title:', doc.get("title"), \
        #         '\nprice:', doc.get("price"), \
        #         '\npublisher:', doc.get("publisher"), \
        #         "\nauthor:",doc.get("author"),\
        #         '\nurl:',doc.get("url"), '\n')
            # print 'explain:', searcher.explain(query, scoreDoc.doc)
    # push_to_history(search_content)
    return Matching_num, Searching_result


def Page_search(search_content):
    STORE_DIR = "index"
    try:
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    except:
        vm_env = lucene.getVMEnv()
        vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()#Version.LUCENE_CURRENT)
    Matching_num, Searching_result = run(searcher, analyzer, search_content)
    return Matching_num, Searching_result

if __name__ == "__main__":
    print(Page_search("小王子"))
# if __name__ == '__main__':
#     STORE_DIR = "index"
#     lucene.initVM(vmargs=['-Djava.awt.headless=true'])
#     print ('lucene', lucene.VERSION)
#     #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#     directory = SimpleFSDirectory(File(STORE_DIR).toPath())
#     searcher = IndexSearcher(DirectoryReader.open(directory))
#     analyzer = StandardAnalyzer()#Version.LUCENE_CURRENT)
#     run(searcher, analyzer)
#     del searcher