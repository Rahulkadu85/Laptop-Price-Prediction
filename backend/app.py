from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # Add this import
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pickle
import numpy as np
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Secret key for session management
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Session configuration for CORS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_TYPE'] = 'filesystem'  # Filesystem not supported on Vercel
# Session(app) # Use default cookie-based sessions for Vercel compatibility

# Disable caching for static files in development
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

base_dir = os.path.dirname(os.path.abspath(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'instance', 'laptop_price.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load models
try:
    model = pickle.load(open(os.path.join(base_dir, 'model.pkl'), 'rb'))
    encoder = pickle.load(open(os.path.join(base_dir, 'encoder.pkl'), 'rb'))
    scaler = pickle.load(open(os.path.join(base_dir, 'scaler.pkl'), 'rb'))
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    encoder = None
    scaler = None

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15))  # Phone number for SMS OTP
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat()
        }

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    otp_type = db.Column(db.String(10), nullable=False)  # 'email' or 'sms'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    brand = db.Column(db.String(50))
    processor_speed = db.Column(db.Float)
    ram_size = db.Column(db.Integer)
    storage_capacity = db.Column(db.Integer)
    screen_size = db.Column(db.Float)
    weight = db.Column(db.Float)
    predicted_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'processor_speed': self.processor_speed,
            'ram_size': self.ram_size,
            'storage_capacity': self.storage_capacity,
            'screen_size': self.screen_size,
            'weight': self.weight,
            'predicted_price': self.predicted_price,
            'created_at': self.created_at.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()

# OTP Configuration - Load from config file
try:
    from otp_config import (
        OTP_EXPIRY_MINUTES,
        SMTP_SERVER,
        SMTP_PORT,
        SMTP_EMAIL,
        SMTP_PASSWORD,
        DEV_MODE
    )
    print("[OK] OTP configuration loaded successfully")
except ImportError:
    # Default values if config file not found
    OTP_EXPIRY_MINUTES = 10
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_EMAIL = 'rahulkadu191@gmail.com'
    SMTP_PASSWORD = 'fvwg oxax twrt lill'
    DEV_MODE = False
    print("[WARNING] Warning: otp_config.py not found. Using default values.")

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_email_otp(email, otp_code, username):
    """Send OTP via email"""
    # Check if DEV_MODE is enabled
    if DEV_MODE:
        print(f"\n{'='*60}")
        print("📧 DEV MODE: Email not sent, printing OTP instead")
        print(f"{'='*60}")
        print(f"To: {email}")
        print(f"Subject: Your Login OTP - Laptop Price Predictor")
        print(f"OTP Code: {otp_code}")
        print(f"Expires: {OTP_EXPIRY_MINUTES} minutes")
        print(f"{'='*60}\n")
        return True
    
    # Production mode - actually send email
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_EMAIL
        msg['To'] = email
        msg['Subject'] = 'Your Login OTP - Laptop Price Predictor'
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #667eea; text-align: center;">💻 Laptop Price Predictor</h2>
                <h3 style="color: #333;">Hello {username}!</h3>
                <p style="font-size: 16px; color: #555;">Your One-Time Password (OTP) for login is:</p>
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 32px; font-weight: bold; text-align: center; padding: 20px; border-radius: 8px; letter-spacing: 5px; margin: 20px 0;">
                    {otp_code}
                </div>
                <p style="font-size: 14px; color: #666;">This OTP will expire in {OTP_EXPIRY_MINUTES} minutes.</p>
                <p style="font-size: 14px; color: #666;">If you didn't request this OTP, please ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #999; text-align: center;">Laptop Price Prediction App</p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"[OK] Email OTP sent to {email}")
        return True
    except Exception as e:
        print(f"[ERROR] Email error: {e}")
        # Fallback to console if email fails
        print(f"\n{'='*60}")
        print("OTP Code (email failed, showing here):")
        print(f"OTP for {email}: {otp_code}")
        print(f"{'='*60}\n")
        return False

def send_sms_otp(phone, otp_code, username):
    """Send OTP via SMS (using Twilio or similar service)"""
    try:
        # For demonstration - in production, use Twilio, AWS SNS, or similar
        # Twilio example:
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body=f"Your Laptop Price Predictor OTP is: {otp_code}. Valid for {OTP_EXPIRY_MINUTES} minutes.",
        #     from_='+1234567890',
        #     to=phone
        # )
        
        # For now, just print to console (for development)
        print(f"[OK] SMS OTP would be sent to {phone}: {otp_code}")
        print(f"  Message: Your Laptop Price Predictor OTP is: {otp_code}. Valid for {OTP_EXPIRY_MINUTES} minutes.")
        return True
    except Exception as e:
        print(f"[ERROR] SMS error: {e}")
        print(f"  OTP for {phone}: {otp_code}")
        return False

# Authentication Routes
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')  # Optional phone number
        password = data.get('password')

        # Validation
        if not username or not email or not password:
            return jsonify({'error': 'Username, email and password are required'}), 400

        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400

        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        # Create new user
        new_user = User(username=username, email=email, phone=phone)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Log user in
        session['user_id'] = new_user.id
        session['username'] = new_user.username

        return jsonify({
            'message': 'Account created successfully',
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/signin', methods=['POST'])
def signin():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        # Find user
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Generate OTP
        otp_code = generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
        
        # Delete old OTPs for this user
        OTP.query.filter_by(user_id=user.id, is_verified=False).delete()
    db.session.commit()
        
        # Create OTP records
        email_otp = OTP(
            user_id=user.id,
            otp_code=otp_code,
            otp_type='email',
            expires_at=expires_at
        )
        db.session.add(email_otp)
        
        # If user has phone, create SMS OTP too (same code for simplicity)
        if user.phone:
            sms_otp = OTP(
                user_id=user.id,
                otp_code=otp_code,
                otp_type='sms',
                expires_at=expires_at
            )
            db.session.add(sms_otp)
        
                db.session.commit()
        
        # Send OTP via email
        send_email_otp(user.email, otp_code, user.username)
        
        # Send OTP via SMS if phone exists
        if user.phone:
            send_sms_otp(user.phone, otp_code, user.username)
        
        # Store user_id temporarily in session (not fully authenticated yet)
        session['pending_user_id'] = user.id
        
        return jsonify({
            'message': 'OTP sent successfully',
            'otp_sent_to': {
                'email': user.email,
                'phone': user.phone if user.phone else None
            },
            'requires_otp': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.json
        otp_code = data.get('otp')
        
        if not otp_code:
            return jsonify({'error': 'OTP is required'}), 400
        
        # Check if there's a pending user
        if 'pending_user_id' not in session:
            return jsonify({'error': 'No pending authentication. Please sign in first.'}), 401
        
        user_id = session['pending_user_id']
        
        # Find valid OTP
        otp_record = OTP.query.filter_by(
            user_id=user_id,
            otp_code=otp_code,
            is_verified=False
        ).filter(OTP.expires_at > datetime.utcnow()).first()
        
        if not otp_record:
            return jsonify({'error': 'Invalid or expired OTP'}), 401
        
        # Mark OTP as verified
        otp_record.is_verified = True
        db.session.commit()
        
        # Get user
        user = User.query.get(user_id)
        
        # Fully authenticate user
        session.pop('pending_user_id', None)
        session['user_id'] = user.id
        session['username'] = user.username
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resend-otp', methods=['POST'])
def resend_otp():
    try:
        if 'pending_user_id' not in session:
            return jsonify({'error': 'No pending authentication'}), 401
        
        user = User.query.get(session['pending_user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate new OTP
        otp_code = generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
        
        # Delete old unverified OTPs
        OTP.query.filter_by(user_id=user.id, is_verified=False).delete()
            db.session.commit()
        
        # Create new OTP records
        email_otp = OTP(
            user_id=user.id,
            otp_code=otp_code,
            otp_type='email',
            expires_at=expires_at
        )
        db.session.add(email_otp)
        
        if user.phone:
            sms_otp = OTP(
                user_id=user.id,
                otp_code=otp_code,
                otp_type='sms',
                expires_at=expires_at
            )
            db.session.add(sms_otp)
        
                db.session.commit()
        
        # Send OTP
        send_email_otp(user.email, otp_code, user.username)
        if user.phone:
            send_sms_otp(user.phone, otp_code, user.username)
        
        return jsonify({
            'message': 'OTP resent successfully',
            'otp_sent_to': {
                'email': user.email,
                'phone': user.phone if user.phone else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': user.to_dict()
            }), 200
    return jsonify({'authenticated': False}), 200

# Main Routes
@app.route('/')
def landing():
    """Landing page - shown by default"""
    return render_template('landing.html')

@app.route('/app')
def index():
    """Main application"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check authentication
    if 'user_id' not in session:
        return jsonify({'error': 'Please login to make predictions'}), 401

    if not model:
        return jsonify({'error': 'Models not loaded'}), 500
        
    try:
        data = request.json
        brand = data['brand']
        processor_speed = float(data['processor_speed'])
        ram_size = int(float(data['ram_size']))
        storage_capacity = int(float(data['storage_capacity']))
        screen_size = float(data['screen_size'])
        weight = float(data['weight'])

        # Encode Brand
        try:
            brand_encoded = encoder.transform([brand])[0]
        except ValueError:
            return jsonify({'error': f'Unknown brand: {brand}. Available brands: {list(encoder.classes_)}'}), 400

        # Prepare features for scaling
        features = np.array([[brand_encoded, processor_speed, ram_size, storage_capacity, screen_size, weight]])
        
        # Scale features
        scaled_features = scaler.transform(features)

        # Predict
        prediction = model.predict(scaled_features)[0]

        # Save to DB with user_id
        new_prediction = Prediction(
            user_id=session['user_id'],
            brand=brand,
            processor_speed=processor_speed,
            ram_size=ram_size,
            storage_capacity=storage_capacity,
            screen_size=screen_size,
            weight=weight,
            predicted_price=prediction
        )
        db.session.add(new_prediction)
        db.session.commit()
        print(f"[OK] Prediction saved: ID={new_prediction.id}, User={session['user_id']}, Brand={brand}, Price={prediction}")

        return jsonify({'price': prediction})

    except Exception as e:
        print(f"[ERROR] Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def history():
    # Debug logging
    print(f"[DEBUG] /history endpoint called")
    print(f"[DEBUG] Session contents: {dict(session)}")
    print(f"[DEBUG] Cookies: {request.cookies}")
    
    # Check authentication
    if 'user_id' not in session:
        print(f"[DEBUG] No user_id in session - returning 401")
        return jsonify({'error': 'Please login to view history'}), 401

    user_id = session['user_id']
    print(f"[DEBUG] Fetching predictions for user_id: {user_id}")
    
    # Get only the logged-in user's predictions
    predictions = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.id.desc()).all()
    print(f"[DEBUG] Found {len(predictions)} predictions for user {user_id}")
    
    if predictions:
        print(f"[DEBUG] First prediction: {predictions[0].to_dict()}")
    
    result = [p.to_dict() for p in predictions]
    print(f"[DEBUG] Returning {len(result)} predictions")
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
