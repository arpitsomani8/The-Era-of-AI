import json

with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

concept_map = {c['id']: c for c in concepts}

print("=== REPEATED / OVERLAPPING SUBTOPICS DETAILS ===")
overlaps = [
    ("PCA", ["ml_unsupervised", "dl_foundations_limits"]),
    ("YOLO", ["dl_vision", "dl_frameworks_cv_inference"]),
    ("Tokenization", ["genai_embed", "genai_nlp_foundations"]),
    ("Positional Encoding / RoPE", ["genai_embed", "genai_nlp_foundations"]),
    ("LangGraph / LangChain", ["genai_agentic_stack", "genai_multimodal_agents"]),
    ("Cosine Decay / Learning Rate", ["ml_opt", "dl_opt"])
]

for label, t_ids in overlaps:
    print(f"\n--- {label} ---")
    for tid in t_ids:
        t = next(x for x in topics if x['id'] == tid)
        print(f"Topic: [{t['id']}] {t['label']}")
        for s in t.get('subtopics', []):
            # find matching concept
            c = next((x for x in concepts if x.get('raw_subtopic') == s and x.get('topic_id') == tid), None)
            cid = c['id'] if c else "NOT FOUND"
            ctitle = c['title'] if c else "N/A"
            if any(k.lower() in s.lower() for k in label.split(' / ')):
                print(f"   Subtopic: \"{s}\" -> Concept: [{cid}] {ctitle}")
