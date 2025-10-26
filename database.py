# database.py
import sqlite3
import os
import string
import random

DB_PATH = "urls.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def save_url(original_url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        short_code = generate_short_code()
        try:
            cursor.execute(
                "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
                (short_code, original_url)
            )
            conn.commit()
            break
        except sqlite3.IntegrityError:
            # Short code already exists—try again
            continue
    conn.close()
    return short_code

def get_original_url(short_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None
