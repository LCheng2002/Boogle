import sqlite3
import time

def push_to_history(content):
    connect = sqlite3.connect('./history.db')
    cursor = connect.cursor()
    Time = time.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY,
            searching_content TEXT,
            Time TEXT
        );
    """)

    cursor.execute("""INSERT INTO history (searching_content,Time) VALUES (?,?);""",[content,Time])

    connect.commit()

    cursor.close()
    connect.close()

push_to_history("足球")