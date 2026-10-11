import json

with open('src/data/concepts.json', encoding='utf-8') as f:
    items = json.load(f)

for i, item in enumerate(items):
    if item.get('category') == 'math':
        print(f"{i:2d}: {item['id']} | {item['title']}")
