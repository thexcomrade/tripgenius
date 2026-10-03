# scratch/dataset_generator/build_all_data.py
import sys, os, unicodedata, re, shutil
import pandas as pd
from collections import Counter
from metadata_enricher import build_spot_record
from parse_prompt_spots import parse_prompt_spots

sys.stdout.reconfigure(encoding='utf-8')

ORIGINAL_CSV = r'D:\tripgenius\database\tourism.csv'
BACKEND_CSV = r'D:\tripgenius\backend\tourism.csv'
PROMPT_FILE = r'd:\tripgenius\scratch\latest_user_prompt.txt'

df_orig = pd.read_csv(ORIGINAL_CSV)
print(f"Base dataset rows: {len(df_orig)}")

existing_names = set(df_orig['Name of the Place'].str.strip().str.lower())
seen_names = set(existing_names)
new_records = []

def add_spot(name, district, state, country, category=None, hint=""):
    name_clean = name.strip()
    norm = name_clean.lower()
    if not name_clean or norm in seen_names or len(name_clean) < 3:
        return
    seen_names.add(norm)
    rec = build_spot_record(name_clean, district, state, country, category, hint)
    new_records.append(rec)

# 1. User Prompt Spots
print("Extracting spots from latest user prompt...")
prompt_spots = parse_prompt_spots(PROMPT_FILE)
for sp in prompt_spots:
    add_spot(sp['Name'], sp['District'], sp['State'], sp['Country'])

print(f"Added {len(new_records)} spots from user prompt.")
