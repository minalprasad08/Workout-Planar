import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if tables:
    print("Tables in database:", tables)
else:
    print("No tables found!")

conn.close()

