"""
OTP Configuration File
Configure your email and SMS settings here
"""

# ==============================================================================
# EMAIL CONFIGURATION (Required for OTP)
# ==============================================================================

# For Gmail:
# 1. Go to https://myaccount.google.com/
# 2. Enable 2-Factor Authentication
# 3. Go to https://myaccount.google.com/apppasswords
# 4. Select "Mail" and your device
# 5. Copy the 16-digit password (it will look like: xxxx xxxx xxxx xxxx)
# 6. Paste it below (remove spaces)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_EMAIL = 'rahulkadu191@gmail.com'  # ✓ Your email is set!
SMTP_PASSWORD = 'wzfcqmvdbneslvkq'  # ✓ Configured

# ==============================================================================
# IMPORTANT: Use Gmail App Password, NOT your regular Gmail password!
# App passwords are 16 characters long and look like: abcd efgh ijkl mnop
# Remove spaces when pasting: abcdefghijklmnop
# ==============================================================================

# OTP Settings
OTP_EXPIRY_MINUTES = 10  # How long the OTP is valid
OTP_LENGTH = 6  # 6-digit OTP

# SMS Configuration (Optional - for Twilio)
# Sign up at https://www.twilio.com/ to get these credentials
USE_SMS = False  # Set to True to enable SMS
TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'  # Your Twilio phone number

# Development Mode
# If True, OTP will be printed to console instead of sending email/SMS
DEV_MODE = False  # ✓ Set by setup script
