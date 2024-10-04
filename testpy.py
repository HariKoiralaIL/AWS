import sqlite3
import os

try:
    conn = sqlite3.connect('mydatabase.db')
    print("Database opened success")
    conn.close()
except sqlite3.Error as e:
    print(f"Error: {e}")
