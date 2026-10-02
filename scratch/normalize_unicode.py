# scratch/normalize_unicode.py
import re
import pandas as pd

for path in [r'D:\tripgenius\database\tourism.csv', r'D:\tripgenius\backend\tourism.csv']:
    df = pd.read_csv(path)
    before = len(df)
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.replace('\u2019', "'", regex=False)
            df[col] = df[col].astype(str).str.replace('\u2018', "'", regex=False)
            df[col] = df[col].astype(str).str.replace('\u201c', '"', regex=False)
            df[col] = df[col].astype(str).str.replace('\u201d', '"', regex=False)
            df[col] = df[col].astype(str).str.replace('\u2014', ' - ', regex=False)
            df[col] = df[col].astype(str).str.replace('\u2013', ' - ', regex=False)
            df[col] = df[col].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()

    df['norm_key'] = df['Name of the Place'].str.lower().str.strip()
    df = df.drop_duplicates(subset=['norm_key'], keep='first').drop(columns=['norm_key'])
    after = len(df)
    df.to_csv(path, index=False, encoding='utf-8')
    print(f'{path}: {before} -> {after} rows (deduped {before - after})')
