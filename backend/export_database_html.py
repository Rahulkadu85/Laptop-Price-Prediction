"""
Export Database to HTML - Creates a viewable HTML file with all database contents
"""
import sqlite3
import os
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'laptop_price.db')
output_path = os.path.join(base_dir, 'database_view.html')

def export_to_html():
    """Export database contents to an HTML file"""
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get data
    cursor.execute('SELECT id, username, email, created_at FROM user ORDER BY id')
    users = cursor.fetchall()
    
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
    
    cursor.execute('''
        SELECT p.id, u.username, p.brand, 
               p.processor_speed, p.ram_size, p.storage_capacity,
               p.screen_size, p.weight, p.predicted_price, p.created_at
        FROM prediction p
        JOIN user u ON p.user_id = u.id
        ORDER BY p.id DESC
    ''')
    predictions = cursor.fetchall()
    
    cursor.execute('SELECT COUNT(*) FROM prediction')
    total_predictions = cursor.fetchone()[0]
    
    conn.close()
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Viewer - Laptop Price Prediction</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        
        h1 {{
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }}
        
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }}
        
        h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        .stat-card {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 10px;
            margin: 10px;
            min-width: 200px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
        }}
        
        .price {{
            color: #28a745;
            font-weight: 600;
        }}
        
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e9ecef;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>💻 Database Viewer</h1>
        <p class="subtitle">Laptop Price Prediction Application</p>
        <p class="subtitle">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <div class="stat-card">
                <div class="stat-label">Total Users</div>
                <div class="stat-value">{len(users)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Predictions</div>
                <div class="stat-value">{total_predictions}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Brands</div>
                <div class="stat-value">{len(brand_stats)}</div>
            </div>
        </div>
        
        <!-- Users Table -->
        <div class="section">
            <h2>👥 Users</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for user in users:
        html += f"""
                    <tr>
                        <td>{user[0]}</td>
                        <td><strong>{user[1]}</strong></td>
                        <td>{user[2]}</td>
                        <td class="timestamp">{user[3]}</td>
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
        
        <!-- Brand Statistics -->
        <div class="section">
            <h2>📊 Predictions by Brand</h2>
            <table>
                <thead>
                    <tr>
                        <th>Brand</th>
                        <th>Count</th>
                        <th>Average Price</th>
                        <th>Min Price</th>
                        <th>Max Price</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for stat in brand_stats:
        html += f"""
                    <tr>
                        <td><strong>{stat[0]}</strong></td>
                        <td>{stat[1]}</td>
                        <td class="price">₹{stat[2]:,.2f}</td>
                        <td class="price">₹{stat[3]:,.2f}</td>
                        <td class="price">₹{stat[4]:,.2f}</td>
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
        
        <!-- All Predictions -->
        <div class="section">
            <h2>📋 All Predictions</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>User</th>
                        <th>Brand</th>
                        <th>CPU (GHz)</th>
                        <th>RAM (GB)</th>
                        <th>Storage (GB)</th>
                        <th>Screen (in)</th>
                        <th>Weight (kg)</th>
                        <th>Predicted Price</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for pred in predictions:
        html += f"""
                    <tr>
                        <td>{pred[0]}</td>
                        <td>{pred[1]}</td>
                        <td><strong>{pred[2]}</strong></td>
                        <td>{pred[3]:.1f}</td>
                        <td>{pred[4]:.0f}</td>
                        <td>{pred[5]:.0f}</td>
                        <td>{pred[6]:.1f}</td>
                        <td>{pred[7]:.1f}</td>
                        <td class="price">₹{pred[8]:,.2f}</td>
                        <td class="timestamp">{pred[9]}</td>
                    </tr>
"""
    
    html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p><strong>Database File:</strong> {db_path}</p>
            <p><strong>Size:</strong> {os.path.getsize(db_path) / 1024:.2f} KB</p>
            <p style="margin-top: 10px;">This is a read-only view. Use the Flask application to modify data.</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("=" * 80)
    print("✓ Database exported to HTML successfully!")
    print("=" * 80)
    print(f"\nFile saved: {output_path}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.2f} KB")
    print(f"\n📂 Open this file in your web browser to view the database!")
    print("\nYou can:")
    print("  1. Double-click the file to open it")
    print("  2. Right-click → Open with → Your web browser")
    print("=" * 80)

if __name__ == '__main__':
    export_to_html()
