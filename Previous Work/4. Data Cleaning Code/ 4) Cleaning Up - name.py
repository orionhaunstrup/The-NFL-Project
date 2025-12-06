import os

# Folder containing the CSV files
folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if not filename.endswith(".csv"):
        continue

    if filename.endswith(" copy.csv"):
        new_name = filename.replace(" copy.csv", ".csv")
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name}")
