import sqlite3
import os

# Connect to the database
db_path = 'laptop_price.db'
if not os.path.exists(db_path):
    print(f"Database file {db_path} not found!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

# If no tables found, let's see what's in the database file
if not tables:
    print("\nNo tables found. Let's see what's in the sqlite_master:")
    cursor.execute("SELECT * FROM sqlite_master")
    master_rows = cursor.fetchall()
    for row in master_rows:
        print(row)

conn.close()