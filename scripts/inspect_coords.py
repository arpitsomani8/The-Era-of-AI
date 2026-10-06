import json

with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

for cat in ['math', 'data', 'ml', 'eval', 'dl', 'genai', 'mlops', 'swe_cloud']:
    t_cat = [t for t in topics if t.get('category') == cat]
    print(f"=== {cat} ({len(t_cat)} topics) ===")
    for t in t_cat:
        print(f"  [{t['id']}] {t['label']} -> x: {t.get('x')}, y: {t.get('y')}")
