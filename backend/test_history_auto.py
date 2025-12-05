
import requests
import json
import sqlite3
import time
import os

BASE_URL = "http://localhost:5000"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'laptop_price.db')

def get_latest_otp(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT otp_code FROM otp WHERE user_id = ? AND is_verified = 0 ORDER BY id DESC LIMIT 1", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def test_history_auto():
    session = requests.Session()
    
    print(f"Testing against {BASE_URL}")
    
    # 1. Sign in
    print("\n1. Signing in...")
    signin_data = {
        "username": "Rahul Kadu",
        "password": "password123" # Assuming this is the password based on previous context or I'll try to reset it if it fails
    }
    
    # Actually, I don't know the password for sure. 
    # But I can create a new user to be safe.
    username = f"test_user_{int(time.time())}"
    password = "password123"
    email = f"{username}@example.com"
    
    print(f"Creating new user: {username}")
    signup_res = session.post(f"{BASE_URL}/api/signup", json={
        "username": username,
        "email": email,
        "password": password
    })
    
    if signup_res.status_code != 201:
        print(f"Signup failed: {signup_res.text}")
        # If signup fails, maybe try to login with known user?
        # But I don't know the password for 'Rahul Kadu'.
        # Let's assume signup works.
        return

    user_data = signup_res.json()['user']
    user_id = user_data['id']
    print(f"User created with ID: {user_id}")
    
    # 2. Sign in (Trigger OTP)
    print("\n2. Signing in to trigger OTP...")
    signin_res = session.post(f"{BASE_URL}/api/signin", json={
        "username": username,
        "password": password
    })
    
    if signin_res.status_code != 200:
        print(f"Signin failed: {signin_res.text}")
        return
        
    signin_json = signin_res.json()
    if not signin_json.get('requires_otp'):
        print("OTP not required? That's unexpected given the code.")
    
    # 3. Get OTP from DB
    print("\n3. Fetching OTP from database...")
    time.sleep(1) # Wait a bit for DB to update
    otp_code = get_latest_otp(user_id)
    print(f"OTP Code found: {otp_code}")
    
    if not otp_code:
        print("Failed to find OTP in database")
        return

    # 4. Verify OTP
    print("\n4. Verifying OTP...")
    verify_res = session.post(f"{BASE_URL}/api/verify-otp", json={
        "otp": otp_code
    })
    
    if verify_res.status_code != 200:
        print(f"OTP verification failed: {verify_res.text}")
        return
        
    print("Login successful!")
    
    # 5. Make a prediction
    print("\n5. Making a prediction...")
    pred_data = {
        "brand": "HP",
        "processor_speed": 2.5,
        "ram_size": 8,
        "storage_capacity": 512,
        "screen_size": 15.6,
        "weight": 1.8
    }
    
    pred_res = session.post(f"{BASE_URL}/predict", json=pred_data)
    if pred_res.status_code != 200:
        print(f"Prediction failed: {pred_res.text}")
        return
        
    print(f"Prediction result: {pred_res.json()}")
    
    # 6. Fetch History
    print("\n6. Fetching History...")
    history_res = session.get(f"{BASE_URL}/history")
    
    if history_res.status_code != 200:
        print(f"History fetch failed: {history_res.text}")
        return
        
    history_data = history_res.json()
    print(f"History data: {history_data}")
    
    if len(history_data) > 0:
        print("SUCCESS: History is being returned correctly.")
    else:
        print("FAILURE: History is empty.")

if __name__ == "__main__":
    test_history_auto()
