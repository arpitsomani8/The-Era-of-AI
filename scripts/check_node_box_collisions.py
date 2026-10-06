# scripts/check_node_box_collisions.py
import json

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

def get_node_bbox(node):
    is_root = node.get('level') == 0
    is_hub = node.get('level') == 1
    label_len = len(node.get('label', ''))
    char_width = 8.6 if is_root else (7.6 if is_hub else 6.8)
    text_width = round(label_len * char_width)
    left_offset = 36 if is_root else (30 if is_hub else 28)
    right_padding = 18
    min_width = 260 if is_root else (210 if is_hub else 180)
    node_width = max(min_width, text_width + left_offset + right_padding)
    node_height = 54 if is_root else (46 if is_hub else 40)
    
    x = node.get('x', 0)
    y = node.get('y', 0)
    
    # Add a safety margin of 10px so pills have breathing room
    margin = 8
    return {
        'id': node['id'],
        'label': node['label'],
        'left': x - node_width / 2 - margin,
        'right': x + node_width / 2 + margin,
        'top': y - node_height / 2 - margin,
        'bottom': y + node_height / 2 + margin,
        'width': node_width,
        'height': node_height
    }

boxes = [get_node_bbox(n) for n in nodes]
collisions = []

for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        b1, b2 = boxes[i], boxes[j]
        # Check AABB overlap
        if not (b1['right'] < b2['left'] or b1['left'] > b2['right'] or b1['bottom'] < b2['top'] or b1['top'] > b2['bottom']):
            overlap_x = min(b1['right'], b2['right']) - max(b1['left'], b2['left'])
            overlap_y = min(b1['bottom'], b2['bottom']) - max(b1['top'], b2['top'])
            collisions.append((b1['id'], b2['id'], overlap_x, overlap_y))

print(f"Total nodes evaluated: {len(boxes)}")
print(f"Total collisions found: {len(collisions)}")
for id1, id2, ox, oy in collisions:
    print(f"  - COLLISION: [{id1}] and [{id2}] overlap by X={ox:.1f}px, Y={oy:.1f}px")
