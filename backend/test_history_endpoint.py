import requests
import json

# Create a session to maintain cookies
session = requests.Session()

# First, let's sign in
signin_data = {
    "username": "Rahul Kadu",
    "password": "test123"
}

print("Signing in...")
signin_response = session.post("http://localhost:5000/api/signin", json=signin_data)
print(f"Sign in status: {signin_response.status_code}")
print(f"Sign in response: {signin_response.json()}")

# If OTP is required, we'll need to handle it
if signin_response.status_code == 200 and signin_response.json().get('requires_otp'):
    print("\nOTP required. Checking console for OTP code...")
    # In a real test, you would get the OTP from the console output
    # For now, let's assume we can proceed without OTP verification for testing
    
# Now let's check if we're authenticated
auth_check = session.get("http://localhost:5000/api/check-auth")
print(f"\nAuth check status: {auth_check.status_code}")
print(f"Auth check response: {auth_check.json()}")

# Now let's try to fetch history
print("\nFetching history...")
history_response = session.get("http://localhost:5000/history")
print(f"History status: {history_response.status_code}")
try:
    history_data = history_response.json()
    print(f"History data type: {type(history_data)}")
    if isinstance(history_data, list):
        print(f"Number of history items: {len(history_data)}")
        if history_data:
            print("First item:", json.dumps(history_data[0], indent=2))
    else:
        print(f"History data: {json.dumps(history_data, indent=2)}")
except Exception as e:
    print(f"Error parsing history response: {e}")
    print(f"Raw response: {history_response.text}")