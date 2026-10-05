import json

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

with open('src/data/crossLinks.json', 'r', encoding='utf-8') as f:
    cross_links = json.load(f)

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

# SVG bounds calculation
min_x = min(n['x'] - get_node_dims(n)[0]/2 for n in nodes) - 100
max_x = max(n['x'] + get_node_dims(n)[0]/2 for n in nodes) + 100
min_y = min(n['y'] - get_node_dims(n)[1]/2 for n in nodes) - 100
max_y = max(n['y'] + get_node_dims(n)[1]/2 for n in nodes) + 100

width = int(max_x - min_x)
height = int(max_y - min_y)

svg_lines = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {width} {height}" width="100%" height="100%" style="background:#090d16; font-family: Inter, sans-serif;">'
]

# Hierarchy lines
node_map = {n['id']: n for n in nodes}
for n in nodes:
    if 'connections' in n:
        for cid in n['connections']:
            if cid in node_map:
                target = node_map[cid]
                svg_lines.append(f'<line x1="{n["x"]}" y1="{n["y"]}" x2="{target["x"]}" y2="{target["y"]}" stroke="#334155" stroke-width="1.5" />')

# Nodes
for n in nodes:
    w, h = get_node_dims(n)
    is_root = n.get('level') == 0
    is_hub = n.get('level') == 1
    rx = 16 if is_root else 10
    bg = '#312e81' if is_root else '#0f172a'
    stroke = '#6366f1' if is_root else '#38bdf8' if n.get('category') == 'ml' else '#ec4899' if n.get('category') == 'dl' else '#10b981' if n.get('category') == 'data' else '#f59e0b' if n.get('category') == 'eval' else '#818cf8'
    text_color = '#ffffff' if is_root else '#f8fafc'
    font_size = 14 if is_root else (12 if is_hub else 11)
    font_weight = 700 if is_root else (600 if is_hub else 500)
    left_off = 36 if is_root else (30 if is_hub else 28)

    svg_lines.append(f'<g transform="translate({n["x"]}, {n["y"]})">')
    svg_lines.append(f'  <rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="{rx}" fill="{bg}" stroke="{stroke}" stroke-width="1.8" />')
    svg_lines.append(f'  <circle cx="{-w/2 + 14}" cy="0" r="{5.5 if is_root else 4}" fill="{stroke}" />')
    svg_lines.append(f'  <text x="{-w/2 + left_off}" y="4" fill="{text_color}" font-size="{font_size}" font-weight="{font_weight}">{n["label"]}</text>')
    svg_lines.append('</g>')

svg_lines.append('</svg>')

with open('public/mindmap_preview.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg_lines))

print(f"Generated public/mindmap_preview.svg ({width}x{height})")
