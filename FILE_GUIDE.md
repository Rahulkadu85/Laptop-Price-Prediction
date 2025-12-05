# Laptop Price Prediction - File Guide

## 📁 Project Structure

### ✅ Text Files (Safe to Edit)
These files can be opened and edited in any text editor:

- **Python Files (*.py)** - Application code
  - `app.py` - Main Flask application
  - `check_db.py` - Database verification script
  - `verify_database.py` - Comprehensive database check
  - `migrate_database.py` - Database migration script
  - `fix_encoding.py` - Encoding fix utility
  - `test_prediction_save.py` - Test script

- **Configuration Files**
  - `requirements.txt` - Python dependencies
  - `.gitignore` - Git ignore patterns

- **Web Files**
  - `templates/index.html` - HTML template
  - `static/css/style.css` - Stylesheets
  - `static/js/app.js` - JavaScript frontend

### ⚠️ Binary Files (DO NOT EDIT AS TEXT)
These files will show as "binary or unsupported encoding" if you try to open them in a text editor. **This is normal and expected**:

- **Machine Learning Models** (`.pkl` files)
  - `model.pkl` - Trained prediction model
  - `encoder.pkl` - Label encoder for brands
  - `scaler.pkl` - Feature scaler
  
  **Note:** These are serialized Python objects created by scikit-learn. They cannot be edited as text. If you need to modify them, retrain the model.

- **Database Files**
  - `laptop_price.db` - SQLite database
  
  **Note:** This is a binary database file. Use SQLite tools or Python scripts to interact with it, not a text editor.

## 🔧 If You See Encoding Errors

If you get "unsupported text encoding" errors on a Python file:

1. Run the encoding fix script:
   ```bash
   cd backend
   python fix_encoding.py
   ```

2. Close and reopen the file in your editor

3. If the issue persists, the file might be corrupted. Restore from git or recreate it.

## 🗄️ Working with Binary Files

### For Database (`.db` files):
```bash
# View database contents
python check_db.py

# Verify database structure
python verify_database.py

# Migrate database schema
python migrate_database.py
```

### For Model Files (`.pkl` files):
```python
# Load and inspect in Python
import pickle

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    print(type(model))
```

## 📝 Summary

- **If it's a `.py`, `.js`, `.html`, `.css`, `.txt` file** → Safe to edit in text editor
- **If it's a `.pkl` or `.db` file** → Binary file, use Python scripts to work with it
- **If you see "binary or unsupported encoding"** → The file is supposed to be binary!

## 🚀 Quick Commands

```bash
# Check database status
python verify_database.py

# Fix encoding issues in text files
python fix_encoding.py

# Run Flask application
python app.py
```
