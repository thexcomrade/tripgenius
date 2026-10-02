# scratch/generate_all_destinations.py
import sys, os, unicodedata, re
import pandas as pd
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

ORIGINAL_CSV = r'D:\tripgenius\database\tourism.csv'
BACKEND_CSV = r'D:\tripgenius\backend\tourism.csv'

df_orig = pd.read_csv(ORIGINAL_CSV)
print(f'Starting with existing rows: {len(df_orig)}')
existing_names = set(df_orig['Name of the Place'].str.strip().str.lower())

def clean_ascii(text):
    if not isinstance(text, str):
        return str(text) if text is not None else ""
    t = text.replace('\u2019', "'").replace('\u2018', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = t.replace('\u2014', ' - ').replace('\u2013', ' - ')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    return ' '.join(t.split()).strip()

all_new_spots = []
seen = set(existing_names)

def add_spot(name, district, state, country, cat, famous, act, style, season, budget, days):
    c_name = clean_ascii(name)
    norm = c_name.lower()
    if not c_name or norm in seen or len(c_name) < 3:
        return
    seen.add(norm)
    all_new_spots.append({
        'Name of the Place': c_name,
        'District': clean_ascii(district),
        'Famous_For': clean_ascii(famous),
        'Activities': clean_ascii(act),
        'State': clean_ascii(state),
        'Country': clean_ascii(country),
        'Category': cat.strip(),
        'Travel_Style': style.strip(),
        'Best_Season': season.strip(),
        'Budget_Category': budget.strip(),
        'Duration_Days': int(days)
    })

print("Helper ready. Generating dataset...")
