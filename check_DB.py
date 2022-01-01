import sqlite3
from sqlite3.dbapi2 import Time
import time

def check_DB(product_id):
    connect = sqlite3.connect('./jingdong_comment.db')
    cursor = connect.cursor()

    # sql = "select name,comment from jingdong_comment where jingdong_comment.product_id = {}".format(product_id)
    sql = "select product_id,name,comment from jingdong_comment where jingdong_comment.product_id = {}".format(product_id)
    cursor.execute(sql)
    print(cursor.fetchall())

    cursor.close()
    connect.close()


check_DB('13311218')
