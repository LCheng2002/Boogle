import sqlite3
from sqlite3.dbapi2 import Time
import time

def push_to_history(content):
    connect = sqlite3.connect('./history.db')
    cursor = connect.cursor()
    Time = time.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jingdong_book(
            id INTEGER PRIMARY KEY,
            content TEXT,
            Time TEXT,
        );
    """)

    cursor.execute("""INSERT INTO jingdong_book (searching_content,Time) VALUES (?,?);""",[content,Time])

    connect.commit()

    cursor.close()
    connect.close()
