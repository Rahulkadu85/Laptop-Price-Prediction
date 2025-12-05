import sqlite3

conn = sqlite3.connect('laptop_price.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

# Check prediction table
cursor.execute("SELECT COUNT(*) FROM prediction")
count = cursor.fetchone()[0]
print(f"\nTotal predictions in database: {count}")

# Get recent predictions
cursor.execute("SELECT * FROM prediction ORDER BY id DESC LIMIT 5")
predictions = cursor.fetchall()
print("\nRecent predictions:")
for row in predictions:
    print(row)

# Check users table
cursor.execute("SELECT COUNT(*) FROM user")
user_count = cursor.fetchone()[0]
print(f"\nTotal users: {user_count}")

# Get users
cursor.execute("SELECT id, username, email FROM user")
users = cursor.fetchall()
print("\nUsers:")
for user in users:
    print(user)

conn.close()
