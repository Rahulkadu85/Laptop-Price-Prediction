"""
Lists all files in the project and categorizes them by type
"""
import os
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))

# File categories
text_extensions = ['.py', '.js', '.html', '.css', '.txt', '.md', '.json', '.yml', '.yaml']
binary_extensions = ['.pkl', '.pickle', '.db', '.sqlite', '.sqlite3']

print("=" * 70)
print("PROJECT FILES OVERVIEW")
print("=" * 70)

# Get all files
all_files = []
for root, dirs, files in os.walk(base_dir):
    # Skip __pycache__
    if '__pycache__' in root:
        continue
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, base_dir)
        all_files.append((rel_path, file))

# Categorize
text_files = []
binary_files = []
other_files = []

for rel_path, filename in all_files:
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in text_extensions:
        text_files.append((rel_path, filename))
    elif ext in binary_extensions:
        binary_files.append((rel_path, filename))
    else:
        other_files.append((rel_path, filename))

# Print text files
print("\n✅ TEXT FILES (Safe to open in editor):")
print("-" * 70)
for rel_path, filename in sorted(text_files):
    file_path = os.path.join(base_dir, rel_path)
    size = os.path.getsize(file_path) / 1024
    print(f"  {rel_path:50s} ({size:>6.1f} KB)")

# Print binary files
print("\n⚠️  BINARY FILES (Will show encoding error if opened):")
print("-" * 70)
for rel_path, filename in sorted(binary_files):
    file_path = os.path.join(base_dir, rel_path)
    size = os.path.getsize(file_path) / 1024
    print(f"  {rel_path:50s} ({size:>6.1f} KB)")

# Print other files
if other_files:
    print("\n📄 OTHER FILES:")
    print("-" * 70)
    for rel_path, filename in sorted(other_files):
        file_path = os.path.join(base_dir, rel_path)
        size = os.path.getsize(file_path) / 1024
        print(f"  {rel_path:50s} ({size:>6.1f} KB)")

print("\n" + "=" * 70)
print(f"Total: {len(text_files)} text files, {len(binary_files)} binary files")
print("=" * 70)

print("\n💡 TIP: If you see 'binary or unsupported encoding' error:")
print("   - For .pkl or .db files: This is NORMAL - use Python scripts to work with them")
print("   - For .py files: Run 'python fix_encoding.py' to fix encoding issues")
