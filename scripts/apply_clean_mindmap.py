# scripts/apply_clean_mindmap.py
import json
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from scripts.test_new_coordinates import NEW_COORDS

# Clean hierarchy mapping: parent hub for each topic
TOPIC_TO_HUB = {
    # Math
    "math_linalg": "math_root",
    "math_calc": "math_root",
    "math_prob": "math_root",
    "math_info": "math_root",

    # Data
    "data_scrub": "data_root",
    "data_impute": "data_root",
    "data_scale": "data_root",
    "data_fe": "data_root",
    "data_split": "data_root",

    # ML
    "ml_linear": "ml_root",
    "ml_loss": "ml_root",
    "ml_opt": "ml_root",
    "ml_logistic": "ml_root",
    "ml_reg": "ml_root",
    "ml_trees": "ml_root",
    "ml_unsupervised": "ml_root",
    "ml_svm_ensembles": "ml_root",
    "ml_time_series": "ml_root",
    "ml_recsys": "ml_root",

    # Eval
    "eval_matrix": "eval_root",
    "eval_curves": "eval_root",
    "eval_tradeoff": "eval_root",
    "eval_fairness_bias": "eval_root",
    "eval_xai": "eval_root",

    # DL
    "dl_neurons": "dl_root",
    "dl_activations": "dl_root",
    "dl_backprop": "dl_root",
    "dl_opt": "dl_root",
    "dl_norm": "dl_root",
    "dl_vision": "dl_root",
    "dl_seq": "dl_root",
    "dl_generative": "dl_root",
    "dl_foundations_limits": "dl_root",
    "dl_frameworks_cv_inference": "dl_root",
    "dl_rl_foundations": "dl_root",
    "dl_gnn": "dl_root",

    # GenAI
    "genai_embed": "genai_root",
    "genai_attention": "genai_root",
    "genai_train": "genai_root",
    "genai_align": "genai_root",
    "genai_rag": "genai_root",
    "genai_prompt_agents": "genai_root",
    "genai_nlp_foundations": "genai_root",
    "genai_transformer_deep_dive": "genai_root",
    "genai_agentic_stack": "genai_root",
    "genai_decoding_architectures": "genai_root",
    "genai_vector_db_pinecone": "genai_root",
    "genai_multimodal_agents": "genai_root",
    "genai_audio_speech": "genai_root",
    "genai_reasoning_test_time": "genai_root",

    # MLOps
    "mlops_hygiene": "mlops_root",
    "mlops_llmops_system_design": "mlops_root",

    # SWE & Cloud
    "swe_patterns_architecture": "hub_swe_cloud",
    "swe_cloud_infra": "hub_swe_cloud"
}

def apply_clean_layout():
    with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
        nodes = json.load(f)

    with open('src/data/topics.json', 'r', encoding='utf-8') as f:
        topics = json.load(f)

    # 1. Update allNodes.json
    for n in nodes:
        nid = n['id']
        x, y = NEW_COORDS[nid]
        n['x'] = x
        n['y'] = y

        # Set clean hierarchy connections
        if nid == 'root':
            n['connections'] = [
                'math_root', 'data_root', 'ml_root', 'eval_root',
                'dl_root', 'genai_root', 'mlops_root', 'hub_swe_cloud'
            ]
        elif n.get('level') == 1:
            if nid == 'hub_swe_cloud':
                n['connections'] = ['root', 'mlops_root']
            else:
                n['connections'] = ['root']
        elif nid in TOPIC_TO_HUB:
            n['connections'] = [TOPIC_TO_HUB[nid]]

    # 2. Update topics.json coordinates & connections
    for t in topics:
        tid = t['id']
        if tid in NEW_COORDS:
            x, y = NEW_COORDS[tid]
            t['x'] = x
            t['y'] = y
        if tid in TOPIC_TO_HUB:
            t['connections'] = [TOPIC_TO_HUB[tid]]

    with open('src/data/allNodes.json', 'w', encoding='utf-8') as f:
        json.dump(nodes, f, indent=2, ensure_ascii=False)

    with open('src/data/topics.json', 'w', encoding='utf-8') as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)

    print("SUCCESS: Clean mindmap layout and hierarchy connections applied to allNodes.json and topics.json!")

if __name__ == '__main__':
    apply_clean_layout()
