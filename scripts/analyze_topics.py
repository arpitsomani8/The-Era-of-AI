import json

with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

for t in topics:
    subs = len(t.get('subtopics', []))
    print(f"{t['category']:<8} | {t['id']:<20} | {t['label']} ({subs} subtopics)")
