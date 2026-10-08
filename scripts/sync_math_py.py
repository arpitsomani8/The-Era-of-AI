import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

with open(os.path.join(SCRIPT_DIR, "update_vectors_concept.py"), "r", encoding="utf-8") as f:
    text = f.read()

# Also let's update concepts_math.py
with open(MATH_PY, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the first concept in concepts_math.py if present
import re

with open(os.path.join(SCRIPT_DIR, "..", "src", "data", "concepts.json"), "r", encoding="utf-8") as f:
    concepts = json.load(f)

concept_0 = concepts[0]

# Let's inspect if concepts_math.py has MATH_CONCEPTS
if 'MATH_CONCEPTS = [' in content:
    # replace first dict
    # We can load MATH_CONCEPTS, replace first item and dump
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_math", MATH_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    math_concepts = mod.MATH_CONCEPTS
    math_concepts[0] = concept_0
    
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
