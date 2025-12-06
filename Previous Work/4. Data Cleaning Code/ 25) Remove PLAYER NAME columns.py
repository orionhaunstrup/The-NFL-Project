import os
import pandas as pd

def clean_qbdatacube():
    folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(folder, "HowGood - QBDataCube.csv")

    if not os.path.exists(file_path):
        print(f"QBDataCube.csv not found in {folder}")
        return

    df = pd.read_csv(file_path)

    # Identify extra PLAYER columns (any column containing "PLAYER", not the first one)
    cols_to_remove = [col for idx, col in enumerate(df.columns)
                      if idx != 0 and "PLAYER" in col.upper().replace(" ", "")]

    if cols_to_remove:
        df.drop(columns=cols_to_remove, inplace=True)
        print(f"Removed columns → {cols_to_remove}")
    else:
        print("No extra PLAYER columns to remove")

    df.to_csv(file_path, index=False)
    print(f"QBDataCube.csv cleaned and saved in {folder}")

if __name__ == "__main__":
    clean_qbdatacube()
