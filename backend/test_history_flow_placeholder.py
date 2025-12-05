
import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_history_flow():
    session = requests.Session()
    
    # 1. Login
    print("1. Logging in...")
    login_data = {
        "username": "Rahul Kadu",
        "password": "password123" # I need to know the password. 
        # Wait, I don't know the password. 
        # But I can create a new user and test with that.
    }
    
    # Let's create a new user to be sure
    username = "testuser_history"
    email = "test_history@example.com"
    password = "password123"
    
    print(f"1. Creating user {username}...")
    signup_res = session.post(f"{BASE_URL}/api/signup", json={
        "username": username,
        "email": email,
        "password": password
    })
    
    if signup_res.status_code == 400 and "already exists" in signup_res.text:
        print("User already exists, logging in...")
        # If user exists, we need to login. 
        # But wait, login requires OTP now?
        # Let's check app.py. Yes, /api/signin sends OTP.
        pass
    else:
        print(f"Signup status: {signup_res.status_code}")
        print(f"Signup response: {signup_res.text}")

    # 2. Login (Trigger OTP)
    print("\n2. Logging in (Triggering OTP)...")
    signin_res = session.post(f"{BASE_URL}/api/signin", json={
        "username": username,
        "password": password
    })
    print(f"Signin status: {signin_res.status_code}")
    signin_data = signin_res.json()
    print(f"Signin response: {signin_data}")
    
    if 'requires_otp' in signin_data and signin_data['requires_otp']:
        # We need to get the OTP from the server logs or database.
        # Since I can't easily read the server logs in real-time from here while the server is running in another process (if it was),
        # I will check the database for the OTP.
        
        # Note: I am not running the server myself right now, the user is likely running it or I need to run it.
        # I will assume I need to run the server in the background to test this?
        # Actually, I should probably check if the server is running.
        pass

if __name__ == "__main__":
    print("This script is just a placeholder. I will use a different approach.")
