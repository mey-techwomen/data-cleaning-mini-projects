Data Cleaning Mini Projects (Python + pandas)

This repository contains hands-on mini projects focused on cleaning messy, real-world style datasets using Python and pandas. The goal is to practice practical data preparation skills such as handling missing values, trimming/standardizing text fields, validating data, and creating clean outputs ready for analysis.

Project 1: Customer Data Cleaning
Objective

Clean a messy customer dataset and generate a cleaned CSV with:

standardized column names

trimmed text fields

parsed numeric values

derived quality flags

de-duplicated records

Input Dataset

File path:

data/raw/customer_messy.csv

Example issues handled:

extra spaces in names/cities/emails

missing values (email / age)

inconsistent phone formats

invalid emails (basic validation)

duplicate customer rows

header formatting issues (quotes/BOM/case)

Output Dataset

File path:

data/cleaned/customers_cleaned.csv

New columns generated:

phone_clean → digits-only phone number

email_valid → boolean flag for basic email validity

Folder Structure
data-cleaning-mini-projects/
  clean_customerdata.py
  data/
    raw/
      customer_messy.csv
    cleaned/
      customers_cleaned.csv

How to Run
1) Install dependencies
pip install pandas

2) Update the base directory (if needed)

In clean_customerdata.py, update:

BASE_DIR = Path("/Users/Aradh/Documents/Python/DATA_Science")

3) Run the script
python clean_customerdata.py

Notes

The script reads the CSV header safely and normalizes it (handles quotes/BOM/extra spaces/case).

Age missing values are filled using the dataset median; if median cannot be computed, a default value is used.

This is a beginner-friendly project designed to build a public portfolio and demonstrate practical data cleaning skills.

Next Improvements (Planned)

Stronger email validation and email cleaning (standardization)

Robust phone formatting (country code support)

Generate a cleaning_report.txt summary (counts of fixes/invalids)

Add a notebook for quick EDA on cleaned data
