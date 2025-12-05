"""
Test script to verify predictions are being saved to the database
"""
from app import app, db, Prediction
from datetime import datetime

print("Testing prediction save functionality...\n")

with app.app_context():
    # Count before
    before_count = Prediction.query.count()
    print(f"Predictions in DB before test: {before_count}")
    
    # Create a test prediction
    test_prediction = Prediction(
        user_id=1,
        brand='HP',
        processor_speed=2.5,
        ram_size=8,
        storage_capacity=512,
        screen_size=15.6,
        weight=2.1,
        predicted_price=45000.00,
        created_at=datetime.utcnow()
    )
    
    try:
        db.session.add(test_prediction)
        db.session.commit()
        print("✓ Test prediction added successfully")
        
        # Count after
        after_count = Prediction.query.count()
        print(f"Predictions in DB after test: {after_count}")
        
        if after_count == before_count + 1:
            print("✓ Prediction was saved correctly!")
            
            # Get the last prediction
            last_pred = Prediction.query.order_by(Prediction.id.desc()).first()
            print(f"\nLast prediction details:")
            print(f"  ID: {last_pred.id}")
            print(f"  User ID: {last_pred.user_id}")
            print(f"  Brand: {last_pred.brand}")
            print(f"  Price: {last_pred.predicted_price}")
            print(f"  Created: {last_pred.created_at}")
            
            # Delete the test prediction
            db.session.delete(test_prediction)
            db.session.commit()
            print("\n✓ Test prediction cleaned up")
        else:
            print("✗ Count mismatch - prediction may not have been saved")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        db.session.rollback()
        import traceback
        traceback.print_exc()
