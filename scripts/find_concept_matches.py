import json

with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

queries = [
    "Principal Component Analysis",
    "YOLO",
    "Subword Tokenization",
    "Tokens, Tokenization",
    "Positional Encodings",
    "LangChain",
    "Learning Rate Schedules",
    "Learning Rate Warmup"
]

for q in queries:
    print(f"\n--- Search: {q} ---")
    matches = [c for c in concepts if q.lower() in c.get('title', '').lower() or q.lower() in c.get('raw_subtopic', '').lower() or q.lower() in c.get('raw_sub', '').lower()]
    for m in matches:
        print(f"  ID: {m['id']} | Topic: {m.get('topic_id')} | Subtopic: {m.get('raw_subtopic') or m.get('raw_sub')} | Title: {m.get('title')}")
