import json
from test_new_layout import proposed_coords

# 1. Update allNodes.json
with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    all_nodes = json.load(f)

updated_all_nodes = 0
for n in all_nodes:
    nid = n['id']
    if nid in proposed_coords:
        n['x'] = proposed_coords[nid]['x']
        n['y'] = proposed_coords[nid]['y']
        updated_all_nodes += 1
    else:
        print(f"Warning: {nid} not found in proposed_coords")

with open('src/data/allNodes.json', 'w', encoding='utf-8') as f:
    json.dump(all_nodes, f, indent=2, ensure_ascii=False)
print(f"Updated {updated_all_nodes} nodes in src/data/allNodes.json")

# 2. Update topics.json
with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

updated_topics = 0
for t in topics:
    tid = t['id']
    if tid in proposed_coords:
        t['x'] = proposed_coords[tid]['x']
        t['y'] = proposed_coords[tid]['y']
        updated_topics += 1

with open('src/data/topics.json', 'w', encoding='utf-8') as f:
    json.dump(topics, f, indent=2, ensure_ascii=False)
print(f"Updated {updated_topics} nodes in src/data/topics.json")

# 3. Update hubNodes.json
with open('src/data/hubNodes.json', 'r', encoding='utf-8') as f:
    hubs = json.load(f)

updated_hubs = 0
for h in hubs:
    hid = h['id']
    if hid in proposed_coords:
        h['x'] = proposed_coords[hid]['x']
        h['y'] = proposed_coords[hid]['y']
        updated_hubs += 1

with open('src/data/hubNodes.json', 'w', encoding='utf-8') as f:
    json.dump(hubs, f, indent=2, ensure_ascii=False)
print(f"Updated {updated_hubs} nodes in src/data/hubNodes.json")
