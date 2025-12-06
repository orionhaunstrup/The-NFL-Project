import os
import re

# Work in current directory
folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.startswith("FootballDB_Passing_"):
        continue

    # Extract year
    m = re.search(r"(\d{4})", filename)
    if not m:
        print(f"Could not find year in {filename}, skipping.")
        continue
    year = m.group(1)

    # Get file extension
    ext = os.path.splitext(filename)[1]

    # New filename
    new_name = f"NFL_Passing_{year}{ext}"

    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, new_name)

    # Rename file
    os.rename(old_path, new_path)
    print(f"Renamed {filename} → {new_name}")
