# scratch/dataset_generator/data_generator.py
import sys, os, re, unicodedata
import pandas as pd
from collections import Counter
from metadata_enricher import build_spot_record
from parse_prompt_spots import parse_prompt_spots

ORIGINAL_CSV = r'D:\tripgenius\database\tourism.csv'
BACKEND_CSV = r'D:\tripgenius\backend\tourism.csv'
PROMPT_FILE = r'd:\tripgenius\scratch\latest_user_prompt.txt'

df_orig = pd.read_csv(ORIGINAL_CSV)
print(f"Current original dataset count: {len(df_orig)}")

existing_names = set(df_orig['Name of the Place'].str.strip().str.lower())
new_records = []
seen = set(existing_names)

def add_entry(name, district, state, country, category=None, hint=""):
    norm = name.strip().lower()
    if not norm or norm in seen or len(norm) < 3:
        return
    seen.add(norm)
    rec = build_spot_record(name, district, state, country, category, hint)
    new_records.append(rec)

# Step 1: Add spots parsed directly from the user's latest prompt
print("1. Parsing user prompt spots...")
prompt_spots = parse_prompt_spots(PROMPT_FILE)
for sp in prompt_spots:
    add_entry(sp['Name'], sp['District'], sp['State'], sp['Country'])

print(f"Added from prompt: {len(new_records)} unique spots.")
