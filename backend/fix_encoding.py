"""
Script to fix encoding issues in Python files
Converts all .py files to UTF-8 encoding
"""
import os
import glob

def fix_file_encoding(file_path):
    """Try to read and re-save file as UTF-8"""
    try:
        print(f"Checking: {os.path.basename(file_path)}")
        
        # Try reading with different encodings
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        content = None
        original_encoding = None
        
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                original_encoding = encoding
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"  ✗ Could not decode file")
            return False
        
        print(f"  Read successfully with: {original_encoding}")
        
        # Write back as UTF-8 with BOM removed
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            # Remove BOM if present
            if content.startswith('\ufeff'):
                content = content[1:]
            f.write(content)
        
        if original_encoding != 'utf-8':
            print(f"  ✓ Converted from {original_encoding} to UTF-8")
            return True
        else:
            print(f"  ✓ Already UTF-8, re-saved cleanly")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

# Get base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("FIXING FILE ENCODINGS")
print("=" * 60)
print()

# Find all Python files
py_files = []
for pattern in ['*.py', '**/*.py']:
    py_files.extend(glob.glob(os.path.join(base_dir, pattern), recursive=True))

# Remove duplicates
py_files = list(set(py_files))

# Also check JS files
js_files = glob.glob(os.path.join(base_dir, 'static', 'js', '*.js'))
py_files.extend(js_files)

converted_count = 0
processed_count = 0

for file_path in py_files:
    # Skip __pycache__ directories
    if '__pycache__' in file_path:
        continue
    
    if fix_file_encoding(file_path):
        converted_count += 1
    processed_count += 1
    print()

print("=" * 60)
print(f"COMPLETE: Processed {processed_count} files")
print(f"Converted: {converted_count} files")
print("=" * 60)

if converted_count == 0:
    print("\n✓ All files are already UTF-8 encoded!")
else:
    print(f"\n✓ Fixed encoding for {converted_count} files")
    print("\nPlease restart your text editor to see the changes.")
