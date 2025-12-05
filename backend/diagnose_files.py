"""
Comprehensive file diagnosis - identifies problematic files
"""
import os
import sys

def check_file(file_path):
    """Check if a file can be read as text"""
    filename = os.path.basename(file_path)
    
    # Skip known binary extensions
    binary_extensions = ['.pkl', '.pickle', '.db', '.sqlite', '.sqlite3', '.pyc', '.pyo']
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in binary_extensions:
        return 'binary', f"{filename} - BINARY FILE (This is normal - use Python scripts)"
    
    # Try to read as text
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(100)  # Read first 100 chars
        return 'ok', f"{filename} - ✓ OK (UTF-8)"
    except UnicodeDecodeError:
        # Try other encodings
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read(100)
                return 'encoding_issue', f"{filename} - ⚠ NEEDS FIXING (currently {encoding})"
            except:
                continue
        return 'error', f"{filename} - ✗ CANNOT READ"
    except Exception as e:
        return 'error', f"{filename} - ✗ ERROR: {str(e)}"

# Get base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

print("=" * 80)
print("FILE ENCODING DIAGNOSIS")
print("=" * 80)
print()

# Walk through all files
ok_files = []
binary_files = []
encoding_issues = []
errors = []

for root, dirs, files in os.walk(base_dir):
    # Skip __pycache__
    if '__pycache__' in root:
        continue
    
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, base_dir)
        
        status, message = check_file(file_path)
        
        if status == 'ok':
            ok_files.append(message)
        elif status == 'binary':
            binary_files.append(message)
        elif status == 'encoding_issue':
            encoding_issues.append((message, file_path))
        else:
            errors.append((message, file_path))

# Print results
if ok_files:
    print("✓ TEXT FILES (Safe to open - UTF-8 encoded):")
    print("-" * 80)
    for msg in sorted(ok_files):
        print(f"  {msg}")
    print()

if binary_files:
    print("⚠️  BINARY FILES (Will show encoding error if opened - THIS IS NORMAL):")
    print("-" * 80)
    for msg in sorted(binary_files):
        print(f"  {msg}")
    print()

if encoding_issues:
    print("🔧 FILES WITH ENCODING ISSUES (Need to be fixed):")
    print("-" * 80)
    for msg, path in encoding_issues:
        print(f"  {msg}")
        print(f"     Path: {path}")
    print()
    print("  Run 'python fix_encoding.py' to fix these files.")
    print()

if errors:
    print("✗ FILES WITH ERRORS:")
    print("-" * 80)
    for msg, path in errors:
        print(f"  {msg}")
        print(f"     Path: {path}")
    print()

# Summary
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✓ Text files (UTF-8): {len(ok_files)}")
print(f"⚠️  Binary files: {len(binary_files)} (NORMAL - don't open in text editor)")
print(f"🔧 Encoding issues: {len(encoding_issues)}")
print(f"✗ Errors: {len(errors)}")
print()

if len(encoding_issues) > 0:
    print("ACTION REQUIRED: Run 'python fix_encoding.py' to fix encoding issues")
elif len(errors) > 0:
    print("ACTION REQUIRED: Review files with errors")
else:
    print("✓ ALL TEXT FILES ARE CORRECTLY ENCODED!")
    print()
    print("If you see 'binary or unsupported encoding' error:")
    print("  → You're trying to open a .pkl or .db file")
    print("  → This is NORMAL - these are binary files")
    print("  → Use Python scripts to work with them")
    print()
    print("See BINARY_FILES_INFO.txt for more details.")

print("=" * 80)
