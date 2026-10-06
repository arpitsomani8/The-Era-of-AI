# scripts/audit_mindmap_connections.py
import json

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

node_dict = {n['id']: n for n in nodes}
all_ids = set(node_dict.keys())

print(f"Total nodes: {len(nodes)}")

broken_connections = []
duplicate_connections = []
all_edges = set()

for n in nodes:
    conns = n.get('connections', [])
    seen = set()
    for target in conns:
        if target not in all_ids:
            broken_connections.append((n['id'], target))
        if target in seen:
            duplicate_connections.append((n['id'], target))
        seen.add(target)
        # Undirected edge representation
        edge = tuple(sorted([n['id'], target]))
        all_edges.add(edge)

print(f"Total unique edges: {len(all_edges)}")
print(f"Broken connections: {len(broken_connections)} -> {broken_connections}")
print(f"Duplicate connections: {len(duplicate_connections)} -> {duplicate_connections}")

# Print connections count per node
print("\n=== CONNECTIONS PER NODE ===")
for n in sorted(nodes, key=lambda x: (x.get('level', 1), x.get('category'), x['id'])):
    print(f"[{n['id']:<30}] (Level {n.get('level')}) -> {n.get('connections')}")
