import requests
import json

# Create a session to maintain cookies
session = requests.Session()

# Let's sign up a new user
signup_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
}

print("Signing up...")
signup_response = session.post("http://localhost:5000/api/signup", json=signup_data)
print(f"Sign up status: {signup_response.status_code}")
print(f"Sign up response: {signup_response.json()}")

if signup_response.status_code == 201:
    print("\nUser created successfully!")
    
    # Now let's make a prediction
    prediction_data = {
        "brand": "HP",
        "processor_speed": 2.5,
        "ram_size": 8,
        "storage_capacity": 512,
        "screen_size": 15.6,
        "weight": 2.0
    }
    
    print("\nMaking a prediction...")
    pred_response = session.post("http://localhost:5000/predict", json=prediction_data)
    print(f"Prediction status: {pred_response.status_code}")
    print(f"Prediction response: {pred_response.json()}")
    
    # Now let's check the history
    print("\nChecking history...")
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
else:
    print("\nFailed to create user")