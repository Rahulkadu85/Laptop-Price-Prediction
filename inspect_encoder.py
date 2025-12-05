import pickle
import os

base_dir = os.getcwd()
encoder_path = os.path.join(base_dir, 'backend', 'encoder.pkl')

try:
    with open(encoder_path, 'rb') as f:
        encoder = pickle.load(f)
    print("Brands:", list(encoder.classes_))
except Exception as e:
    print(f"Error: {e}")
