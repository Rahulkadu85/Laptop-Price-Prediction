from app import db, Prediction, User
import app as app_module

# Push app context
app_module.app.app_context().push()

print("="*60)
print("DATABASE DIAGNOSTIC")
print("="*60)

# Get all users
users = User.query.all()
print(f"\nTotal Users: {len(users)}")
for user in users:
    print(f"  - User ID {user.id}: {user.username} ({user.email})")

# Get all predictions
predictions = Prediction.query.all()
print(f"\nTotal Predictions: {len(predictions)}")

# Group predictions by user
from collections import defaultdict
user_predictions = defaultdict(list)
for pred in predictions:
    user_predictions[pred.user_id].append(pred)

print("\nPredictions by User:")
for user_id, preds in user_predictions.items():
    user = User.query.get(user_id)
    username = user.username if user else "Unknown User"
    print(f"  - User ID {user_id} ({username}): {len(preds)} predictions")
    for pred in preds[:3]:  # Show first 3
        print(f"      > {pred.brand} - Rs {pred.predicted_price:.2f}")
    if len(preds) > 3:
        print(f"      ... and {len(preds)-3} more")

# Check if there are any predictions without a valid user
orphaned = [p for p in predictions if not User.query.get(p.user_id)]
if orphaned:
    print(f"\nWarning: {len(orphaned)} orphaned predictions (user deleted)")
else:
    print("\nAll predictions have valid users")

print("\n" + "="*60)
