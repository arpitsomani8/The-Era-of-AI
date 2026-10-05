import json

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

def get_node_dims(node):
    is_root = node.get('level') == 0
    is_hub = node.get('level') == 1
    label_len = len(node.get('label', ''))
    char_width = 8.6 if is_root else (7.6 if is_hub else 6.8)
    text_width = round(label_len * char_width)
    left_offset = 36 if is_root else (30 if is_hub else 28)
    right_padding = 18
    min_width = 260 if is_root else (210 if is_hub else 180)
    node_w = max(min_width, text_width + left_offset + right_padding)
    node_h = 54 if is_root else (46 if is_hub else 40)
    return node_w, node_h

print(f"Total nodes: {len(nodes)}")
for n in nodes:
    w, h = get_node_dims(n)
    print(f"{n['id']:25} | lvl:{n.get('level', 2)} | cat:{n.get('category',''):7} | x:{n['x']:5} | y:{n['y']:5} | w:{w:3} | h:{h:2} | {n['label']}")

# Check collisions
collisions = []
margin_x = 24  # desired minimum gap between boxes
margin_y = 20

for i in range(len(nodes)):
    n1 = nodes[i]
    w1, h1 = get_node_dims(n1)
    l1, r1 = n1['x'] - w1 / 2, n1['x'] + w1 / 2
    t1, b1 = n1['y'] - h1 / 2, n1['y'] + h1 / 2

    for j in range(i + 1, len(nodes)):
        n2 = nodes[j]
        w2, h2 = get_node_dims(n2)
        l2, r2 = n2['x'] - w2 / 2, n2['x'] + w2 / 2
        t2, b2 = n2['y'] - h2 / 2, n2['y'] + h2 / 2

        # Check overlap including margin
        overlap_x = min(r1, r2) - max(l1, l2)
        overlap_y = min(b1, b2) - max(t1, t2)

        if overlap_x > 0 and overlap_y > 0:
            collisions.append((n1['id'], n2['id'], overlap_x, overlap_y, n1['label'], n2['label']))

print(f"\nTotal collisions: {len(collisions)}")
for c in collisions:
    print(f"Overlap {c[0]} vs {c[1]}: overlap_x={c[2]:.1f}px, overlap_y={c[3]:.1f}px")
