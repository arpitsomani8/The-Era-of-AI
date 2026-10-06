# scripts/build_complete_aligned_curriculum.py
import json
import os

def make_concept(cid, title, topic_id, topic_label, category, category_label, raw_subtopic,
                 defn, formula, logic, example, tags, simple_summary, core_terms, symbol_guide,
                 num_example, pitfalls):
    # build definition bullets from core_terms
    bullets = [f"{t['term']}: {t['what_is_it']}" for t in core_terms]
    return {
        "id": cid,
        "title": title,
        "topic_id": topic_id,
        "topic_label": topic_label,
        "category": category,
        "category_label": category_label,
        "raw_subtopic": raw_subtopic,
        "raw_sub": raw_subtopic,
        "def": defn,
        "definition": defn,
        "formula": formula,
        "formula_explanation": "",
        "logic": logic,
        "core_logic": logic,
        "architectural_logic": "",
        "example": example,
        "tags": tags,
        "simple_summary": simple_summary,
        "core_terms": core_terms,
        "symbol_guide": symbol_guide,
        "numerical_example": num_example,
        "pitfalls": pitfalls,
        "key_takeaways": [],
        "definition_bullets": bullets
    }

print("Helper defined.")
