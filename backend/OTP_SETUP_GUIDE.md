# 🔐 OTP (One-Time Password) Setup Guide

## ✅ Features Added

Your Laptop Price Prediction app now supports **2-Factor Authentication (2FA)** with OTP!

### What's New:
- 📧 **Email OTP** - Receive 6-digit OTP code via email
- 📱 **SMS OTP** - Receive OTP code via SMS (optional, requires phone number)
- ⏱️ **Time-limited** - OTP expires after 10 minutes
- 🔄 **Resend OTP** - Request a new code if needed
- 🔒 **Secure Login** - Two-step verification for enhanced security

---

## 🚀 How It Works

### Login Flow:
1. User enters **username** and **password**
2. System sends **OTP** to registered email (and SMS if phone provided)
3. User enters the **6-digit OTP code**
4. System verifies OTP and completes login

---

## 📋 Setup Instructions

### Step 1: Run Migration (Already Done ✓)
```bash
cd backend
python add_otp_tables.py
```

### Step 2: Configure Email Settings

Edit `otp_config.py` and add your email credentials:

#### For Gmail:
1. Go to your Google Account: https://myaccount.google.com/
2. Enable **2-Factor Authentication**
3. Generate an **App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-digit password

4. Update `otp_config.py`:
```python
SMTP_EMAIL = 'your-email@gmail.com'
SMTP_PASSWORD = 'your-16-digit-app-password'
DEV_MODE = False  # Set to False to actually send emails
```

#### For Other Email Providers:
```python
# For Outlook/Hotmail
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587

# For Yahoo
SMTP_SERVER = 'smtp.mail.yahoo.com'
SMTP_PORT = 587
```

### Step 3: Configure SMS (Optional)

#### Using Twilio:
1. Sign up at https://www.twilio.com/
2. Get your credentials from the dashboard
3. Update `otp_config.py`:
```python
USE_SMS = True
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'
```

---

## 🧪 Testing

### Development Mode (Current):
With `DEV_MODE = True` in `otp_config.py`, OTP codes are **printed to console** instead of being sent:

```bash
python app.py
```

When someone logs in, you'll see:
```
✓ Email OTP sent to user@example.com
  OTP for user@example.com: 123456
```

### Production Mode:
Set `DEV_MODE = False` in `otp_config.py` to actually send emails.

---

## 📝 API Endpoints

### 1. Sign Up (with optional phone)
```http
POST /api/signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "+1234567890",  // Optional
  "password": "secure123"
}
```

### 2. Sign In (sends OTP)
```http
POST /api/signin
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure123"
}

Response:
{
  "message": "OTP sent successfully",
  "otp_sent_to": {
    "email": "john@example.com",
    "phone": "+1234567890"
  },
  "requires_otp": true
}
```

### 3. Verify OTP
```http
POST /api/verify-otp
Content-Type: application/json

{
  "otp": "123456"
}

Response:
{
  "message": "Login successful",
  "user": { ... }
}
```

### 4. Resend OTP
```http
POST /api/resend-otp

Response:
{
  "message": "OTP resent successfully"
}
```

---

## 🎨 Frontend Integration Example

```javascript
// Login step 1: Send credentials
const loginResponse = await fetch('/api/signin', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ username, password })
});

const data = await loginResponse.json();

if (data.requires_otp) {
    // Show OTP input form
    showOTPForm(data.otp_sent_to);
}

// Login step 2: Verify OTP
const verifyResponse = await fetch('/api/verify-otp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ otp: userEnteredOTP })
});

if (verifyResponse.ok) {
    // Login successful!
    const user = await verifyResponse.json();
}
```

---

## 🗄️ Database Changes

### New `phone` column in `user` table:
```sql
phone VARCHAR(15)  -- Optional phone number
```

### New `otp` table:
```sql
CREATE TABLE otp (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    otp_code VARCHAR(6),
    otp_type VARCHAR(10),  -- 'email' or 'sms'
    created_at DATETIME,
    expires_at DATETIME,
    is_verified BOOLEAN
)
```

---

## ⚙️ Configuration Options

### In `otp_config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `OTP_EXPIRY_MINUTES` | 10 | How long OTP is valid |
| `OTP_LENGTH` | 6 | Number of digits in OTP |
| `DEV_MODE` | True | Print OTP to console instead of sending |
| `USE_SMS` | False | Enable SMS OTP |

---

## 🔍 Troubleshooting

### Issue: OTP not received via email

**Check:**
1. Is `DEV_MODE = False` in `otp_config.py`?
2. Are email credentials correct?
3. Did you use Gmail App Password (not regular password)?
4. Check Flask console for error messages
5. Check spam/junk folder

**Solution:**
```bash
# Check console output
python app.py
# Look for "✓ Email OTP sent" or error messages
```

### Issue: "Invalid or expired OTP"

**Reasons:**
- OTP expired (>10 minutes old)
- Wrong OTP code entered
- OTP already used

**Solution:**
- Click "Resend OTP" to get a new code
- Make sure you're entering the latest OTP

---

## 📊 View OTP Records

```bash
cd backend
python -c "import sqlite3; conn = sqlite3.connect('laptop_price.db'); cursor = conn.cursor(); cursor.execute('SELECT * FROM otp ORDER BY id DESC LIMIT 5'); print(cursor.fetchall())"
```

---

## 🔒 Security Best Practices

1. ✅ **Never share** your SMTP password
2. ✅ Use **App Passwords** for Gmail (not your main password)
3. ✅ Set `DEV_MODE = False` in production
4. ✅ Use **HTTPS** in production
5. ✅ Rotate **SMTP credentials** periodically
6. ✅ Store `otp_config.py` securely (add to `.gitignore`)

---

## 🎯 Testing Checklist

- [ ] Run migration script
- [ ] Configure email settings
- [ ] Test signup with phone number
- [ ] Test login (OTP sent to email)
- [ ] Test OTP verification
- [ ] Test resend OTP
- [ ] Test expired OTP
- [ ] Test invalid OTP
- [ ] (Optional) Test SMS OTP

---

## 📞 Support

If you encounter issues:
1. Check Flask console for error messages
2. Verify `otp_config.py` settings
3. Test in DEV_MODE first
4. Check database with `view_database.py`

---

**Congratulations! 🎉 Your app now has 2-Factor Authentication!**
