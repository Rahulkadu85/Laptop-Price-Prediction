"""
Test OTP functionality - Demonstrates how OTP login works
"""
from app import app, db, User, OTP, generate_otp, send_email_otp, send_sms_otp
from datetime import datetime, timedelta

print("=" * 70)
print("OTP FUNCTIONALITY TEST")
print("=" * 70)

with app.app_context():
    # Get a test user
    user = User.query.first()
    
    if not user:
        print("\n❌ No users found. Create a user first through signup.")
        exit(1)
    
    print(f"\n👤 Testing with user: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Phone: {user.phone if user.phone else 'Not provided'}")
    
    # Generate OTP
    print("\n🔐 Generating OTP...")
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    # Create OTP record
    otp_record = OTP(
        user_id=user.id,
        otp_code=otp_code,
        otp_type='email',
        expires_at=expires_at
    )
    db.session.add(otp_record)
    db.session.commit()
    
    print(f"✓ OTP Generated: {otp_code}")
    print(f"  Expires at: {expires_at}")
    print(f"  OTP ID: {otp_record.id}")
    
    # Send OTP (will print to console in DEV_MODE)
    print("\n📧 Sending Email OTP...")
    send_email_otp(user.email, otp_code, user.username)
    
    if user.phone:
        print("\n📱 Sending SMS OTP...")
        send_sms_otp(user.phone, otp_code, user.username)
    
    # Show OTP records
    print("\n📊 OTP Records in Database:")
    all_otps = OTP.query.filter_by(user_id=user.id).order_by(OTP.id.desc()).limit(5).all()
    
    print(f"\n{'ID':<5} {'Code':<10} {'Type':<10} {'Verified':<10} {'Expires At':<25}")
    print("-" * 70)
    for otp in all_otps:
        verified = "✓ Yes" if otp.is_verified else "✗ No"
        print(f"{otp.id:<5} {otp.otp_code:<10} {otp.otp_type:<10} {verified:<10} {otp.expires_at}")
    
    print("\n" + "=" * 70)
    print("✓ TEST COMPLETE!")
    print("=" * 70)
    print("\nNOTE: In DEV_MODE, OTP is printed to console instead of being sent.")
    print("To actually send emails, set DEV_MODE=False in otp_config.py")
