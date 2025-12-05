"""
Migration script to add OTP functionality
- Adds phone column to user table
- Creates OTP table
"""
import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'laptop_price.db')

print("=" * 70)
print("OTP FEATURE MIGRATION")
print("=" * 70)

if not os.path.exists(db_path):
    print("\n❌ Database not found. Run the Flask app first to create it.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if phone column exists
    cursor.execute("PRAGMA table_info(user)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'phone' not in columns:
        print("\n📱 Adding phone column to user table...")
        cursor.execute("ALTER TABLE user ADD COLUMN phone VARCHAR(15)")
        print("✓ Phone column added")
    else:
        print("\n✓ Phone column already exists")
    
    # Check if OTP table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='otp'")
    if not cursor.fetchone():
        print("\n🔐 Creating OTP table...")
        cursor.execute("""
            CREATE TABLE otp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                otp_code VARCHAR(6) NOT NULL,
                otp_type VARCHAR(10) NOT NULL,
                created_at DATETIME NOT NULL,
                expires_at DATETIME NOT NULL,
                is_verified BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES user(id)
            )
        """)
        print("✓ OTP table created")
    else:
        print("\n✓ OTP table already exists")
    
    conn.commit()
    
    print("\n" + "=" * 70)
    print("✓ MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Configure email settings in otp_config.py")
    print("2. Restart your Flask application")
    print("3. Users can now add phone numbers during signup")
    print("4. OTP will be sent on login to email (and SMS if phone provided)")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    conn.rollback()
    import traceback
    traceback.print_exc()
finally:
    conn.close()
