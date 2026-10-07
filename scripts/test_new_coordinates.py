# scripts/test_new_coordinates.py
import json

NEW_COORDS = {
    # 0. Center
    "root": (0, 0),

    # 1. Math (Top-Left)
    "math_root": (-650, -450),
    "math_linalg": (-1100, -660),
    "math_calc": (-1100, -520),
    "math_prob": (-1100, -380),
    "math_info": (-1100, -240),

    # 2. Data Preprocessing (Far-Left)
    "data_root": (-650, 150),
    "data_scrub": (-1100, -70),
    "data_impute": (-1100, 40),
    "data_scale": (-1100, 150),
    "data_fe": (-1100, 260),
    "data_split": (-1100, 370),

    # 3. Classical ML (Top / North)
    "ml_root": (-120, -420),
    "ml_time_series": (-380, -960),
    "ml_reg": (-380, -840),
    "ml_loss": (-380, -720),
    "ml_linear": (-380, -600),

    "ml_recsys": (140, -960),
    "ml_trees": (140, -840),
    "ml_opt": (140, -720),
    "ml_logistic": (140, -600),
    "ml_unsupervised": (140, -480),
    "ml_svm_ensembles": (140, -360),

    # 4. Evaluation & Generalization (Bottom-Left / South-West)
    "eval_root": (-500, 580),
    "eval_matrix": (-840, 520),
    "eval_curves": (-840, 640),
    "eval_fairness_bias": (-840, 760),
    "eval_tradeoff": (-350, 680),
    "eval_xai": (-350, 800),

    # 5. Deep Learning (Top-Right / North-East)
    "dl_root": (600, -320),
    # Column A (Inner, X=600)
    "dl_neurons": (600, -640),
    "dl_backprop": (600, -530),
    "dl_norm": (600, -420),
    "dl_seq": (600, -210),
    "dl_foundations_limits": (600, -100),
    "dl_rl_foundations": (600, 10),

    # Column B (Outer, X=1100)
    "dl_activations": (1100, -640),
    "dl_opt": (1100, -530),
    "dl_vision": (1100, -420),
    "dl_generative": (1100, -210),
    "dl_frameworks_cv_inference": (1100, -100),
    "dl_gnn": (1100, 10),

    # 6. GenAI & Transformers (Right / East)
    "genai_root": (1100, 170),
    # Column A (X=1100)
    "genai_embed": (1100, 270),
    "genai_attention": (1100, 380),
    "genai_transformer_deep_dive": (1100, 490),
    "genai_decoding_architectures": (1100, 600),
    "genai_audio_speech": (1100, 710),
    "genai_nlp_foundations": (1100, 820),

    # Column B (X=1600)
    "genai_train": (1600, 160),
    "genai_align": (1600, 270),
    "genai_rag": (1600, 380),
    "genai_vector_db_pinecone": (1600, 490),
    "genai_prompt_agents": (1600, 600),
    "genai_agentic_stack": (1600, 710),
    "genai_multimodal_agents": (1600, 820),
    "genai_reasoning_test_time": (1600, 930),

    # 7. MLOps & Production (Bottom-Center / South)
    "mlops_root": (80, 540),
    "mlops_hygiene": (80, 680),
    "mlops_llmops_system_design": (80, 800),

    # 8. Software Engineering & Cloud (Bottom-Right / South-East)
    "hub_swe_cloud": (560, 640),
    "swe_patterns_architecture": (560, 770),
    "swe_cloud_infra": (560, 900)
}

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

def get_node_bbox(node, x, y):
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
    margin = 8
    return {
        'id': node['id'],
        'left': x - node_width / 2 - margin,
        'right': x + node_width / 2 + margin,
        'top': y - node_height / 2 - margin,
        'bottom': y + node_height / 2 + margin,
        'width': node_width,
        'height': node_height
    }

boxes = [get_node_bbox(n, NEW_COORDS[n['id']][0], NEW_COORDS[n['id']][1]) for n in nodes]
collisions = []

for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        b1, b2 = boxes[i], boxes[j]
        if not (b1['right'] < b2['left'] or b1['left'] > b2['right'] or b1['bottom'] < b2['top'] or b1['top'] > b2['bottom']):
            overlap_x = min(b1['right'], b2['right']) - max(b1['left'], b2['left'])
            overlap_y = min(b1['bottom'], b2['bottom']) - max(b1['top'], b2['top'])
            collisions.append((b1['id'], b2['id'], overlap_x, overlap_y))

print(f"Total nodes: {len(boxes)}")
print(f"Collisions: {len(collisions)}")
for id1, id2, ox, oy in collisions:
    print(f"  - COLLISION: [{id1}] and [{id2}] overlap by X={ox:.1f}px, Y={oy:.1f}px")
