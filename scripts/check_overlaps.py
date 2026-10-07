import json

with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

pairs_to_check = [
    ('pca', 'principal component'),
    ('cosine decay', 'learning rate'),
    ('yolo', 'object detection'),
    ('tokenization', 'wordpiece'),
    ('positional encoding', 'rope'),
    ('peft', 'lora'),
    ('langgraph', 'langchain')
]

for kw1, kw2 in pairs_to_check:
    print(f'\n=== Matches for: {kw1} & {kw2} ===')
    for t in topics:
        for s in t.get('subtopics', []):
            if kw1 in s.lower() and kw2 in s.lower():
                print(f'  [{t["id"]}] {t["label"]} -> "{s}"')
