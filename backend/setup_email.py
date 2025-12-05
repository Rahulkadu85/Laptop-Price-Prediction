"""
Interactive Email Setup Script
This will help you configure your Gmail App Password
"""
import os

print("=" * 70)
print("EMAIL CONFIGURATION SETUP")
print("=" * 70)

print("\n📧 Your email: rahulkadu191@gmail.com ✓")

print("\n" + "=" * 70)
print("STEP 1: Get Gmail App Password")
print("=" * 70)
print("\n1. Open: https://myaccount.google.com/security")
print("2. Enable '2-Step Verification' (if not already enabled)")
print("3. Go to: https://myaccount.google.com/apppasswords")
print("4. Generate an App Password for 'Mail'")
print("5. Copy the 16-digit password")

print("\n" + "=" * 70)
print("STEP 2: Enter Your App Password")
print("=" * 70)

app_password = input("\nPaste your 16-digit App Password here (remove spaces): ").strip().replace(" ", "")

if len(app_password) < 10:
    print("\n❌ Error: Password seems too short. App passwords are usually 16 characters.")
    print("Please try again and paste the complete password.")
    exit(1)

print("\n" + "=" * 70)
print("STEP 3: Choose Mode")
print("=" * 70)
print("\n1. Production Mode - Actually send emails")
print("2. Dev Mode - Just print to console")

choice = input("\nEnter choice (1 or 2): ").strip()

dev_mode = "True" if choice == "2" else "False"

# Read current config
config_path = os.path.join(os.path.dirname(__file__), 'otp_config.py')

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace password
    if "SMTP_PASSWORD = " in content:
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if line.strip().startswith("SMTP_PASSWORD = "):
                new_lines.append(f"SMTP_PASSWORD = '{app_password}'  # ✓ Configured")
            elif line.strip().startswith("DEV_MODE = "):
                new_lines.append(f"DEV_MODE = {dev_mode}  # ✓ Set by setup script")
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        # Write back
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n" + "=" * 70)
        print("✓ CONFIGURATION SAVED!")
        print("=" * 70)
        print(f"\nSMTP_PASSWORD: {app_password[:4]}...{app_password[-4:]} (hidden for security)")
        print(f"DEV_MODE: {dev_mode}")
        
        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("\n1. Test email sending:")
        print("   python test_otp.py")
        print("\n2. Start your Flask app:")
        print("   python app.py")
        print("\n3. Try logging in - you should receive OTP in your email!")
        
        if dev_mode == "False":
            print("\n📧 Emails will be sent to: rahulkadu191@gmail.com")
            print("   Check your inbox (and spam folder)")
        else:
            print("\n📝 OTP will be printed to console")
        
    else:
        print("\n❌ Error: Could not find SMTP_PASSWORD in config file")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
