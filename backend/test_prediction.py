import requests
import json

# Test the prediction endpoint
base_url = "http://localhost:5000"

# First, let's check if we need to login
session = requests.Session()

# Try to check authentication status
auth_check = session.get(f"{base_url}/api/check-auth")
print("Auth check:", auth_check.json())

# If not authenticated, let's sign in
if not auth_check.json().get('authenticated'):
    print("\nNot authenticated. Attempting to sign in...")
    
    # Sign in with existing user
    signin_data = {
        "username": "Rahul Kadu",
        "password": "test123"  # You'll need to use the actual password
    }
    
    signin_response = session.post(f"{base_url}/api/signin", json=signin_data)
    print("Sign in response:", signin_response.json())
    
    if signin_response.json().get('requires_otp'):
        print("\nOTP required. Please check your email/console for the OTP.")
        otp = input("Enter OTP: ")
        
        otp_response = session.post(f"{base_url}/api/verify-otp", json={"otp": otp})
        print("OTP verification:", otp_response.json())

# Now try to make a prediction
print("\n\nAttempting prediction...")
prediction_data = {
    "brand": "HP",
    "processor_speed": 3.5,
    "ram_size": 8,
    "storage_capacity": 512,
    "screen_size": 15.6,
    "weight": 2.0
}

prediction_response = session.post(f"{base_url}/predict", json=prediction_data)
print("Prediction response status:", prediction_response.status_code)
print("Prediction response:", prediction_response.json())

# Check if the prediction was saved
print("\n\nChecking database...")
import sqlite3
conn = sqlite3.connect('laptop_price.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM prediction ORDER BY id DESC LIMIT 1")
latest = cursor.fetchone()
print("Latest prediction in DB:", latest)
conn.close()
