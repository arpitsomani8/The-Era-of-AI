# scripts/solve_mindmap_layout.py
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
    w = max(min_width, text_width + left_offset + right_padding)
    h = 54 if is_root else (46 if is_hub else 40)
    return w, h

# Let's inspect max width per category
for cat in ['math', 'data', 'ml', 'eval', 'dl', 'genai', 'mlops', 'swe_cloud']:
    cat_nodes = [n for n in nodes if n.get('category') == cat and n.get('level') == 2]
    widths = [get_node_dims(n)[0] for n in cat_nodes]
    print(f"Cat {cat:<10}: count={len(cat_nodes)}, max_width={max(widths)}px, avg_width={sum(widths)/len(widths):.0f}px")
