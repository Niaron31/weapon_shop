import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL
                   )""")
    
    conn.commit()
    conn.close()

def init_db_info():
    conn = sqlite3.connect("info.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS info(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   owner_name TEXT NOT NULL,
                   name TEXT NOT NULL,
                   type TEXT NOT NULL,
                   price TEXT NOT NULL,
                   image_path TEXT
                   )
    """)
    conn.commit()
    conn.close()