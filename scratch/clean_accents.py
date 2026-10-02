# scratch/clean_accents.py
import unicodedata
import pandas as pd

def clean_to_ascii(text):
    if not isinstance(text, str):
        return text
    # First normalize known punctuation
    t = text.replace('\u2019', "'").replace('\u2018', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = t.replace('\u2014', ' - ').replace('\u2013', ' - ')
    # NFKD decomposition replaces accented characters (e.g. Î -> I, é -> e)
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    return ' '.join(t.split())

for path in [r'D:\tripgenius\database\tourism.csv', r'D:\tripgenius\backend\tourism.csv']:
    df = pd.read_csv(path)
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(clean_to_ascii)

    # Final deduplication by lowercase name
    df['lower_name'] = df['Name of the Place'].str.strip().str.lower()
    df = df.drop_duplicates(subset=['lower_name'], keep='first').drop(columns=['lower_name'])

    df.to_csv(path, index=False, encoding='utf-8')
    print(f'Cleaned {path}: {len(df)} rows, 0 non-ASCII chars.')
