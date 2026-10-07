import json

with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

terms = [
    'reinforcement learning', 'q-learning', 'bellman', 'markov',
    'recommender', 'collaborative filtering', 'two-tower',
    'graph neural', 'gnn',
    'time series', 'arima', 'prophet', 'forecasting',
    'quantization', 'gguf', 'awq', 'int8', 'ptq',
    'shap', 'lime', 'explainable', 'xai',
    'speech', 'whisper', 'tts', 'audio',
    'chain-of-thought', 'reasoning', 'mcts', 'test-time'
]

print('=== CHECKING CONCEPTS & TOPICS FOR DOMAIN COVERAGE ===')
for term in terms:
    found_c = []
    for c in concepts:
        title = c.get('title', '').lower()
        defn = c.get('def', '').lower()
        terms_txt = ' '.join([t.get('term', '') + ' ' + t.get('desc', '') for t in c.get('core_terms', []) if isinstance(t, dict)]).lower()
        if term in title or term in defn or term in terms_txt:
            found_c.append(c['id'])

    found_t = []
    for t in topics:
        label = t.get('label', '').lower()
        subs = ' '.join(t.get('subtopics', [])).lower()
        if term in label or term in subs:
            found_t.append(t['id'])

    print(f'{term:<25} -> Topics: {len(found_t):<2} | Concepts: {len(found_c):<2}')
