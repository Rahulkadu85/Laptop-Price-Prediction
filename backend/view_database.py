"""
Database Viewer - Shows database contents in readable text format
This allows you to VIEW the database without opening the binary .db file
"""
import sqlite3
import os
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'instance', 'laptop_price.db')

def print_separator(char="=", length=100):
    print(char * length)

def print_section(title):
    print("\n")
    print_separator("=")
    print(f"  {title}")
    print_separator("=")

def view_database():
    """Display all database contents in a readable format"""
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        print(f"   Looking for: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Database info
    print_separator("=")
    print("DATABASE VIEWER - Laptop Price Prediction")
    print_separator("=")
    print(f"Database: {db_path}")
    print(f"Size: {os.path.getsize(db_path) / 1024:.2f} KB")
    print(f"Viewed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # ========== USERS TABLE ==========
    print_section("USERS TABLE")
    cursor.execute('SELECT COUNT(*) FROM user')
    user_count = cursor.fetchone()[0]
    print(f"\nTotal Users: {user_count}\n")
    
    if user_count > 0:
        cursor.execute('SELECT id, username, email, created_at FROM user ORDER BY id')
        users = cursor.fetchall()
        
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Created At':<25}")
        print("-" * 100)
        for user in users:
            print(f"{user[0]:<5} {user[1]:<20} {user[2]:<30} {user[3]:<25}")
    
    # ========== PREDICTIONS TABLE ==========
    print_section("PREDICTIONS TABLE")
    cursor.execute('SELECT COUNT(*) FROM prediction')
    pred_count = cursor.fetchone()[0]
    print(f"\nTotal Predictions: {pred_count}\n")
    
    if pred_count > 0:
        # Summary by brand
        cursor.execute('''
            SELECT brand, COUNT(*) as count, 
                   AVG(predicted_price) as avg_price,
                   MIN(predicted_price) as min_price,
                   MAX(predicted_price) as max_price
            FROM prediction 
            GROUP BY brand 
            ORDER BY count DESC
        ''')
        brand_stats = cursor.fetchall()
        
        print("Summary by Brand:")
        print(f"\n{'Brand':<15} {'Count':<10} {'Avg Price':<15} {'Min Price':<15} {'Max Price':<15}")
        print("-" * 100)
        for stat in brand_stats:
            print(f"{stat[0]:<15} {stat[1]:<10} {stat[2]:>12,.2f}  {stat[3]:>12,.2f}  {stat[4]:>12,.2f}")
        
        # Recent predictions (detailed view)
        print("\n\nRecent Predictions (Last 20):")
        cursor.execute('''
            SELECT p.id, p.user_id, u.username, p.brand, 
                   p.processor_speed, p.ram_size, p.storage_capacity,
                   p.screen_size, p.weight, p.predicted_price, p.created_at
            FROM prediction p
            JOIN user u ON p.user_id = u.id
            ORDER BY p.id DESC
            LIMIT 20
        ''')
        predictions = cursor.fetchall()
        
        print(f"\n{'ID':<5} {'User':<15} {'Brand':<10} {'CPU':<6} {'RAM':<6} {'Storage':<8} {'Screen':<7} {'Weight':<7} {'Price':<15} {'Date':<20}")
        print("-" * 120)
        
        for pred in predictions:
            pid, uid, username, brand, cpu, ram, storage, screen, weight, price, date = pred
            print(f"{pid:<5} {username:<15} {brand:<10} {cpu:<6.1f} {ram:<6.0f} {storage:<8.0f} {screen:<7.1f} {weight:<7.1f} {price:>12,.2f}  {date:<20}")
        
        # All predictions (compact view)
        if pred_count > 20:
            print(f"\n\nAll Predictions (Compact View):")
            cursor.execute('''
                SELECT p.id, u.username, p.brand, p.predicted_price, p.created_at
                FROM prediction p
                JOIN user u ON p.user_id = u.id
                ORDER BY p.id DESC
            ''')
            all_preds = cursor.fetchall()
            
            print(f"\n{'ID':<5} {'User':<20} {'Brand':<12} {'Predicted Price':<18} {'Date':<25}")
            print("-" * 100)
            for pred in all_preds:
                print(f"{pred[0]:<5} {pred[1]:<20} {pred[2]:<12} {pred[3]:>14,.2f}   {pred[4]:<25}")
    
    # ========== DATABASE STATISTICS ==========
    print_section("DATABASE STATISTICS")
    
    # Date range
    cursor.execute('SELECT MIN(created_at), MAX(created_at) FROM prediction')
    date_range = cursor.fetchone()
    print(f"\nPrediction Date Range:")
    print(f"  First: {date_range[0]}")
    print(f"  Last:  {date_range[1]}")
    
    # User activity
    cursor.execute('''
        SELECT u.username, COUNT(p.id) as prediction_count
        FROM user u
        LEFT JOIN prediction p ON u.id = p.user_id
        GROUP BY u.id, u.username
        ORDER BY prediction_count DESC
    ''')
    user_activity = cursor.fetchall()
    
    print(f"\n\nUser Activity:")
    print(f"{'Username':<20} {'Predictions':<15}")
    print("-" * 40)
    for activity in user_activity:
        print(f"{activity[0]:<20} {activity[1]:<15}")
    
    conn.close()
    
    print_separator("=")
    print("\nDatabase view complete!")
    print("\nNote: This is a READ-ONLY view. To modify data, use the Flask application.")
    print_separator("=")

if __name__ == '__main__':
    view_database()
