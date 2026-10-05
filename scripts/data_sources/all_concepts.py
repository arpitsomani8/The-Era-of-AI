"""
Master Aggregator for All 169 AI/ML/DL Core Concepts.
Imports all domain concept databases, builds lookup dictionaries by ID and raw subtopic title,
and provides helper utilities for generating standalone pages and embedding in the application.
"""

import json
import os

from concepts_math import MATH_CONCEPTS
from concepts_data_prep import DATA_CONCEPTS as DATA_PREP_CONCEPTS
from concepts_ml import ML_CONCEPTS
from concepts_eval import EVAL_CONCEPTS
from concepts_dl import DL_CONCEPTS
from concepts_dl_arch import DL_ARCH_CONCEPTS
from concepts_genai import GENAI_CONCEPTS
from concepts_mlops import MLOPS_CONCEPTS

ALL_CONCEPTS = (
    MATH_CONCEPTS +
    DATA_PREP_CONCEPTS +
    ML_CONCEPTS +
    EVAL_CONCEPTS +
    DL_CONCEPTS +
    DL_ARCH_CONCEPTS +
    GENAI_CONCEPTS +
    MLOPS_CONCEPTS
)

# Standardize all concept dicts so all fields are consistently accessible
STANDARDIZED_CONCEPTS = []
for c in ALL_CONCEPTS:
    item = dict(c)
    raw_sub = item.get("raw_sub") or item.get("raw_subtopic") or item.get("title", "")
    definition = item.get("definition") or item.get("def") or ""
    item["raw_sub"] = raw_sub
    item["raw_subtopic"] = raw_sub
    item["definition"] = definition
    item["def"] = definition
    if "formula_explanation" not in item:
        item["formula_explanation"] = ""
    if "tags" not in item:
        item["tags"] = [item.get("category_label", ""), item.get("topic_label", "")]
    STANDARDIZED_CONCEPTS.append(item)

ALL_CONCEPTS = STANDARDIZED_CONCEPTS

# Build lookup maps
CONCEPTS_BY_ID = {c["id"]: c for c in ALL_CONCEPTS}
CONCEPTS_BY_RAW_SUB = {c["raw_sub"]: c for c in ALL_CONCEPTS}

# Quick normalize lookup for string matching
def normalize_str(s):
    import re
    return re.sub(r'[^a-z0-9]', '', s.lower())

NORMALIZED_SUB_MAP = {normalize_str(c["raw_sub"]): c for c in ALL_CONCEPTS}
for c in ALL_CONCEPTS:
    NORMALIZED_SUB_MAP[normalize_str(c["title"])] = c

def find_concept(query_str):
    if not query_str:
        return None
    if query_str in CONCEPTS_BY_ID:
        return CONCEPTS_BY_ID[query_str]
    if query_str in CONCEPTS_BY_RAW_SUB:
        return CONCEPTS_BY_RAW_SUB[query_str]
    norm = normalize_str(query_str)
    if norm in NORMALIZED_SUB_MAP:
        return NORMALIZED_SUB_MAP[norm]
    for c in ALL_CONCEPTS:
        if norm in normalize_str(c["title"]) or normalize_str(c["title"]) in norm:
            return c
        if norm in normalize_str(c["raw_sub"]) or normalize_str(c["raw_sub"]) in norm:
            return c
    return None

if __name__ == "__main__":
    print(f"Total concepts aggregated: {len(ALL_CONCEPTS)}")
    assert len(ALL_CONCEPTS) >= 169, f"Expected at least 169, got {len(ALL_CONCEPTS)}"
    
    # Save as JSON for frontend embedding and standalone pages
    out_path = os.path.join(os.path.dirname(__file__), "all_concepts.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ALL_CONCEPTS, f, indent=2, ensure_ascii=False)
    print(f"Saved {out_path} ({os.path.getsize(out_path):,} bytes)")
