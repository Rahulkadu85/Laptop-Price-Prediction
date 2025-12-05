import requests

# Test the history endpoint directly
response = requests.get("http://localhost:5000/history")
print(f"Status Code: {response.status_code}")
print(f"Response Headers: {response.headers}")
try:
    data = response.json()
    print(f"Response Data: {data}")
except:
    print(f"Raw Response: {response.text}")