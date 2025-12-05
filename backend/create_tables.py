from app import app, db, User, OTP, Prediction

# Create all tables explicitly
with app.app_context():
    print("Creating User table...")
    User.__table__.create(db.engine, checkfirst=True)
    
    print("Creating OTP table...")
    OTP.__table__.create(db.engine, checkfirst=True)
    
    print("Creating Prediction table...")
    Prediction.__table__.create(db.engine, checkfirst=True)
    
    print("All tables created successfully!")