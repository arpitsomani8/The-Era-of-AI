import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

convex_concept = {
    "id": "concept_convex_optimization",
    "title": "Convex vs Non-Convex Loss Landscapes",
    "topic_id": "math_calc",
    "topic_label": "Calculus & Optimization Dynamics",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Convex vs Non-Convex Loss Landscapes",
    "def": "A function is convex if the straight line between any two points lies on or above the graph. Convex landscapes have a single unique global minimum, whereas non-convex landscapes have multiple valleys, hills, and saddle points.",
    "formula": "$$f(\\alpha x + (1-\\alpha)y) \\le \\alpha f(x) + (1-\\alpha)f(y) \\quad \\forall \\alpha \\in [0, 1], \\quad H(w) \\succeq 0$$",
    "logic": "Classical models (Linear/Logistic Regression) are convex, guaranteeing a single optimal solution. Deep neural networks are non-convex due to non-linear activations and weight products, but overparameterization and SGD naturally guide them to wide, flat basins that generalize well.",
    "example": "Convex bowl f(x) = x² has a single bottom at x = 0. Non-convex mountain range g(x) = x⁴ - 4x² has two separate valleys at x = ±√2 separated by a hill at x = 0.",
    "tags": [
        "Convex Optimization",
        "Non-Convex Landscapes",
        "Loss Landscapes",
        "Global Minimum",
        "Flat Minima",
        "Calculus"
    ],
    "raw_sub": "Convex vs Non-Convex Loss Landscapes",
    "definition": "A function is convex if any straight line segment between two points never falls below the curve. In optimization, convex functions guarantee a single global minimum, while non-convex functions feature multiple local minima and saddle points.",
    "formula_explanation": "The secant line inequality states that any point on the chord between (x, f(x)) and (y, f(y)) sits above the function curve. For twice-differentiable functions, convexity is equivalent to the Hessian matrix being positive semi-definite (H ⪰ 0) everywhere.",
    "simple_summary": "A convex landscape is a salad bowl: drop a marble anywhere, and it always rolls to the single lowest bottom. A non-convex landscape is a mountain range: where you land depends on where you started, but modern AI easily finds great valleys.",
    "core_terms": [
        {
            "term": "The Loss Landscape",
            "what_is_it": "• The multi-dimensional terrain showing how model error changes across all possible combinations of weights and biases.\n• Low points are valleys (low loss, accurate predictions); high points are peaks (high loss, poor predictions).",
            "analogy": "An expansive mountain range where each coordinate is a setting of parameters, and the altitude is the model's error rate.",
            "why_it_matters": "Optimization is simply navigation: guiding an algorithm blindfolded across this landscape to locate the lowest valley floor."
        },
        {
            "term": "Convex Landscape (The Salad Bowl)",
            "what_is_it": "• A smooth, bowl-shaped terrain where any straight line between two points lies entirely on or above the surface.\n• Has exactly ONE global minimum, zero false valleys, and zero saddle points—any point where ∇L = 0 is guaranteed to be optimal.",
            "analogy": "A smooth salad bowl: wherever you drop a marble, it is mathematically guaranteed to roll to the exact same center bottom.",
            "why_it_matters": "Governs classical ML (Linear and Logistic Regression), guaranteeing a single perfect answer regardless of weight initialization."
        },
        {
            "term": "Non-Convex Landscape (The Mountain Range)",
            "what_is_it": "• A rugged terrain filled with countless peaks, cliffs, plateaus, saddle points, and local valleys (e.g., f(x) = x⁴ - 4x²).\n• Finding the absolute global minimum is NP-hard, but modern optimizers easily find wide, 'good enough' valleys that generalize well.",
            "analogy": "The Himalayas: walking downhill might land you in a high mountain lake rather than sea level, but that valley is still comfortably low.",
            "why_it_matters": "Describes all deep neural networks (CNNs, Transformers, LLMs), requiring stochastic optimizers (SGD, Adam) to navigate."
        }
    ],
    "types_header": "Convex vs. Non-Convex: The Grand Divide in AI",
    "types_badge": "Optimization Comparison",
    "quick_types": [
        {
            "type": "Terrain Geometry",
            "definition": "Convex: Smooth bowl with 1 minimum. Non-Convex: Rugged mountain range with billions of valleys and saddles.",
            "looks_like": "Salad Bowl (x²) vs. Mountain Peaks (x⁴ - 4x²)"
        },
        {
            "type": "Model Families",
            "definition": "Convex: Linear/Logistic Regression, SVMs. Non-Convex: MLPs, CNNs, Transformers, LLMs (GPT, Gemini).",
            "looks_like": "Classical ML vs. Modern Deep Learning"
        },
        {
            "type": "Mathematical Guarantees",
            "definition": "Convex: Guaranteed global optimum. Non-Convex: No guarantee of absolute minimum, but finds low-loss basins.",
            "looks_like": "Proven Optimum vs. Empirically Excellent"
        },
        {
            "type": "Initialization Sensitivity",
            "definition": "Convex: Zero sensitivity (start anywhere, reach the same point). Non-Convex: High sensitivity (requires smart init like He/Xavier).",
            "looks_like": "Robust from any start vs. Init-dependent"
        },
        {
            "type": "Generalization (Flat vs. Sharp Minima)",
            "definition": "Sharp pits overfit on test shifts; wide flat basins maintain low loss and generalize cleanly.",
            "looks_like": "SGD/Adam naturally settles into flat basins"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "f",
            "meaning": "Loss / Objective function",
            "plain_english": "The function mapping parameter weights to prediction error"
        },
        {
            "symbol": "x, y",
            "meaning": "Parameter coordinates",
            "plain_english": "Any two distinct points in the parameter weight space"
        },
        {
            "symbol": "α (alpha) ∈ [0, 1]",
            "meaning": "Secant line weighting",
            "plain_english": "Defines the straight line segment connecting points x and y"
        },
        {
            "symbol": "f(αx + (1-α)y)",
            "meaning": "Curve value along segment",
            "plain_english": "The value of the function on the curve beneath the secant line"
        },
        {
            "symbol": "H(w) ⪰ 0",
            "meaning": "Positive semi-definite Hessian",
            "plain_english": "Hessian matrix has all eigenvalues ≥ 0 everywhere, curving upward"
        }
    ],
    "numerical_example": "Comparing 1D Convex f(x) = x² vs. Non-Convex g(x) = x⁴ - 4x²:\n\n1. Convex Function f(x) = x²:\n   • First derivative: f'(x) = 2x = 0  ==>  x = 0\n   • Second derivative: f''(x) = 2 > 0 (Positive everywhere!)\n   --> Exactly 1 critical point at x = 0, guaranteed to be the global minimum.\n\n2. Non-Convex Function g(x) = x⁴ - 4x²:\n   • First derivative: g'(x) = 4x³ - 8x = 4x(x² - 2) = 0\n   --> Three critical points: x = 0, x = -√2 (-1.414), x = +√2 (+1.414)\n   • Second derivative: g''(x) = 12x² - 8:\n     - At x = 0: g''(0) = -8 < 0  ==>  Local Maximum (peak)!\n     - At x = ±√2: g''(±√2) = 12(2) - 8 = +16 > 0  ==>  Two separate Local Minima!\n\nOutcome:\nStarting gradient descent at x = 0.1 rolls right to +√2; starting at x = -0.1 rolls left to -√2. Starting position determines which valley is reached!",
    "pitfalls": "Common Trap: Believing non-convex means unoptimizable. While finding the global minimum is theoretically NP-hard, overparameterized neural networks have thousands of equally good flat basins, so finding the absolute lowest point is not necessary for state-of-the-art accuracy.",
    "core_logic": "Linear Regression and Logistic Regression are convex (guaranteed global optimum with standard gradient descent). Deep Neural Networks are non-convex with countless saddle points, requiring momentum, adaptive learning rates, and overparameterization to escape plateaus.",
    "architectural_logic": "Without skip connections, deep networks suffer from chaotic, highly non-convex loss landscapes where gradients shatter. ResNet and Transformer residual connections (x + F(x)) smooth the loss surface into near-convex bowls, allowing stable convergence across hundreds of layers.",
    "connected_logic": [
        {
            "title": "The Secant Line Test & Hessian Connection",
            "content": "• Secant Line Test: A function is convex if the straight line chord between any two points lies on or above the curve.\n• Hessian Connection: A twice-differentiable function is convex if and only if its Hessian is positive semi-definite (H ⪰ 0) everywhere, curving upward across all coordinates."
        },
        {
            "title": "Why Deep Neural Networks are Non-Convex",
            "content": "• Non-linear activations (ReLU, GELU) fold space, while layer weight products (W₂ × W₁) inherently create saddle curvature (x · y).\n• Permutation symmetry: Swapping hidden neurons yields mathematically identical outputs, creating N! equivalent minima across the landscape."
        },
        {
            "title": "The Deep Learning Paradox: Overparameterization & Flat Minima",
            "content": "• In massive networks with billions of weights, almost all reached valleys have virtually identical low loss depths.\n• SGD naturally bounces out of sharp, brittle pits and settles into wide, flat basins that generalize robustly when test data shifts."
        },
        {
            "title": "The ResNet Miracle: Landscape Smoothing via Skip Connections",
            "content": "• Without skip connections, deep networks produce chaotic, crumpled loss landscapes that trap optimizers.\n• Adding residual connections (y = x + F(x)) smooths the chaotic terrain into near-convex bowls, allowing gradients to flow effortlessly."
        }
    ],
    "key_takeaways": [
        "A convex function has a single global minimum; any line between two points lies above the graph.",
        "A function is convex if its Hessian is positive semi-definite (H ⪰ 0) everywhere on the landscape.",
        "Classical ML (Linear/Logistic Regression) is convex; Deep Learning (Transformers, CNNs) is non-convex.",
        "Deep networks are non-convex due to non-linear activations, layer multiplication, and neuron permutation symmetries.",
        "Overparameterization and SGD help deep models find wide, flat minima that generalize well to unseen test data."
    ],
    "definition_bullets": [
        "Convex Landscape: Bowl-shaped loss surface with a single guaranteed global minimum and no saddle points.",
        "Non-Convex Landscape: Complex terrain with multiple local minima, plateaus, and saddle points.",
        "Flat Minima: Wide, gentle loss basins discovered by SGD that generalize reliably to new data."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_convex_optimization':
        concepts[idx] = convex_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_convex_optimization successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_convex_optimization':
            all_concepts[idx] = convex_concept
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
        if c['id'] == 'concept_convex_optimization':
            math_concepts[idx] = convex_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
