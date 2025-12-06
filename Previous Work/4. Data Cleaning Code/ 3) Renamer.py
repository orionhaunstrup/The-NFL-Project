import os

# Folder where the script is located
folder = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(folder):
    if filename.startswith("FootballDB_Passing_") and filename.endswith(".csv"):
        new_name = filename.replace("FootballDB_Passing_", "NFL_Passing_")
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {filename} → {new_name}")
