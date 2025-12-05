# 📧 How to Setup Your SMTP Password - Step by Step Guide

## ✅ Your Email is Already Configured!
- **Email:** rahulkadu191@gmail.com ✓

Now you just need to add your **Gmail App Password**.

---

## 🔐 Step-by-Step Instructions

### Step 1: Enable 2-Factor Authentication

1. Go to: **https://myaccount.google.com/**
2. Click on **"Security"** in the left menu
3. Scroll down to **"2-Step Verification"**
4. Click **"Get Started"** and follow the setup process
5. ✅ Complete 2-Factor Authentication setup

---

### Step 2: Generate Gmail App Password

1. Go to: **https://myaccount.google.com/apppasswords**
   
   (Or: Google Account → Security → 2-Step Verification → App passwords)

2. You may need to **sign in again**

3. You'll see **"App passwords"** page

4. Under **"Select app"**, choose **"Mail"**

5. Under **"Select device"**, choose your device or **"Other"** and type "Laptop Price Predictor"

6. Click **"Generate"**

7. Google will show you a **16-character password** like this:
   ```
   abcd efgh ijkl mnop
   ```

8. **Copy this password** (you'll need it in the next step)

---

### Step 3: Add Password to Configuration File

1. Open the file: **`backend/otp_config.py`**

2. Find this line:
   ```python
   SMTP_PASSWORD = 'your-16-digit-app-password-here'  # ← CHANGE THIS!
   ```

3. Replace it with your app password (remove spaces):
   ```python
   SMTP_PASSWORD = 'abcdefghijklmnop'  # ✓ Your actual app password
   ```

   **Example:**
   ```python
   # If Google gave you: abcd efgh ijkl mnop
   # You write: abcdefghijklmnop (no spaces)
   SMTP_PASSWORD = 'abcdefghijklmnop'
   ```

4. Change `DEV_MODE` to `False`:
   ```python
   DEV_MODE = False  # This will actually send emails
   ```

5. **Save the file** (Ctrl+S)

---

### Step 4: Test Your Configuration

1. Open terminal in `backend` folder:
   ```bash
   cd backend
   ```

2. Run the test script:
   ```bash
   python test_otp.py
   ```

3. **Check your email!** You should receive an OTP email.

4. If you see this in the console:
   ```
   ✓ Email OTP sent to rahulkadu191@gmail.com
   ```
   **Success!** 🎉

---

## 📝 Quick Reference

### Your Configuration (in `otp_config.py`):

```python
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_EMAIL = 'rahulkadu191@gmail.com'  # ✓ Already set
SMTP_PASSWORD = 'your-16-digit-app-password'  # ← Add your app password here
DEV_MODE = False  # Set to False to send real emails
```

---

## ⚠️ Important Notes

### **DO NOT use your regular Gmail password!**
- ❌ Regular password: Will NOT work
- ✅ App password: 16-digit code from Google

### **App Password Format:**
- Google shows: `abcd efgh ijkl mnop` (with spaces)
- You type: `abcdefghijklmnop` (no spaces)

### **Security:**
- Keep your app password **private**
- Don't share `otp_config.py` file
- Add `otp_config.py` to `.gitignore` if using Git

---

## 🧪 Testing Checklist

- [ ] 2-Factor Authentication enabled on Google Account
- [ ] App password generated from Google
- [ ] App password added to `otp_config.py` (no spaces)
- [ ] `DEV_MODE = False` in config
- [ ] File saved
- [ ] Test script run: `python test_otp.py`
- [ ] Email received in inbox

---

## 🔧 Troubleshooting

### **Issue: "Username and Password not accepted"**

**Solution:**
1. Make sure you're using **App Password**, not regular password
2. Check that 2-Factor Authentication is enabled
3. Generate a **new** App Password
4. Make sure there are **no spaces** in the password

### **Issue: Email not received**

**Check:**
1. Spam/Junk folder
2. Gmail inbox filters
3. Console output for errors
4. Internet connection

### **Issue: "App passwords" option not visible**

**Solution:**
1. First enable 2-Factor Authentication
2. Wait a few minutes
3. Refresh the page
4. Try this direct link: https://myaccount.google.com/apppasswords

---

## 🎯 After Setup

Once configured, your app will:
- ✅ Send OTP emails automatically at login
- ✅ Use professional HTML email template
- ✅ Show clear OTP codes to users
- ✅ Track all OTPs in database

---

## 📞 Need Help?

If you're still having issues:

1. **Check Flask console** for error messages
2. **Try DEV_MODE = True** first to test without email
3. **Generate a new App Password** and try again
4. **Verify email** is spelled correctly in config

---

## ✅ Quick Setup (TL;DR)

```bash
# 1. Enable 2FA on Google Account
#    https://myaccount.google.com/security

# 2. Generate App Password
#    https://myaccount.google.com/apppasswords

# 3. Edit otp_config.py
SMTP_PASSWORD = 'your-16-digit-password'
DEV_MODE = False

# 4. Test it
python test_otp.py
```

**Done!** 🎉
