import os
import sqlite3

DB_PATH = "images.db"
BASE_DIR = os.path.join("static", "images")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS images")
cursor.execute("""
    CREATE TABLE images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        file_path TEXT NOT NULL
    )
""")

for category in os.listdir(BASE_DIR):
    category_path = os.path.join(BASE_DIR, category)
    if not os.path.isdir(category_path):
        continue

    for file in os.listdir(category_path):
        file_path = os.path.join(category_path, file).replace("\\", "/")
        cursor.execute(
            "INSERT INTO images (category, file_path) VALUES (?, ?)",
            (category, file_path)
        )

conn.commit()
conn.close()

print("Database created succssfully.")