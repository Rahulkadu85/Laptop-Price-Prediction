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

# For each table, show structure
for table in tables:
    table_name = table[0]
    print(f"\nStructure of {table_name}:")
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]}) - Not Null: {bool(col[3])} - PK: {bool(col[5])}")

conn.close()