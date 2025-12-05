"""
Script to fix the database schema by recreating it with the correct structure.
This will delete the old database and create a new one with user_id column.
"""
import os
import sys

# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'laptop_price.db')

print(f"Looking for database at: {db_path}")

# Check if database exists
if os.path.exists(db_path):
    print(f"Found existing database. Deleting it...")
    try:
        os.remove(db_path)
        print("✓ Old database deleted successfully!")
    except Exception as e:
        print(f"✗ Error deleting database: {e}")
        sys.exit(1)
else:
    print("No existing database found.")

# Now import Flask app to create new database with correct schema
print("\nCreating new database with correct schema...")
try:
    from app import app, db
    
    with app.app_context():
        db.create_all()
        print("✓ New database created successfully with correct schema!")
        print("\nDatabase structure includes:")
        print("  - User table (id, username, email, password_hash, created_at)")
        print("  - Prediction table (id, user_id, brand, processor_speed, ram_size,")
        print("                      storage_capacity, screen_size, weight, predicted_price, created_at)")
        print("\n✓ Fix completed! You can now run your Flask application.")
        
except Exception as e:
    print(f"✗ Error creating new database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
