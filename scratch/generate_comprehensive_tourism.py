# scratch/generate_comprehensive_tourism.py
import sys, re, os, unicodedata, shutil
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

records = []
seen_names = set(existing_names)

def add(name, district, state, country, category, famous_for, activities, travel_style, best_season, budget, duration):
    name_clean = clean_ascii(name)
    norm = name_clean.lower()
    if not name_clean or norm in seen_names or len(name_clean) < 3:
        return
    seen_names.add(norm)
    records.append({
        'Name of the Place': name_clean,
        'District': clean_ascii(district),
        'Famous_For': clean_ascii(famous_for),
        'Activities': clean_ascii(activities),
        'State': clean_ascii(state),
        'Country': clean_ascii(country),
        'Category': category.strip(),
        'Travel_Style': travel_style.strip(),
        'Best_Season': best_season.strip(),
        'Budget_Category': budget.strip(),
        'Duration_Days': int(duration)
    })

print("Writing generation engine...")
