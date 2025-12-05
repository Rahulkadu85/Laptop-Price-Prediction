import pickle
from sklearn.preprocessing import LabelEncoder
import os

# Define all laptop brands you want to support
brands = ['HP', 'Asus', 'Acer', 'Lenovo', 'Dell']

# Create and fit the encoder
encoder = LabelEncoder()
encoder.fit(brands)

# Save the updated encoder
base_dir = os.path.dirname(os.path.abspath(__file__))
encoder_path = os.path.join(base_dir, 'encoder.pkl')

with open(encoder_path, 'wb') as f:
    pickle.dump(encoder, f)

print("Encoder updated successfully!")
print(f"Available brands: {list(encoder.classes_)}")
