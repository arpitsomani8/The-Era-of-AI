import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

gd_term = {
    "term": "Gradient Descent (-∇Loss)",
    "what_is_it": "• The foundational optimization algorithm that updates weights in the negative gradient direction: w ← w - η ∇Loss.\n• Continually guides weights downhill until the prediction error reaches the lowest accessible point in the loss landscape.",
    "analogy": "Rolling a marble down the inside of a bowl until it naturally settles at the lowest point in the center.",
    "why_it_matters": "The primary mathematical engine that trains modern machine learning models from linear regression to trillion-parameter LLMs."
}

with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for c in concepts:
    if c['id'] == 'concept_gradient_vector':
        terms = c['core_terms']
        # if not present, add it
        if not any('Gradient Descent' in t['term'] for t in terms):
            terms.append(gd_term)
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json successfully!")

if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for c in all_concepts:
        if c['id'] == 'concept_gradient_vector':
            terms = c['core_terms']
            if not any('Gradient Descent' in t['term'] for t in terms):
                terms.append(gd_term)
            break
    with open(ALL_CONCEPTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)
    print("Updated scripts/data_sources/all_concepts.json successfully!")

if os.path.exists(MATH_PY):
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_math", MATH_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    math_concepts = mod.MATH_CONCEPTS
    for c in math_concepts:
        if c['id'] == 'concept_gradient_vector':
            terms = c['core_terms']
            if not any('Gradient Descent' in t['term'] for t in terms):
                terms.append(gd_term)
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
