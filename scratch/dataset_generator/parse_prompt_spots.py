# scratch/dataset_generator/parse_prompt_spots.py
import re

def parse_prompt_spots(prompt_file):
    with open(prompt_file, 'r', encoding='utf-8') as f:
        text = f.read()

    results = []

    # 1. Parse Countries
    country_blocks = [
        ("Argentina", "Argentina", r'Argentina:\s*([^.\n]+)'),
        ("Australia", "Australia", r'Australia:\s*([^.\n]+)'),
        ("Bhutan", "Bhutan", r'Bhutan:\s*([^.\n]+)'),
        ("Brazil", "Brazil", r'Brazil:\s*([^.\n]+)'),
        ("Canada", "Canada", r'Canada:\s*([^.\n]+)'),
        ("China", "China", r'China:\s*([^.\n]+)'),
        ("Egypt", "Egypt", r'Egypt:\s*([^.\n]+)'),
        ("France", "France", r'France:\s*([^.\n]+)'),
        ("Germany", "Germany", r'Germany:\s*([^.\n]+)'),
        ("Greece", "Greece", r'Greece:\s*([^.\n]+)'),
        ("Italy", "Italy", r'Italy:\s*([^.\n]+)'),
        ("Japan", "Japan", r'Japan:\s*([^.\n]+)'),
        ("Malaysia", "Malaysia", r'Malaysia:\s*([^.\n]+)'),
        ("Nepal", "Nepal", r'Nepal:\s*([^.\n]+)'),
        ("New Zealand", "New Zealand", r'New Zealand:\s*([^.\n]+)'),
        ("Philippines", "Philippines", r'Philippines:\s*([^.\n]+)'),
        ("South Africa", "South Africa", r'South Africa:\s*([^.\n]+)'),
        ("South Korea", "South Korea", r'South Korea:\s*([^.\n]+)'),
        ("Spain", "Spain", r'Spain:\s*([^.\n]+)'),
        ("Sri Lanka", "Sri Lanka", r'Sri Lanka:\s*([^.\n]+)'),
        ("Switzerland", "Switzerland", r'Switzerland:\s*([^.\n]+)'),
        ("Thailand", "Thailand", r'Thailand:\s*([^.\n]+)'),
        ("Turkey", "Turkey", r'Turkey:\s*([^.\n]+)'),
        ("UAE", "UAE", r'UAE:\s*([^.\n]+)'),
        ("United Kingdom", "United Kingdom", r'United Kingdom:\s*([^.\n]+)'),
        ("USA", "USA", r'USA:\s*([^.\n]+)')
    ]

    for country, default_dist, pattern in country_blocks:
        m = re.search(pattern, text)
        if m:
            raw_items = m.group(1).split(',')
            for item in raw_items:
                item_clean = item.strip()
                # strip trailing phrases like "and other destinations"
                item_clean = re.sub(r'\s+and\s+other\s+.*$', '', item_clean, flags=re.IGNORECASE)
                item_clean = re.sub(r'\s+and\s+numerous\s+.*$', '', item_clean, flags=re.IGNORECASE)
                if item_clean and len(item_clean) > 2 and not item_clean.lower().startswith('and '):
                    results.append({
                        'Name': item_clean,
                        'District': default_dist,
                        'State': country,
                        'Country': country
                    })

    # Indonesia special block
    indo_m = re.search(r'Indonesia:.*?(includes\s+Bali\s+destinations\s+such\s+as\s+[^;]+;[^;]+;[^;]+;[^;]+;[^;]+;[^;]+)', text, re.DOTALL)
    if indo_m:
        raw_indo = indo_m.group(1)
        # extract words between commas
        for piece in re.split(r'[,;]\s*', raw_indo):
            piece_clean = re.sub(r'^(?:includes|including|Java destinations including|Lombok destinations including|Sumatra destinations including|Komodo destinations including|Sulawesi destinations including)\s+', '', piece.strip(), flags=re.IGNORECASE)
            piece_clean = re.sub(r'\s+and\s+other\s+.*$', '', piece_clean, flags=re.IGNORECASE)
            piece_clean = re.sub(r'\s+and\s+numerous\s+.*$', '', piece_clean, flags=re.IGNORECASE)
            if piece_clean and len(piece_clean) > 2 and not piece_clean.lower().startswith('and '):
                results.append({
                    'Name': piece_clean,
                    'District': 'Indonesia',
                    'State': 'Indonesia',
                    'Country': 'Indonesia'
                })

    # 2. Parse Indian States
    state_patterns = [
        ("Andhra Pradesh", r'For Andhra Pradesh,.*?includes\s+([^.\n]+)'),
        ("Arunachal Pradesh", r'For Arunachal Pradesh,.*?includes\s+([^.\n]+)'),
        ("Assam", r'For Assam,.*?includes\s+([^.\n]+)'),
        ("Bihar", r'For Bihar,.*?includes\s+([^.\n]+)'),
        ("Chhattisgarh", r'For Chhattisgarh,.*?includes\s+([^.\n]+)'),
        ("Goa", r'For Goa,.*?Palolem:\s*([^.\n]+)'),
        ("Gujarat", r'For Gujarat,.*?includes\s+([^.\n]+)'),
        ("Haryana", r'For Haryana,.*?include\s+([^.\n]+)'),
        ("Himachal Pradesh", r'For Himachal Pradesh,.*?include\s+([^.\n]+)'),
        ("Jharkhand", r'For Jharkhand,.*?include\s+([^.\n]+)'),
        ("Karnataka", r'For Karnataka,.*?extensive:\s*([^.\n]+)'),
        ("Kerala", r'For Kerala,.*?such as\s+([^.\n]+)')
    ]

    for state, pattern in state_patterns:
        m = re.search(pattern, text)
        if m:
            raw_items = m.group(1).split(',')
            for item in raw_items:
                item_clean = item.strip()
                item_clean = re.sub(r'\s+and\s+other\s+.*$', '', item_clean, flags=re.IGNORECASE)
                item_clean = re.sub(r'\s+and\s+additional\s+.*$', '', item_clean, flags=re.IGNORECASE)
                item_clean = re.sub(r'\s+and\s+numerous\s+.*$', '', item_clean, flags=re.IGNORECASE)
                item_clean = re.sub(r'\s+and\s+many\s+more\s+.*$', '', item_clean, flags=re.IGNORECASE)
                if item_clean and len(item_clean) > 2 and not item_clean.lower().startswith('and '):
                    results.append({
                        'Name': item_clean,
                        'District': state,
                        'State': state,
                        'Country': 'India'
                    })

    return results

if __name__ == '__main__':
    spots = parse_prompt_spots(r'd:\tripgenius\scratch\latest_user_prompt.txt')
    print(f'Extracted {len(spots)} spots directly from prompt.')
    print('Sample spots:', spots[:5])
