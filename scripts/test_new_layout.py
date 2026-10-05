import json

# Proposed coordinates dictionary
proposed_coords = {
    # Root
    "root": {"x": 0, "y": 0},

    # 1. Math Root and Children
    "math_root": {"x": -500, "y": -420},
    "math_linalg": {"x": -880, "y": -600},
    "math_calc": {"x": -880, "y": -480},
    "math_prob": {"x": -880, "y": -360},
    "math_info": {"x": -880, "y": -240},

    # 2. Data Root and Children
    "data_root": {"x": -560, "y": 180},
    "data_scrub": {"x": -940, "y": 0},
    "data_impute": {"x": -940, "y": 90},
    "data_scale": {"x": -940, "y": 180},
    "data_fe": {"x": -940, "y": 270},
    "data_split": {"x": -940, "y": 360},

    # 3. Classical ML Root and Children
    "ml_root": {"x": -140, "y": -450},
    # Tier 1 (y: -610)
    "ml_linear": {"x": -380, "y": -610},
    "ml_logistic": {"x": 100, "y": -610},
    # Tier 2 (y: -710)
    "ml_loss": {"x": -380, "y": -710},
    "ml_opt": {"x": 100, "y": -710},
    # Tier 3 (y: -810)
    "ml_reg": {"x": -460, "y": -810},
    "ml_trees": {"x": -90, "y": -810},
    "ml_unsupervised": {"x": 280, "y": -810},

    # MLOps
    "mlops_root": {"x": 140, "y": -250},

    # 5. Deep Learning Root and Children
    "dl_root": {"x": 440, "y": -200},
    # Col 1 (x: 840), Col 2 (x: 1260)
    "dl_neurons": {"x": 840, "y": -420},
    "dl_activations": {"x": 1260, "y": -420},
    "dl_backprop": {"x": 840, "y": -290},
    "dl_opt": {"x": 1260, "y": -290},
    "dl_norm": {"x": 840, "y": -160},
    "dl_vision": {"x": 1260, "y": -160},
    "dl_seq": {"x": 840, "y": -30},
    "dl_generative": {"x": 1260, "y": -30},

    # 6. Transformers & Generative AI Root and Children
    "genai_root": {"x": 440, "y": 260},
    # Col 1 (x: 840), Col 2 (x: 1260)
    "genai_embed": {"x": 840, "y": 140},
    "genai_attention": {"x": 1260, "y": 140},
    "genai_train": {"x": 840, "y": 260},
    "genai_align": {"x": 1260, "y": 260},
    "genai_rag": {"x": 840, "y": 380},
    "genai_prompt_agents": {"x": 1260, "y": 380},

    # 4. Model Evaluation & Generalization Root and Children
    "eval_root": {"x": -100, "y": 350},
    "eval_matrix": {"x": -450, "y": 540},
    "eval_curves": {"x": -70, "y": 540},
    "eval_tradeoff": {"x": 310, "y": 540},
}

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

# Apply proposed coords
for n in nodes:
    nid = n['id']
    if nid in proposed_coords:
        n['x'] = proposed_coords[nid]['x']
        n['y'] = proposed_coords[nid]['y']
    else:
        print(f"WARNING: missing coord for {nid}")

# Check collisions
min_gap = 15  # ensure at least 15px pure gap between every box boundary
collisions = []
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

        # Check overlap including min_gap
        overlap_x = min(r1 + min_gap/2, r2 + min_gap/2) - max(l1 - min_gap/2, l2 - min_gap/2)
        overlap_y = min(b1 + min_gap/2, b2 + min_gap/2) - max(t1 - min_gap/2, t2 - min_gap/2)

        if overlap_x > 0 and overlap_y > 0:
            collisions.append((n1['id'], n2['id'], overlap_x, overlap_y))

print(f"Total nodes: {len(nodes)}")
print(f"Collisions with {min_gap}px minimum buffer: {len(collisions)}")
for c in collisions:
    print(f"  Collision {c[0]} vs {c[1]}: overlap_x={c[2]:.1f}, overlap_y={c[3]:.1f}")
