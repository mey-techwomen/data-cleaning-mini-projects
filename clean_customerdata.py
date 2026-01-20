"""
clean_customerdata.py

Mini Project: Customer Data Cleaning (pandas)
- Reads a messy customer CSV
- Normalizes header issues (quotes/BOM/spacing/case)
- Cleans basic fields (trim text, parse age)
- Creates helpful flags/derived columns (email_valid, phone_clean)
- Drops duplicates
- Saves cleaned output CSV

Update BASE_DIR to match your machine path.
"""

import pandas as pd
from pathlib import Path
import re

# ====== UPDATE THIS ONLY if your folder is different ======
BASE_DIR = Path("/Users/Aradh/Documents/Python/DATA_Science")

# Input (raw) CSV and output (cleaned) CSV locations
RAW_PATH = BASE_DIR / "data" / "raw" / "customer_messy.csv"
OUT_PATH = BASE_DIR / "data" / "cleaned" / "customers_cleaned.csv"

# Columns we expect after cleaning the header
REQUIRED_COLS = ["customer_id", "name", "email", "phone", "city", "age"]


def pick_delimiter(header_line: str) -> str:
    """
    Detect the delimiter by checking which candidate appears most in the header line.
    Works for common delimiters: comma, semicolon, tab, pipe.
    """
    candidates = [",", ";", "\t", "|"]
    counts = {d: header_line.count(d) for d in candidates}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else ","


def normalize_columns(cols) -> list[str]:
    """
    Normalize column names so downstream code can rely on consistent names.
    - remove BOM (invisible \ufeff)
    - trim whitespace
    - strip surrounding quotes
    - lower-case
    """
    cleaned = []
    for c in cols:
        c = str(c).replace("\ufeff", "").strip()
        c = c.strip('"').strip("'")
        cleaned.append(c.lower())
    return cleaned


def clean_phone(value) -> str:
    """Convert phone number to digits-only (e.g., '(469) 111-2222' -> '4691112222')."""
    if pd.isna(value):
        return ""
    return re.sub(r"\D", "", str(value))


def is_valid_email(value) -> bool:
    """
    Very basic email validation (good enough for a beginner mini-project).
    Flags missing emails and obvious invalid patterns like '@@'.
    """
    if pd.isna(value):
        return False
    email = str(value).strip()
    if email == "":
        return False
    if "@@" in email:
        return False
    return ("@" in email) and ("." in email) and (" " not in email)


def main() -> None:
    # Helpful prints during development (keep these; they show what file is used)
    print("RUNNING:", __file__)
    print("CSV PATH:", RAW_PATH)

    # 1) Validate input file exists
    if not RAW_PATH.exists():
        print("❌ CSV not found:", RAW_PATH)
        print("Fix: place customer_messy.csv in data/raw OR update BASE_DIR/RAW_PATH.")
        return

    # 2) Read the first line (header) as raw text
    #    We do this because some editors wrap the whole header in quotes like:
    #    "customer_id,name,email,phone,city,age"
    with open(RAW_PATH, "r", encoding="utf-8", errors="replace") as f:
        header_line = f.readline().strip()

    # If the entire header line is wrapped in quotes, remove them before splitting
    header_line = header_line.strip().strip('"').strip("'")

    # 3) Detect delimiter and build clean column list
    delim = pick_delimiter(header_line)
    raw_cols = [c.strip() for c in header_line.split(delim)]
    cols = normalize_columns(raw_cols)

    print("Detected delimiter:", repr(delim))
    print("Header columns:", cols)

    # 4) Read the data rows WITHOUT trusting the file header
    #    header=None + skiprows=1 means:
    #    - treat every row as data
    #    - skip the first header row we already handled manually
    df = pd.read_csv(RAW_PATH, header=None, skiprows=1, sep=delim, engine="python")

    # Fallback: If parsing collapses into 1 column, brute-force split on common delimiters
    if df.shape[1] == 1:
        df = pd.read_csv(
            RAW_PATH,
            header=None,
            skiprows=1,
            sep=r",|;|\t|\|",
            engine="python"
        )

    # 5) Ensure header and data column counts match before assigning
    if len(cols) != df.shape[1]:
        print("❌ Header/data column mismatch.")
        print("Header count:", len(cols), "| Data count:", df.shape[1])
        print("First row raw:", df.iloc[0].tolist())
        print("Fix: re-save CSV as plain UTF-8 CSV in TextEdit if needed.")
        return

    df.columns = cols

    # 6) Validate required columns exist
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        print("❌ Missing required columns:", missing)
        print("Columns found:", df.columns.tolist())
        return

    # 7) Basic cleaning: trim whitespace in text fields
    for col in ["name", "email", "phone", "city"]:
        df[col] = df[col].astype(str).str.strip()

    # 8) Convert age to numeric (invalid values become NaN)
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # Fill missing age with median; if median itself is NaN, use a sensible default
    median_age = df["age"].median()
    if pd.isna(median_age):
        median_age = 30
    df["age"] = df["age"].fillna(median_age)

    # 9) Add derived columns useful for analysis/quality checks
    df["phone_clean"] = df["phone"].apply(clean_phone)
    df["email_valid"] = df["email"].apply(is_valid_email)

    # 10) Drop duplicates (simple rule for this project)
    before = len(df)
    df = df.drop_duplicates(subset=["name", "email", "city", "age"], keep="first")
    after = len(df)

    # 11) Save cleaned dataset
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    # 12) Print a small summary
    print("✅ Success! Cleaned file saved to:", OUT_PATH)
    print("Rows before:", before, "| Rows after:", after)
    print("Invalid emails flagged:", int((~df["email_valid"]).sum()))


if __name__ == "__main__":
    main()
