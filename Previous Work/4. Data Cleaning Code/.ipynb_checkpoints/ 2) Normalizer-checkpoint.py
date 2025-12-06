import pandas as pd
import os
import glob
import re
import numpy as np
from tqdm import tqdm

# -------------------------------
# YEAR → N mapping (halved)
# -------------------------------
N_year = {
    1940: 10, 1941: 10, 1942: 10, 1943: 8, 1944: 10, 1945: 10, 1946: 10, 1947: 10, 1948: 10, 1949: 10,
    1950: 12, 1951: 12, 1952: 12, 1953: 12, 1954: 12, 1955: 12, 1956: 12, 1957: 12, 1958: 12, 1959: 12,
    1960: 22, 1961: 22, 1962: 22, 1963: 22, 1964: 22, 1965: 22,
    1966: 24, 1967: 25, 1968: 26, 1969: 26, 1970: 26, 1971: 26, 1972: 26, 1973: 26, 1974: 26, 1975: 26,
    1976: 28, 1977: 28, 1978: 28, 1979: 28, 1980: 28, 1981: 28, 1982: 28, 1983: 28, 1984: 28, 1985: 28,
    1986: 28, 1987: 28, 1988: 28, 1989: 28, 1990: 28, 1991: 28, 1992: 28, 1993: 28, 1994: 28,
    1995: 30, 1996: 30, 1997: 30, 1998: 30, 1999: 31, 2000: 31, 2001: 31,
    2002: 32, 2003: 32, 2004: 32, 2005: 32, 2006: 32, 2007: 32, 2008: 32, 2009: 32, 2010: 32,
    2011: 32, 2012: 32, 2013: 32, 2014: 32, 2015: 32, 2016: 32, 2017: 32, 2018: 32, 2019: 32,
    2020: 32, 2021: 32, 2022: 32, 2023: 32, 2024: 32
}
# Halve all N
for y in N_year:
    N_year[y] = N_year[y] // 2

# -------------------------------
# Work in this script's directory
# -------------------------------
input_folder = os.path.dirname(os.path.abspath(__file__))
csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

# -------------------------------
# Helper: convert numeric values (for all columns EXCEPT Completion % and QB passer rating)
# -------------------------------
def convert_value(v):
    if pd.isna(v) or str(v).strip() == "":
        return 0
    s = str(v).strip()
    if "/" in s:     # fraction
        try:
            a, b = s.split("/")
            return float(a) / float(b)
        except:
            return None
    try:
        return float(s)
    except:
        return None

# -------------------------------
# MAIN LOOP WITH PROGRESS BAR
# -------------------------------
for file_path in tqdm(csv_files, desc="Normalizing NFL CSV files", unit="file"):
    base = os.path.basename(file_path)

    # Extract year
    m = re.search(r"(19\d{2}|20\d{2})", base)
    if m:
        year = int(m.group(0))
        N = N_year.get(year, 3)  # fallback
    else:
        N = 3

    df = pd.read_csv(file_path)

    for col in df.columns[1:]:
        if col == "Completion %":
            # divide by 100
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) / 100
            continue

        if col == "QB passer rating":
            # divide by 100
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) / 100
            continue

        # Default: convert & normalize by Nth largest
        original_values = df[col]
        converted = original_values.apply(convert_value)

        if converted.isna().any() and not original_values.replace("", np.nan).isna().all():
            continue
        if converted.notna().sum() == 0:
            continue

        col_vals = converted.fillna(0)

        if col_vals.sum() == 0:
            df[col] = 0
            continue

        if len(col_vals) >= N:
            nth = col_vals.nlargest(N).iloc[-1]
        else:
            nth = col_vals.max()

        if nth == 0:
            nonzero = col_vals[col_vals > 0]
            if len(nonzero) == 0:
                df[col] = 0
                continue
            nth = nonzero.mean()

        df[col] = col_vals / nth

    # Save output
    df.to_csv(os.path.join(input_folder, f"NORMALIZED_{base}"), index=False)
