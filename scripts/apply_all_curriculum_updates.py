# scripts/apply_all_curriculum_updates.py
import json
import sys
import os

sys.path.insert(0, os.path.abspath('.'))

from scripts.generate_missing_curriculum_data import NEW_TOPICS
from scripts.build_full_updated_dataset import get_realigned_concepts
from scripts.curriculum_part_rl import get_rl_concepts
from scripts.curriculum_part_ts import get_time_series_concepts
from scripts.curriculum_part_recsys import get_recsys_concepts
from scripts.curriculum_part_gnn import get_gnn_concepts
from scripts.curriculum_part_xai import get_xai_concepts
from scripts.curriculum_part_audio import get_audio_concepts
from scripts.curriculum_part_reasoning import get_reasoning_concepts

def apply_updates():
    # 1. Load files
    with open('src/data/topics.json', 'r', encoding='utf-8') as f:
        topics = json.load(f)

    with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
        nodes = json.load(f)

    with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
        concepts = json.load(f)

    print(f"Initial state -> Topics: {len(topics)}, Nodes: {len(nodes)}, Concepts: {len(concepts)}")

    # 2. De-duplication / Subtopic Realignments mapping:
    # (topic_id, old_subtopic_substring, new_subtopic_string)
    realignments = [
        ("dl_foundations_limits", "Principal Component Analysis", "Autoencoders & Latent Bottlenecks"),
        ("dl_frameworks_cv_inference", "YOLO Architectural Evolution", "Real-Time Inference Acceleration (TensorRT, ONNX Runtime & CUDA Graphs)"),
        ("genai_nlp_foundations", "Tokens, Tokenization (BPE, WordPiece)", "Text Preprocessing, Lemmatization, Stopwords & Linguistic Normalization"),
        ("genai_embed", "Positional Encodings & Rotary Embeddings (RoPE)", "Context Window Scaling (YaRN, LongLoRA & StreamingLLM)"),
        ("genai_multimodal_agents", "LangGraph vs LangChain: State Machines", "Multimodal Tool Calling & Vision-Language Agents"),
        ("ml_opt", "Learning Rate Schedules & Cosine Decay", "Hyperparameter Tuning (Grid Search, Random Search & Bayesian Optuna)")
    ]

    # Update topics.json subtopics
    for tid, old_kw, new_sub in realignments:
        for t in topics:
            if t['id'] == tid:
                for idx, s in enumerate(t.get('subtopics', [])):
                    if old_kw.lower() in s.lower():
                        print(f"topics.json: [{tid}] updating '{s}' -> '{new_sub}'")
                        t['subtopics'][idx] = new_sub
                        break

    # Update allNodes.json subtopics
    for tid, old_kw, new_sub in realignments:
        for n in nodes:
            if n.get('id') == tid:
                for idx, s in enumerate(n.get('subtopics', [])):
                    if old_kw.lower() in s.lower():
                        print(f"allNodes.json: [{tid}] updating '{s}' -> '{new_sub}'")
                        n['subtopics'][idx] = new_sub
                        break

    # Append 7 new topics to topics.json
    existing_topic_ids = {t['id'] for t in topics}
    for nt in NEW_TOPICS:
        if nt['id'] not in existing_topic_ids:
            topics.append(nt)
            existing_topic_ids.add(nt['id'])
            print(f"topics.json: Added new topic [{nt['id']}] {nt['label']}")

    # Append 7 new topic nodes to allNodes.json
    existing_node_ids = {n['id'] for n in nodes}
    for nt in NEW_TOPICS:
        if nt['id'] not in existing_node_ids:
            new_node = {
                "id": nt['id'],
                "label": nt['label'],
                "level": nt['level'],
                "category": nt['category'],
                "x": nt['x'],
                "y": nt['y'],
                "subtopics": nt['subtopics'],
                "connections": nt['connections']
            }
            nodes.append(new_node)
            existing_node_ids.add(nt['id'])
            print(f"allNodes.json: Added new node [{new_node['id']}]")

    # Connect root nodes to their new topic children in allNodes.json
    root_connections_map = {
        "dl_root": ["dl_rl_foundations", "dl_gnn"],
        "ml_root": ["ml_time_series", "ml_recsys"],
        "eval_root": ["eval_xai"],
        "genai_root": ["genai_audio_speech", "genai_reasoning_test_time"]
    }
    for root_id, child_ids in root_connections_map.items():
        for n in nodes:
            if n.get('id') == root_id:
                curr_conns = set(n.get('connections', []))
                for cid in child_ids:
                    if cid not in curr_conns:
                        n['connections'].append(cid)
                        print(f"allNodes.json: Connected root [{root_id}] -> [{cid}]")

    # 3. Update concepts.json
    # Replace old realigned concepts
    realigned_concepts = get_realigned_concepts()
    old_cids_to_replace = {
        "concept_pca_dimensionality_reduction": "concept_autoencoders_latent_bottlenecks",
        "concept_yolo_realtime_detection": "concept_inference_acceleration_tensorrt_onnx",
        "concept_tokens_tokenization": "concept_text_preprocessing_normalization",
        "positional-encodings-rope": "concept_context_window_scaling_yarn",
        "concept_langgraph_cyclical_state_machines": "concept_multimodal_tool_calling_agents",
        "concept_lr_schedules": "concept_hyperparameter_tuning_bayesian"
    }

    realigned_map = {c['id']: c for c in realigned_concepts}

    new_concepts_list = []
    replaced_count = 0
    for c in concepts:
        cid = c['id']
        if cid in old_cids_to_replace:
            new_id = old_cids_to_replace[cid]
            if new_id in realigned_map:
                new_concepts_list.append(realigned_map[new_id])
                replaced_count += 1
                print(f"concepts.json: Replaced [{cid}] with [{new_id}]")
            else:
                new_concepts_list.append(c)
        else:
            new_concepts_list.append(c)

    # Gather all 35 new concepts
    all_35_new = (
        get_rl_concepts() +
        get_time_series_concepts() +
        get_recsys_concepts() +
        get_gnn_concepts() +
        get_xai_concepts() +
        get_audio_concepts() +
        get_reasoning_concepts()
    )
    print(f"Total new domain concepts gathered: {len(all_35_new)}")

    existing_concept_ids = {c['id'] for c in new_concepts_list}
    added_new_count = 0
    for nc in all_35_new:
        if nc['id'] not in existing_concept_ids:
            new_concepts_list.append(nc)
            existing_concept_ids.add(nc['id'])
            added_new_count += 1

    print(f"concepts.json: Added {added_new_count} brand new concepts.")

    # 4. Save updated files
    with open('src/data/topics.json', 'w', encoding='utf-8') as f:
        json.dump(topics, f, indent=2, ensure_ascii=False)

    with open('src/data/allNodes.json', 'w', encoding='utf-8') as f:
        json.dump(nodes, f, indent=2, ensure_ascii=False)

    with open('src/data/concepts.json', 'w', encoding='utf-8') as f:
        json.dump(new_concepts_list, f, indent=2, ensure_ascii=False)

    print(f"Final state -> Topics: {len(topics)}, Nodes: {len(nodes)}, Concepts: {len(new_concepts_list)}")
    print("Files successfully written!")

if __name__ == '__main__':
    apply_updates()
