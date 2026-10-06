import json

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

print(f"Total nodes: {len(nodes)}")
for n in nodes:
    if n.get('level', 1) <= 1 or 'root' in n.get('id', ''):
        print(f"[{n.get('id')}] {n.get('label')} | Cat: {n.get('category')} | Level: {n.get('level')} | Pos: ({n.get('x')}, {n.get('y')}) | Connections: {n.get('connections')}")
