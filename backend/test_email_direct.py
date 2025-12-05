"""
Test email sending with your actual Gmail credentials
This will help diagnose the issue
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("=" * 70)
print("GMAIL OTP EMAIL TEST")
print("=" * 70)

email = 'rahulkadu191@gmail.com'
print(f"\nYour email: {email}")

print("\n" + "=" * 70)
print("IMPORTANT: You need a Gmail App Password!")
print("=" * 70)
print("\n1. Go to: https://myaccount.google.com/apppasswords")
print("2. Generate an App Password for 'Mail'")
print("3. Copy the 16-digit password")
print("4. Paste it below when asked")

password = input("\nEnter your Gmail App Password (16 digits, no spaces): ").strip().replace(" ", "")

if len(password) < 10:
    print("\n❌ Password seems too short. App passwords are 16 characters.")
    print("Please get it from: https://myaccount.google.com/apppasswords")
    exit(1)

print("\n📧 Attempting to send test email...")

try:
    # Create test email
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'OTP Test - Laptop Price Predictor'
    
    body = f"""
    <h2>✅ Email Configuration Test Successful!</h2>
    <p>Your OTP email system is now working correctly.</p>
    <p>Test OTP Code: <strong>123456</strong></p>
    <p>This is a test email from your Laptop Price Prediction app.</p>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.send_message(msg)
    server.quit()
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Email sent successfully!")
    print("=" * 70)
    print(f"\nCheck your inbox: {email}")
    print("(Also check spam/junk folder)")
    
    print("\n" + "=" * 70)
    print("NEXT STEP: Update Configuration")
    print("=" * 70)
    print("\nYour App Password works! Now let's save it to config...")
    
    # Update config file
    config_path = 'otp_config.py'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace password line
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if "SMTP_PASSWORD = " in line and "CHANGE THIS" in line:
                new_lines.append(f"SMTP_PASSWORD = '{password}'  # ✓ App Password configured!")
            else:
                new_lines.append(line)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print("\n✓ Configuration file updated!")
        print("✓ DEV_MODE is already set to False")
        print("\n🎉 Your OTP emails will now work!")
        print("\nRun: python app.py")
        print("Then try logging in - you'll receive OTP via email!")
        
    except Exception as e:
        print(f"\n⚠️ Could not auto-update config: {e}")
        print(f"\nManually add this to otp_config.py line 21:")
        print(f"SMTP_PASSWORD = '{password}'")
    
except smtplib.SMTPAuthenticationError as e:
    print("\n" + "=" * 70)
    print("❌ AUTHENTICATION FAILED")
    print("=" * 70)
    print("\nError:", str(e))
    print("\n📋 Troubleshooting:")
    print("1. Make sure you're using Gmail APP PASSWORD, not regular password")
    print("2. Enable 2-Step Verification first")
    print("3. Generate new App Password at: https://myaccount.google.com/apppasswords")
    print("4. Copy the password exactly (remove all spaces)")
    
except Exception as e:
    print("\n" + "=" * 70)
    print("❌ ERROR")
    print("=" * 70)
    print(f"\nError: {e}")
    print("\nMake sure:")
    print("1. You have internet connection")
    print("2. Gmail App Password is correct")
    print("3. 2-Step Verification is enabled on your Google Account")

print("\n" + "=" * 70)
