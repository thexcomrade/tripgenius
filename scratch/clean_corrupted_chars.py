# scratch/clean_corrupted_chars.py
import sys, re
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

for path in [r'D:\tripgenius\database\tourism.csv', r'D:\tripgenius\backend\tourism.csv']:
    df = pd.read_csv(path)
    print(f'Checking {path} ({len(df)} rows)...')

    # Replace common unicode corruptions
    def fix_text(val):
        if not isinstance(val, str):
            return val
        s = val
        # Fix smart apostrophes / quotes
        s = s.replace('\ufffd', "'")
        s = s.replace('â€™', "'")
        s = s.replace('â€œ', '"')
        s = s.replace('â€', '"')
        s = s.replace('â€”', ' — ')
        s = s.replace('â€“', ' — ')
        s = s.replace('â€˜', "'")
        s = s.replace('Ã©', 'e')
        s = s.replace('Ã', 'a')
        # Clean up double spaces
        s = re.sub(r'\s+', ' ', s).strip()
        return s

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(fix_text)

    # Check if Annapurna Base Camp is present
    abc_matches = df[df['Name of the Place'].str.lower() == 'annapurna base camp']
    if abc_matches.empty:
        new_row = {
            'Name of the Place': 'Annapurna Base Camp',
            'District': 'Gandaki',
            'Famous_For': 'Iconic high-altitude Himalayan trek in Nepal reaching 4,130m, surrounded by Annapurna I, Machapuchare and Hiunchuli',
            'Activities': 'High-altitude trekking, Teahouse stays, Machapuchare sunrise view, Hot spring bath at Jhinu, Alpine photography',
            'State': 'Gandaki Province',
            'Country': 'Nepal',
            'Category': 'Adventure',
            'Travel_Style': 'Adventure, Trekking, Expedition, Photography',
            'Best_Season': 'April to June, September to November',
            'Budget_Category': 'Moderate',
            'Duration_Days': 3
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        print('Added Annapurna Base Camp!')

    # Deduplicate again just in case
    df['lower_name'] = df['Name of the Place'].str.strip().str.lower()
    df = df.drop_duplicates(subset=['lower_name'], keep='first').drop(columns=['lower_name'])

    df.to_csv(path, index=False, encoding='utf-8')
    print(f'Saved cleaned {path}, total rows: {len(df)}')
