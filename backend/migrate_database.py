"""
Script to migrate the database schema by adding the missing user_id column.
This uses raw SQL to alter the table without deleting existing data.
"""
import sqlite3
import os

# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'laptop_price.db')

print(f"Looking for database at: {db_path}")

if not os.path.exists(db_path):
    print("Database doesn't exist. It will be created when you run the Flask app.")
    exit(0)

try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if prediction table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prediction'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Prediction table doesn't exist. It will be created when you run the Flask app.")
        conn.close()
        exit(0)
    
    # Check existing columns
    cursor.execute("PRAGMA table_info(prediction)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print(f"Existing columns in prediction table: {column_names}")
    
    if 'user_id' in column_names:
        print("✓ user_id column already exists! No migration needed.")
        conn.close()
        exit(0)
    
    print("\nStarting migration...")
    
    # Begin transaction
    cursor.execute("BEGIN TRANSACTION")
    
    # Rename old table
    cursor.execute("ALTER TABLE prediction RENAME TO prediction_old")
    print("✓ Renamed old table to prediction_old")
    
    # Create new table with correct schema
    cursor.execute("""
        CREATE TABLE prediction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            brand VARCHAR(50),
            processor_speed FLOAT,
            ram_size INTEGER,
            storage_capacity INTEGER,
            screen_size FLOAT,
            weight FLOAT,
            predicted_price FLOAT,
            created_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    """)
    print("✓ Created new prediction table with user_id column")
    
    # Check if we need to create a default user
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        # Create a default user for old predictions
        cursor.execute("""
            INSERT INTO user (username, email, password_hash, created_at)
            VALUES ('default_user', 'default@example.com', 'pbkdf2:sha256:600000$default', datetime('now'))
        """)
        default_user_id = cursor.lastrowid
        print(f"✓ Created default user with ID {default_user_id} for old predictions")
    else:
        # Use the first user
        cursor.execute("SELECT id FROM user LIMIT 1")
        default_user_id = cursor.fetchone()[0]
        print(f"✓ Using existing user with ID {default_user_id} for old predictions")
    
    # Check if old table has created_at column
    cursor.execute("PRAGMA table_info(prediction_old)")
    old_columns = cursor.fetchall()
    old_column_names = [col[1] for col in old_columns]
    has_created_at = 'created_at' in old_column_names
    
    # Copy data from old table to new table with default user_id
    if has_created_at:
        cursor.execute(f"""
            INSERT INTO prediction (id, user_id, brand, processor_speed, ram_size, 
                                   storage_capacity, screen_size, weight, predicted_price, created_at)
            SELECT id, {default_user_id}, brand, processor_speed, ram_size, 
                   storage_capacity, screen_size, weight, predicted_price, created_at
            FROM prediction_old
        """)
    else:
        cursor.execute(f"""
            INSERT INTO prediction (id, user_id, brand, processor_speed, ram_size, 
                                   storage_capacity, screen_size, weight, predicted_price, created_at)
            SELECT id, {default_user_id}, brand, processor_speed, ram_size, 
                   storage_capacity, screen_size, weight, predicted_price, datetime('now')
            FROM prediction_old
        """)
    
    rows_migrated = cursor.rowcount
    print(f"✓ Migrated {rows_migrated} predictions to new table")
    
    # Drop old table
    cursor.execute("DROP TABLE prediction_old")
    print("✓ Dropped old table")
    
    # Commit transaction
    conn.commit()
    print("\n✓ Migration completed successfully!")
    print(f"  - All {rows_migrated} existing predictions have been assigned to user_id {default_user_id}")
    print("  - New predictions will use the correct user_id from sessions")
    
except sqlite3.Error as e:
    print(f"✗ Database error: {e}")
    if conn:
        conn.rollback()
        print("✗ Changes rolled back")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if conn:
        conn.close()
        print("\nDatabase connection closed.")
