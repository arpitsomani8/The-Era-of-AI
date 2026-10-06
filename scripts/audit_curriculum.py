import json
from collections import defaultdict, Counter

with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

print('=== 1. TOPIC LEVEL AUDIT ===')
topic_titles = [t['label'] for t in topics]
print(f'Total topics: {len(topics)}')
topic_counts = Counter(topic_titles)
duplicates_t = {k: v for k, v in topic_counts.items() if v > 1}
print(f'Duplicate topic labels: {duplicates_t}')

print('\n=== 2. SUBTOPIC LEVEL AUDIT ===')
subtopic_to_topics = defaultdict(list)
for t in topics:
    for s in t.get('subtopics', []):
        subtopic_to_topics[s.strip().lower()].append(t['label'])

duplicates_s = {k: v for k, v in subtopic_to_topics.items() if len(v) > 1}
print(f'Subtopics appearing in multiple topics: {len(duplicates_s)}')
for k, v in duplicates_s.items():
    print(f'  - "{k}" in: {v}')

print('\n=== 3. CONCEPT ID & TITLE AUDIT ===')
concept_ids = [c['id'] for c in concepts]
concept_id_counts = Counter(concept_ids)
dup_ids = {k: v for k, v in concept_id_counts.items() if v > 1}
print(f'Duplicate concept IDs: {dup_ids}')

concept_titles = [c.get('title', '').strip().lower() for c in concepts]
concept_title_counts = Counter(concept_titles)
dup_titles = {k: v for k, v in concept_title_counts.items() if v > 1}
print(f'Duplicate concept titles: {dup_titles}')

print('\n=== 4. SIMILAR / OVERLAPPING SUBTOPIC CHECK ===')
all_subs = list(subtopic_to_topics.keys())
similar_pairs = []
for i in range(len(all_subs)):
    for j in range(i + 1, len(all_subs)):
        s1, s2 = all_subs[i], all_subs[j]
        # Check if identical words or high overlap
        words1 = set(s1.replace(',', '').replace('(', '').replace(')', '').replace('&', '').split())
        words2 = set(s2.replace(',', '').replace('(', '').replace(')', '').replace('&', '').split())
        overlap = words1.intersection(words2)
        if len(overlap) >= 3 and abs(len(words1) - len(words2)) <= 2:
            similar_pairs.append((s1, s2, overlap))

print(f'Potentially overlapping subtopics ({len(similar_pairs)} found):')
for s1, s2, ov in similar_pairs[:20]:
    print(f'  - "{s1}" vs "{s2}" (Shared: {ov})')

print('\n=== 5. TOPICS BY SECTION / CATEGORY ===')
category_topics = defaultdict(list)
for t in topics:
    cat = t.get('category', 'unknown')
    category_topics[cat].append((t['id'], t['label'], len(t.get('subtopics', []))))

for cat, t_list in category_topics.items():
    print(f'\n--- Category: {cat} ({len(t_list)} topics, {sum(x[2] for x in t_list)} subtopics) ---')
    for tid, tlbl, scnt in t_list:
        print(f'  [{tid}] {tlbl} ({scnt} subtopics)')
