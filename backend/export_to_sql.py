import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'laptop_price.db')
sql_dump_path = os.path.join(base_dir, 'laptop_price_dump.sql')

def export_db_to_sql():
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    with open(sql_dump_path, 'w', encoding='utf-8') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    
    conn.close()
    print(f"Successfully exported database to: {sql_dump_path}")

if __name__ == "__main__":
    export_db_to_sql()
