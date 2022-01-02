# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime

# from java.io import File
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        # store = SimpleFSDirectory(File(storeDir).toPath())
        store = SimpleFSDirectory(Paths.get(storeDir))
        analyzer = StandardAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(True)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)  # Not Indexed
        
        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(False)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)  # Indexes documents, frequencies and positions.
        
        # t3 = FieldType() #t3 is used to index titles
        # t3.setStored(True)
        # t3.setTokenized(True)
        # t3.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        reg= re.compile(r"(?<=/)[0-9]*(?=\.)")

        for i in range(53):
            for rt, ds, fs in os.walk(root+f'/{i}'):
                for f in fs:
                    indextxt = open(rt+"/"+f, 'r')
                    while True:
                        t = indextxt.readline()
                        if (len(t) == 0):
                            indextxt.close()
                            break
                        t = t.split()
                        title = t[0]
                        price = t[1]
                        publisher = t[2]
                        author = t[3]
                        url = t[4]
                        src = t[5]

                        print(url)
                        product_id = reg.findall(url)[0]
                        # filename = t[1]
                        # URL = t[0]
        # for root, dirnames, filenames in os.walk(root):
        #     for filename in filenames:
                        print("adding",i, title)
                        doc = Document()
                        doc.add(Field("title", title, t1))
                        doc.add(Field("price", price, t2))
                        doc.add(Field("publisher", publisher, t2))
                        doc.add(Field("author",author, t1))
                        doc.add(Field("url", url, t2))
                        doc.add(Field("src",src, t2))
                        doc.add(Field("product_id",product_id,t2))
                        writer.addDocument(doc)
                    indextxt.close()

if __name__ == '__main__':
    lucene.initVM()#vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    # import ipdb; ipdb.set_trace()
    start = datetime.now()
    try:
        IndexFiles('first', "index")
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e