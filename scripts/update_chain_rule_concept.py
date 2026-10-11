import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

chain_rule_concept = {
    "id": "concept_chain_rule",
    "title": "The Chain Rule of Calculus",
    "topic_id": "math_calc",
    "topic_label": "Calculus & Optimization Dynamics",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "The Chain Rule of Calculus (Nested functions f(g(x)))",
    "def": "The mathematical formula for computing the derivative of composite, nested functions by multiplying the derivatives of each intermediate sub-function.",
    "formula": "$$\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}, \\quad \\frac{\\partial \\mathcal{L}}{\\partial W_1} = \\frac{\\partial \\mathcal{L}}{\\partial \\hat{y}} \\cdot \\frac{\\partial \\hat{y}}{\\partial W_2} \\cdot \\frac{\\partial W_2}{\\partial W_1}$$",
    "logic": "The chain rule is the mathematical engine behind backpropagation. Neural networks are chains of composite functions; gradients propagate backward layer by layer via sequential chain rule multiplications.",
    "example": "If pedal pressure affects speed (du/dx = 3) and speed affects fuel burn (dy/du = 4), the chain rule calculates direct pedal-to-fuel sensitivity as 3 × 4 = 12.",
    "tags": [
        "Chain Rule",
        "Calculus",
        "Backpropagation",
        "Vanishing Gradient",
        "Deep Learning Foundations"
    ],
    "raw_sub": "The Chain Rule of Calculus (Nested functions f(g(x)))",
    "definition": "The mathematical rule for differentiating nested composite functions: the rate of change of the final output equals the product of all intermediate rates of change.",
    "formula_explanation": "If x influences u and u influences y, dy/dx = (dy/du) · (du/dx). In deep learning, backpropagation calculates weight updates by multiplying incoming gradients with local layer derivatives from loss back to input.",
    "simple_summary": "The Chain Rule is the gear system of deep learning: when data passes through layers like connected gears, the chain rule multiplies their local slopes together to calculate how early weights affect the final loss.",
    "core_terms": [
        {
            "term": "The Chain Rule",
            "what_is_it": "• A calculus rule stating that the derivative of nested composite functions equals the product of intermediate rates: dy/dx = (dy/du) · (du/dx).\n• It is the mathematical engine behind Backpropagation, allowing networks with hundreds of layers (like GPT-4 or Gemini) to learn from errors.",
            "analogy": "Connected gears: Turning Gear A turns Gear B 3 times, and Gear B turns Gear C 4 times. Turning Gear A turns Gear C 3 × 4 = 12 times.",
            "why_it_matters": "Without the chain rule, an AI could never determine which specific weights in earlier layers caused a prediction error."
        },
        {
            "term": "Composite Function (f(g(x)))",
            "what_is_it": "• A function nested inside another function, where the output of the inner operation becomes the input to the outer operation.\n• Deep neural networks are giant chains of composite functions: Loss = f_L(f_{L-1}(... f₁(x))).",
            "analogy": "An assembly line: Station 1 cuts the metal sheet (g(x)), Station 2 stamps the design (f(u)), and the final station inspects quality.",
            "why_it_matters": "Stacking composite functions allows AI models to learn hierarchical representations from raw pixels to abstract concepts."
        },
        {
            "term": "Backpropagation (Chain Rule in Reverse)",
            "what_is_it": "• The backward pass algorithm: while data flows forward to produce predictions, gradients flow backward via the chain rule.\n• Each layer takes the gradient from the layer ahead, multiplies it by its own local derivative, and passes the result back to earlier layers.",
            "analogy": "A bucket brigade in reverse: the fire chief at the end (Loss) tells the team how much water was missing, and the instruction ripples backward to the tap.",
            "why_it_matters": "Calculates exact gradients for billions of parameters in a single backward pass instead of impossible brute-force trial and error."
        }
    ],
    "types_header": "Chain Rule Multiplication: Issues & Fixes",
    "types_badge": "Issues & Solutions",
    "quick_types": [
        {
            "type": "Vanishing Gradients (g < 1.0) [Issue]",
            "definition": "Multiplying derivatives smaller than 1 across deep layers shrinks the gradient to near zero.",
            "looks_like": "0.5⁵⁰ ≈ 8.8 × 10⁻¹⁶ (Early layers stop updating)"
        },
        {
            "type": "Exploding Gradients (g > 1.0) [Issue]",
            "definition": "Multiplying derivatives greater than 1 causes gradients to blow up astronomically into NaN errors.",
            "looks_like": "1.5⁵⁰ ≈ 6.37 × 10⁸ (Unstable weights & training crashes)"
        },
        {
            "type": "ReLU Activations [Fix]",
            "definition": "Replaces Sigmoid with ReLU whose derivative is constant 1.0 for all positive inputs.",
            "looks_like": "∂ReLU/∂x = 1.0 (Zero gradient shrinkage)"
        },
        {
            "type": "Residual Skip Connections [Fix]",
            "definition": "Adds shortcut highway paths (ResNets & Transformers) giving gradients an unblocked addition route.",
            "looks_like": "Gradient = 1 + ∂F/∂x (Guaranteed gradient flow)"
        },
        {
            "type": "Normalization Layers [Fix]",
            "definition": "LayerNorm and BatchNorm keep activations and gradients bounded within a stable numerical scale.",
            "looks_like": "Mean = 0, Var = 1 (Prevents explosion and internal drift)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "dy / dx",
            "meaning": "Total derivative",
            "plain_english": "Overall sensitivity of output y to changes in initial input x"
        },
        {
            "symbol": "dy / du",
            "meaning": "Outer local derivative",
            "plain_english": "How output y responds to intermediate variable u"
        },
        {
            "symbol": "du / dx",
            "meaning": "Inner local derivative",
            "plain_english": "How intermediate variable u responds to initial input x"
        },
        {
            "symbol": "∂ℒ / ∂W₁",
            "meaning": "Backpropagation weight gradient",
            "plain_english": "Sensitivity of final Loss ℒ to an early weight W₁ in the network"
        },
        {
            "symbol": "∂ℒ / ∂ŷ",
            "meaning": "Output prediction error gradient",
            "plain_english": "The starting error signal computed at the final prediction layer"
        }
    ],
    "numerical_example": "Differentiating composite function y = (3x + 1)² at x = 2:\n\n1. Split into inner and outer components:\n   • Let inner u = 3x + 1\n   • Let outer y = u²\n\n2. Compute local derivatives:\n   • du/dx = 3\n   • dy/du = 2u = 2(3x + 1)\n\n3. Multiply using the Chain Rule (dy/dx = dy/du · du/dx):\n   • dy/dx = 2(3x + 1) × 3 = 6(3x + 1) = 18x + 6\n\n4. Evaluate at x = 2:\n   • dy/dx = 18(2) + 6 = 36 + 6 = 42\n   --> A nudge of +0.01 in x produces an immediate +0.42 change in y!",
    "pitfalls": "Common Trap: The vanishing gradient trap. Multiplying 50 derivatives that are slightly less than 1 (e.g. 0.5⁵⁰ ≈ 10⁻¹⁶) shrinks the gradient to zero, freezing early layers. Use ReLU activations and residual connections to maintain healthy gradient flow.",
    "core_logic": "The chain rule is the mathematical bedrock of backpropagation. A neural network is simply a chain of composite functions y = f_L(f_{L-1}(... f₁(x))); gradients propagate backward layer by layer via sequential chain rule multiplications.",
    "architectural_logic": "Modern deep architectures like Transformers and ResNets rely on the additive property of the multivariate chain rule. By adding residual skip connections y = x + F(x), the gradient ∂Loss/∂x = ∂Loss/∂y · (1 + ∂F/∂x) always contains a direct '+1' highway path, completely eliminating vanishing gradients.",
    "connected_logic": [
        {
            "title": "The Domino Effect: Multiplying Local Rates",
            "content": "• If x alters u and u alters y, overall sensitivity is the product of intermediate rates: dy/dx = (dy/du) · (du/dx).\n• Backpropagation is literally the chain rule evaluated from right to left, multiplying local Jacobians layer-by-layer."
        },
        {
            "title": "Forward Pass vs. Backward Pass",
            "content": "• Forward Pass: Input data flows forward through stacked weight layers to compute predictions and final loss.\n• Backward Pass: Error signal flows in reverse, where each layer multiplies incoming gradients by its local slope and sends it backward."
        },
        {
            "title": "The Deep Multiplication Dilemma",
            "content": "• In a 50-layer network, gradients multiply across 50 terms: Gradient ≈ g₁ × g₂ × ... × g₅₀.\n• Factors < 1 shrink to 0 (vanishing gradients), while factors > 1 explode to millions (exploding gradients), paralyzing deep training."
        },
        {
            "title": "How Modern AI Solved Gradient Degradation",
            "content": "• ReLU Activations: Provide a constant derivative of 1 for positive inputs, eliminating Sigmoid saturation.\n• Skip Connections & LayerNorm: ResNets and Transformers provide gradient highways (y = x + F(x)), ensuring signals flow back unattenuated."
        }
    ],
    "key_takeaways": [
        "The Chain Rule states that the derivative of nested composite functions is the product of intermediate derivatives.",
        "Backpropagation is the Chain Rule applied in reverse: gradients flow from Loss backward to early weights.",
        "Deep multiplication creates vanishing gradients (if terms < 1) or exploding gradients (if terms > 1).",
        "ReLU activations prevent vanishing gradients by maintaining a constant derivative of 1 for positive inputs.",
        "Skip connections (ResNets & Transformers) create gradient highways that preserve gradient signals across hundreds of layers."
    ],
    "definition_bullets": [
        "Chain Rule: Formula for composite derivatives: dy/dx = (dy/du) · (du/dx).",
        "Backpropagation: Applying the chain rule backward through neural layers to update weights.",
        "Vanishing / Exploding Gradients: Numerical instability caused by multiplying dozens of layer derivatives."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_chain_rule':
        concepts[idx] = chain_rule_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_chain_rule successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_chain_rule':
            all_concepts[idx] = chain_rule_concept
            break
    with open(ALL_CONCEPTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)
    print("Updated scripts/data_sources/all_concepts.json successfully!")

# 3. Update concepts_math.py
if os.path.exists(MATH_PY):
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_math", MATH_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    math_concepts = mod.MATH_CONCEPTS
    for idx, c in enumerate(math_concepts):
        if c['id'] == 'concept_chain_rule':
            math_concepts[idx] = chain_rule_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
