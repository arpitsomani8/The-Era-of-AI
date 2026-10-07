# scripts/rebalance_mindmap_layout.py
import json
import math

COORDINATES_MAP = {
    # 0. Center
    "root": (0, 0),

    # 1. Math (Top-Left)
    "math_root": (-650, -450),
    "math_linalg": (-1050, -620),
    "math_calc": (-1050, -480),
    "math_prob": (-1050, -340),
    "math_info": (-1050, -200),

    # 2. Data Preprocessing (Far-Left)
    "data_root": (-650, 120),
    "data_scrub": (-1080, -60),
    "data_impute": (-1080, 50),
    "data_scale": (-1080, 160),
    "data_fe": (-1080, 270),
    "data_split": (-1080, 380),

    # 3. Classical ML (Top / North)
    "ml_root": (-140, -450),
    "ml_time_series": (-440, -900),
    "ml_reg": (-440, -790),
    "ml_loss": (-440, -680),
    "ml_linear": (-440, -570),

    "ml_recsys": (-140, -900),
    "ml_trees": (-140, -790),
    "ml_svm_ensembles": (-140, -680),

    "ml_opt": (160, -790),
    "ml_logistic": (160, -680),
    "ml_unsupervised": (160, -570),

    # 4. Evaluation & Generalization (Bottom-Left / South-West)
    "eval_root": (-250, 420),
    "eval_matrix": (-540, 580),
    "eval_curves": (-300, 580),
    "eval_tradeoff": (-60, 580),
    "eval_xai": (180, 580),
    "eval_fairness_bias": (-180, 710),

    # 5. Deep Learning (Top-Right / North-East)
    "dl_root": (450, -280),
    # Column A (Inner, X=750)
    "dl_neurons": (750, -520),
    "dl_backprop": (750, -410),
    "dl_norm": (750, -300),
    "dl_seq": (750, -190),
    "dl_foundations_limits": (750, -80),
    "dl_rl_foundations": (750, 30),

    # Column B (Outer, X=1120)
    "dl_activations": (1120, -520),
    "dl_opt": (1120, -410),
    "dl_vision": (1120, -300),
    "dl_generative": (1120, -190),
    "dl_frameworks_cv_inference": (1120, -80),
    "dl_gnn": (1120, 30),

    # 6. GenAI & Transformers (Right / East)
    "genai_root": (450, 300),
    # Column A (Foundations, X=750)
    "genai_nlp_foundations": (750, 160),
    "genai_embed": (750, 270),
    "genai_attention": (750, 380),
    "genai_transformer_deep_dive": (750, 490),
    "genai_decoding_architectures": (750, 600),

    # Column B (Training, RAG, Audio, X=1020)
    "genai_train": (1020, 160),
    "genai_align": (1020, 270),
    "genai_rag": (1020, 380),
    "genai_vector_db_pinecone": (1020, 490),
    "genai_audio_speech": (1020, 600),

    # Column C (Agents & Reasoning, X=1280)
    "genai_prompt_agents": (1280, 200),
    "genai_agentic_stack": (1280, 330),
    "genai_multimodal_agents": (1280, 460),
    "genai_reasoning_test_time": (1280, 590),

    # 7. MLOps & Production (Bottom-Center / South)
    "mlops_root": (100, 320),
    "mlops_hygiene": (100, 440),
    "mlops_llmops_system_design": (320, 440),

    # 8. Software Engineering & Cloud (Bottom / South-East)
    "hub_swe_cloud": (220, 710),
    "swe_patterns_architecture": (100, 840),
    "swe_cloud_infra": (380, 840)
}

def verify_and_apply():
    with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
        nodes = json.load(f)

    with open('src/data/topics.json', 'r', encoding='utf-8') as f:
        topics = json.load(f)

    node_ids = {n['id'] for n in nodes}
    print(f"Total nodes in file: {len(nodes)}")
    print(f"Total coordinates mapped: {len(COORDINATES_MAP)}")

    missing_in_map = node_ids - set(COORDINATES_MAP.keys())
    if missing_in_map:
        print(f"ERROR: Nodes missing in COORDINATES_MAP: {missing_in_map}")
        return

    # Check for duplicate positions
    pos_to_id = {}
    for nid, (x, y) in COORDINATES_MAP.items():
        if (x, y) in pos_to_id:
            print(f"COLLISION: {nid} and {pos_to_id[(x,y)]} both at ({x}, {y})")
            return
        pos_to_id[(x, y)] = nid

    # Apply to allNodes.json
    for n in nodes:
        nid = n['id']
        x, y = COORDINATES_MAP[nid]
        n['x'] = x
        n['y'] = y

    # Apply to topics.json
    for t in topics:
        tid = t['id']
        if tid in COORDINATES_MAP:
            x, y = COORDINATES_MAP[tid]
            t['x'] = x
            t['y'] = y

    with open('src/data/allNodes.json', 'w', encoding='utf-8') as f:
        json.dump(nodes, f, indent=2, ensure_ascii=False)

    with open('src/data/topics.json', 'w', encoding='utf-8') as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)

    print("SUCCESS: All 63 nodes re-balanced with zero collisions!")

    # Check bounds
    all_x = [n['x'] for n in nodes]
    all_y = [n['y'] for n in nodes]
    print(f"New Bounds -> X: [{min(all_x)}, {max(all_x)}] (Span: {max(all_x) - min(all_x)}px), Y: [{min(all_y)}, {max(all_y)}] (Span: {max(all_y) - min(all_y)}px)")

if __name__ == '__main__':
    verify_and_apply()
