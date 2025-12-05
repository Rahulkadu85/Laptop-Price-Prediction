import requests
import json

# Create a session to maintain cookies
session = requests.Session()

# Let's try to sign up
signup_data = {
    "username": "Rahul Kadu",
    "email": "rahulkadu191@gmail.com",
    "password": "test123"
}

print("Signing up...")
signup_response = session.post("http://localhost:5000/api/signup", json=signup_data)
print(f"Sign up status: {signup_response.status_code}")
print(f"Sign up response: {signup_response.json()}")