import requests
import json

base_url = "http://localhost:5000"
session = requests.Session()

# Test 1: Check if server is running
try:
    response = session.get(f"{base_url}/api/check-auth")
    print("="*60)
    print("SERVER STATUS CHECK")
    print("="*60)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
except Exception as e:
    print(f"ERROR: Server not responding - {e}")
    print("Please start the Flask server with: python app.py")
    exit(1)

# Test 2: Sign in as user 1 (Rahul Kadu)
print("="*60)
print("TESTING SIGN IN")
print("="*60)

signin_data = {
    "username": "Rahul Kadu",
    "password": "test123"
}

signin_response = session.post(f"{base_url}/api/signin", json=signin_data)
print(f"Sign in status: {signin_response.status_code}")
signin_result = signin_response.json()
print(f"Response: {json.dumps(signin_result, indent=2)}")

if signin_result.get('requires_otp'):
    print("\nOTP Required. Please check console/email for OTP.")
    otp = input("Enter OTP: ")
    
    otp_response = session.post(f"{base_url}/api/verify-otp", json={"otp": otp})
    print(f"OTP verification status: {otp_response.status_code}")
    print(f"Response: {json.dumps(otp_response.json(), indent=2)}")

# Test 3: Check authentication
print("\n" + "="*60)
print("AUTHENTICATION CHECK")
print("="*60)

auth_check = session.get(f"{base_url}/api/check-auth")
auth_data = auth_check.json()
print(f"Authenticated: {auth_data.get('authenticated')}")
if auth_data.get('authenticated'):
    print(f"User: {auth_data.get('user')}")

# Test 4: Fetch history
print("\n" + "="*60)
print("TESTING HISTORY ENDPOINT")
print("="*60)

history_response = session.get(f"{base_url}/history")
print(f"History status: {history_response.status_code}")
history_data = history_response.json()

if isinstance(history_data, list):
    print(f"Number of predictions returned: {len(history_data)}")
    print("\nFirst 3 predictions:")
    for pred in history_data[:3]:
        print(f"  - ID {pred['id']}: {pred['brand']} - Rs {pred['predicted_price']:.2f}")
        print(f"    RAM: {pred['ram_size']}GB, Storage: {pred['storage_capacity']}GB")
else:
    print(f"Response: {json.dumps(history_data, indent=2)}")

print("\n" + "="*60)
