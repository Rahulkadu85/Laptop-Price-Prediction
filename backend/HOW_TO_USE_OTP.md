# 🔐 How to Use OTP Login - Complete Guide

## ✅ What's Implemented

Your Laptop Price Prediction app now has **full OTP (One-Time Password) authentication** at login time!

### 📋 Login Flow:

```
1. User enters username + password
        ↓
2. System validates credentials
        ↓
3. System generates 6-digit OTP
        ↓
4. OTP sent to Email (& SMS if phone provided)
        ↓
5. User sees OTP input screen
        ↓
6. User enters 6-digit OTP
        ↓
7. System verifies OTP
        ↓
8. Login complete! ✅
```

---

## 🎯 How to Use (Step by Step)

### **For New Users (Signup):**

1. Click **"Sign Up"** tab
2. Enter:
   - Username
   - Email address
   - Phone number (optional - for SMS OTP)
   - Password (minimum 6 characters)
3. Click **"Create Account"**
4. Account created! You're logged in directly (no OTP needed for first signup)

### **For Existing Users (Login with OTP):**

1. Click **"Sign In"** tab
2. Enter your **username** and **password**
3. Click **"Sign In"**
4. **OTP Screen appears!** 📱
   - Shows where OTP was sent (email/phone)
   - Check your email inbox (and spam folder)
   - Check your SMS if you provided phone number
5. Enter the **6-digit OTP code**
6. Click **"Verify OTP"**
7. ✅ Login successful!

---

## 🖥️ UI Features

### OTP Verification Screen:

**Shows:**
- 🔐 "Enter OTP" heading
- 📧 Email where OTP was sent
- 📱 Phone number where OTP was sent (if provided)
- Input field for 6-digit code
- ✓ "Verify OTP" button
- 🔄 "Resend OTP" button
- ← "Back to Login" button

**Features:**
- Large input field with centered text
- Letter-spaced for easy reading
- Only accepts 6 digits
- Success/error messages
- Helpful tip about checking spam folder

---

## 🔄 Additional Features

### **Resend OTP:**
- If you didn't receive the OTP
- Click **"🔄 Resend OTP"** button
- New OTP will be generated and sent
- Old OTP will be invalidated

### **Back to Login:**
- Click **"← Back to Login"** to return to login screen
- Useful if you entered wrong credentials

### **OTP Expiry:**
- OTP is valid for **10 minutes**
- After 10 minutes, request a new OTP

---

## 📧 Email Configuration (For Production)

Currently in **DEV_MODE**, OTP is printed to console. To actually send emails:

### **Step 1: Edit `otp_config.py`**

```python
# Your Gmail account
SMTP_EMAIL = 'youremail@gmail.com'

# Gmail App Password (not your regular password!)
SMTP_PASSWORD = 'your-16-digit-app-password'

# Set to False to actually send emails
DEV_MODE = False
```

### **Step 2: Get Gmail App Password**

1. Go to https://myaccount.google.com/
2. Enable **2-Factor Authentication**
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" and your device
5. Copy the 16-digit password
6. Paste it in `otp_config.py`

---

## 📱 SMS Configuration (Optional)

### **Using Twilio:**

1. Sign up at https://www.twilio.com/
2. Get credentials from dashboard
3. Edit `otp_config.py`:

```python
USE_SMS = True
TWILIO_ACCOUNT_SID = 'your_sid_here'
TWILIO_AUTH_TOKEN = 'your_token_here'
TWILIO_PHONE_NUMBER = '+1234567890'
```

---

## 🧪 Testing

### **In Development Mode:**

1. Run Flask app:
   ```bash
   cd backend
   python app.py
   ```

2. Open browser to `http://localhost:5000`

3. Try to login with existing user

4. **Check Flask console** for OTP:
   ```
   ✓ Email OTP sent to user@example.com
     OTP for user@example.com: 123456
   ```

5. Enter the OTP from console into the web form

6. Verify it works!

---

## 📊 What Happens Behind the Scenes

### **When you click "Sign In":**

**Backend (`app.py`):**
```python
1. Validates username/password
2. Generates 6-digit random OTP
3. Stores OTP in database with expiry time
4. Sends OTP via email (and SMS if phone exists)
5. Returns response: { requires_otp: true }
```

**Frontend (`app.js`):**
```javascript
1. Receives response with requires_otp
2. Shows OTP input screen
3. Displays email/phone where OTP was sent
4. Waits for user to enter OTP
```

### **When you enter OTP:**

**Frontend:**
```javascript
1. Sends OTP to /api/verify-otp
```

**Backend:**
```python
1. Checks if OTP exists and is not expired
2. Checks if OTP matches
3. Marks OTP as verified
4. Completes login
5. Returns user data
```

**Frontend:**
```javascript
1. Receives user data
2. Hides OTP screen
3. Shows main app
4. Loads prediction history
```

---

## 🔍 Troubleshooting

### **Issue: OTP not showing in email**

**Solution:**
1. Check Flask console - OTP is printed there in DEV_MODE
2. Check spam/junk folder
3. Verify `DEV_MODE = False` in `otp_config.py`
4. Verify email credentials are correct
5. Make sure you're using Gmail App Password, not regular password

### **Issue: "Invalid or expired OTP"**

**Reasons:**
- OTP expired (>10 minutes old)
- Wrong OTP code
- OTP already used
- You requested a new OTP (old one invalidated)

**Solution:**
- Click "Resend OTP" to get a fresh code
- Make sure you're entering the latest OTP

### **Issue: Not receiving SMS**

**Check:**
- Is `USE_SMS = True` in `otp_config.py`?
- Are Twilio credentials correct?
- Did user provide phone number during signup?
- Check Twilio console for delivery status

---

## 📂 Database Tables

### **User Table (updated):**
```sql
id              INTEGER PRIMARY KEY
username        VARCHAR(80)
email           VARCHAR(120)
phone           VARCHAR(15)      -- NEW!
password_hash   VARCHAR(200)
created_at      DATETIME
```

### **OTP Table (new):**
```sql
id              INTEGER PRIMARY KEY
user_id         INTEGER (foreign key)
otp_code        VARCHAR(6)
otp_type        VARCHAR(10)      -- 'email' or 'sms'
created_at      DATETIME
expires_at      DATETIME
is_verified     BOOLEAN
```

---

## 🎨 UI/UX Features

✅ **Beautiful OTP input** - Large, centered, letter-spaced
✅ **Shows where OTP was sent** - Email and phone display
✅ **Resend functionality** - Easy to request new OTP
✅ **Back button** - Return to login if needed
✅ **Success/error messages** - Clear feedback
✅ **Loading states** - Shows "Verifying..." during check
✅ **Helpful tips** - Reminds to check spam folder
✅ **Responsive design** - Works on all devices

---

## 🚀 Quick Test Checklist

- [ ] Run migration: `python add_otp_tables.py`
- [ ] Start Flask: `python app.py`
- [ ] Open browser: `http://localhost:5000`
- [ ] Sign up with email (and optional phone)
- [ ] Logout
- [ ] Sign in - OTP screen should appear
- [ ] Check console for OTP code
- [ ] Enter OTP code
- [ ] Login should complete
- [ ] Try "Resend OTP" button
- [ ] Try "Back to Login" button
- [ ] Try wrong OTP code
- [ ] Try expired OTP (wait 10+ minutes)

---

## 📞 Need Help?

1. Check Flask console for errors
2. Verify `otp_config.py` settings
3. Run `python test_otp.py` to test OTP generation
4. Check database: `python view_database.py`
5. Look at OTP table: Check if OTPs are being created

---

## 🎉 Success!

You now have a **production-ready 2-Factor Authentication system** with:
- ✅ Email OTP
- ✅ SMS OTP (optional)
- ✅ Beautiful UI
- ✅ Resend functionality
- ✅ Expiry handling
- ✅ Database tracking

**Your users' accounts are now much more secure!** 🔒
