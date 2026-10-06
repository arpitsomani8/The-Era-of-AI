import json

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

print(f"Total nodes: {len(nodes)}\n")

categories = ['center', 'math', 'data', 'ml', 'eval', 'dl', 'genai', 'mlops', 'swe_cloud']

for cat in categories:
    cat_nodes = [n for n in nodes if n.get('category') == cat]
    print(f"=== CATEGORY: {cat} ({len(cat_nodes)} nodes) ===")
    for n in sorted(cat_nodes, key=lambda x: (x.get('level', 1), x['id'])):
        print(f"  [{n['id']}] Level {n.get('level')} | Pos: ({n['x']}, {n['y']}) | Label: \"{n['label']}\" | Conns: {n.get('connections', [])}")
    print()
