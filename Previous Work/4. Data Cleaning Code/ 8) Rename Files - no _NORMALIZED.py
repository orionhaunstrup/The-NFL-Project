import os

# Folder where the script is located
folder = os.path.dirname(os.path.abspath(__file__))

print(f"Looking in folder: {folder}")

found_csv = False
for filename in os.listdir(folder):
    if filename.endswith(".csv"):
        found_csv = True
        print(f"Found .csv file: {filename}")

        # Remove "NORMALIZED_" from the start of the filename if present
        if filename.startswith("NORMALIZED_"):
            new_name = filename[len("NORMALIZED_"):]  # strip the prefix
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed {filename} → {new_name}")

if not found_csv:
    print("No .csv files found in this folder.")
