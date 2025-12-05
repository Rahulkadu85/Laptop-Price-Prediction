
from app import app, db, User, Prediction

with app.app_context():
    print("Users:")
    users = User.query.all()
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}, Email: {u.email}")

    print("\nPredictions:")
    predictions = Prediction.query.all()
    for p in predictions:
        print(f"ID: {p.id}, UserID: {p.user_id}, Brand: {p.brand}, Price: {p.predicted_price}")
