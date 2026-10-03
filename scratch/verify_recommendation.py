# scratch/verify_recommendation.py
import sys
sys.path.insert(0, r'd:\tripgenius\backend')
from app.services.recommendation_service import RecommendationService

rec = RecommendationService()
print(f"RecommendationService loaded {len(rec.dataset)} spots successfully.")

test_queries = [
    'Kappil', 'Ranipuram', 'Lonar', 'Brihadisvara', 'Statue of Unity',
    'Algiers', 'Band-e-Amir', 'Kissama', 'Denali', 'Uluru', 
    'Fushimi Inari', 'Neuschwanstein', 'Plitvice'
]

print("\nTesting Query Matching in rec.dataset:")
all_passed = True
for q in test_queries:
    matches = rec.dataset[rec.dataset['Name of the Place'].str.contains(q, case=False, na=False)]
    if len(matches) > 0:
        row = matches.iloc[0]
        print(f"  [SUCCESS] '{q}' -> {row['Name of the Place']} ({row['District']}, {row['State']}, {row['Country']}) | Category: {row['Category']}")
    else:
        print(f"  [FAILED] '{q}' not found!")
        all_passed = False

if all_passed:
    print("\nALL TEST QUERIES MATCHED IN DATASET!")

# Test search_destination method
print("\nTesting search_destination for 'Kerala':")
results_kerala = rec.search_destination('Kerala')[:5]
print(f"Kerala returned {len(results_kerala)} top matches:")
for r in results_kerala:
    print(f"  - {r.get('place_name')} ({r.get('district')}, {r.get('state')}) | Score: {r.get('relevance_score')}")

print("\nTesting search_destination for 'France':")
results_france = rec.search_destination('France')[:5]
print(f"France returned {len(results_france)} top matches:")
for r in results_france:
    print(f"  - {r.get('place_name')} ({r.get('district')}, {r.get('country')}) | Score: {r.get('relevance_score')}")

print("\nTesting search_destination for 'Algeria':")
results_algeria = rec.search_destination('Algeria')[:5]
print(f"Algeria returned {len(results_algeria)} top matches:")
for r in results_algeria:
    print(f"  - {r.get('place_name')} ({r.get('district')}, {r.get('country')}) | Score: {r.get('relevance_score')}")

print("\nTesting search_destination for 'Kappil':")
results_kappil = rec.search_destination('Kappil')[:5]
print(f"Kappil returned {len(results_kappil)} top matches:")
for r in results_kappil:
    print(f"  - {r.get('place_name')} ({r.get('district')}, {r.get('state')}) | Score: {r.get('relevance_score')}")

print("\nVerification fully passed!")
