import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

hessian_concept = {
    "id": "concept_hessian_matrix",
    "title": "Hessian Matrix & 2nd Order Curvature",
    "topic_id": "math_calc",
    "topic_label": "Calculus & Optimization Dynamics",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Hessian Matrix (2nd order curvature & saddle points)",
    "def": "The Hessian is an n × n symmetric square matrix of second-order partial derivatives describing the local curvature and bending of a multi-variable loss surface.",
    "formula": "$$H_{ij} = \\frac{\\partial^2 f}{\\partial w_i \\partial w_j}, \\quad w \\leftarrow w - H^{-1} \\nabla f, \\quad H = Q \\Lambda Q^T$$",
    "logic": "The gradient tells us how quickly a function changes, while the Hessian tells us how that rate of change itself changes. When the gradient is zero (∇L = 0), the eigenvalues of the Hessian determine whether the point is a local minimum, maximum, or saddle point.",
    "example": "For f(x, y) = x² - y² at (0, 0), the gradient is [0, 0]ᵀ and Hessian eigenvalues are λ₁ = 2 and λ₂ = -2. Because the signs are mixed, (0, 0) is proven to be a saddle point.",
    "tags": [
        "Hessian Matrix",
        "Second Order Curvature",
        "Saddle Points",
        "Newton Method",
        "Optimization",
        "Calculus"
    ],
    "raw_sub": "Hessian Matrix (2nd order curvature & saddle points)",
    "definition": "The Hessian matrix organizes all second-order partial derivatives into a symmetric matrix (H = Hᵀ), capturing how a loss surface bends in every direction to classify minima, maxima, and saddle points.",
    "formula_explanation": "H contains second partial derivatives H_{ij} = ∂²f/∂wᵢ∂wⱼ. Newton's method uses H⁻¹ to adjust step sizes by local curvature. The diagonal matrix Λ contains eigenvalues measuring curvature along orthogonal principal axes Q.",
    "simple_summary": "The gradient tells you the slope under your feet; the Hessian tells you if the ground is curving into a bowl, a dome, or a horse saddle. It is the curvature compass of optimization.",
    "core_terms": [
        {
            "term": "Hessian Matrix (H or ∇²f)",
            "what_is_it": "• An n × n square matrix collecting all possible second-order partial derivatives of a multivariable function: H_{ij} = ∂²f/∂wᵢ∂wⱼ.\n• While the gradient measures slope (rate of change), the Hessian measures curvature (how that slope itself changes).",
            "analogy": "A car speedometer vs. accelerometer: the gradient tells you your current speed; the Hessian tells you if you are accelerating, braking, or turning a curve.",
            "why_it_matters": "When the gradient is zero (∇L = 0), only the Hessian can distinguish whether you reached a true minimum, a maximum, or a saddle point."
        },
        {
            "term": "2nd-Order Curvature (Bowl, Dome, Saddle)",
            "what_is_it": "• Curvature measures how a surface bends across dimensions.\n• Stationary points fall into 3 shapes: Bowl (curves up in all directions → minimum), Dome (curves down in all directions → maximum), and Saddle (curves up in one direction, down in another).",
            "analogy": "A Pringle potato chip: it curves upward in one direction to hold dip, but curves downward along the outer edges to fit into the can.",
            "why_it_matters": "In high-dimensional neural networks, almost all flat regions are saddle points where naive optimization stalls out."
        },
        {
            "term": "The Symmetry Miracle (Schwarz's Theorem)",
            "what_is_it": "• Because mixed partial derivatives are equal (∂²f/∂x∂y = ∂²f/∂y∂x), the Hessian matrix is ALWAYS symmetric (H = Hᵀ).\n• By the Spectral Theorem, this guarantees all Hessian eigenvalues are real numbers and its eigenvectors are mutually perpendicular (orthogonal).",
            "analogy": "A square mirror folded across the diagonal: every off-diagonal entry on the top right perfectly matches its partner on the bottom left.",
            "why_it_matters": "Ensures the loss surface can be cleanly rotated into independent principal curvature axes via eigenvalue decomposition."
        }
    ],
    "types_header": "Hessian Eigenvalues & Surface Shapes (at ∇L = 0)",
    "types_badge": "Curvature Classification",
    "quick_types": [
        {
            "type": "Positive Definite (All λᵢ > 0)",
            "definition": "Curves upward in every direction like a bowl.",
            "looks_like": "Shape: Bowl → Local Minimum (Success in ML!)"
        },
        {
            "type": "Negative Definite (All λᵢ < 0)",
            "definition": "Curves downward in every direction like an umbrella or dome.",
            "looks_like": "Shape: Dome → Local Maximum (Worst point)"
        },
        {
            "type": "Indefinite (Mixed: some λ > 0, some λ < 0)",
            "definition": "Curves upward along some directions and downward along others.",
            "looks_like": "Shape: Pringle / Horse Saddle → Saddle Point"
        },
        {
            "type": "Semi-Definite / Singular (At least one λ = 0)",
            "definition": "Completely flat along at least one direction; curvature test is inconclusive.",
            "looks_like": "Shape: Flat Valley Ridge / Gutter"
        },
        {
            "type": "High-Dimensional Reality in AI",
            "definition": "With millions of parameters, having all λ > 0 simultaneously is virtually impossible.",
            "looks_like": "Almost all flat regions in LLMs are Saddle Points"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "H (∇²f)",
            "meaning": "Hessian Matrix",
            "plain_english": "n × n symmetric matrix of all second-order partial derivatives"
        },
        {
            "symbol": "∂²f / ∂wᵢ∂wⱼ",
            "meaning": "Second partial derivative",
            "plain_english": "Rate of change of the slope with respect to parameters wᵢ and wⱼ"
        },
        {
            "symbol": "H⁻¹",
            "meaning": "Inverse Hessian",
            "plain_english": "Curvature scaler in Newton's Method (w ← w - H⁻¹∇f)"
        },
        {
            "symbol": "∇f",
            "meaning": "First-order gradient vector",
            "plain_english": "Slope vector indicating directional uphill climb"
        },
        {
            "symbol": "Λ (Lambda)",
            "meaning": "Eigenvalue diagonal matrix",
            "plain_english": "Values (λ₁, ..., λₙ) measuring curvature along principal axes"
        }
    ],
    "numerical_example": "Analyzing critical point of f(x, y) = x² - y² at (0, 0):\n\n1. First Partial Derivatives (Gradient):\n   • ∂f/∂x = 2x\n   • ∂f/∂y = -2y\n   At (0, 0): ∇f = [0, 0]ᵀ  (Ground is completely flat!)\n\n2. Second Partial Derivatives (Hessian Matrix H):\n   • ∂²f/∂x² = 2\n   • ∂²f/∂y² = -2\n   • ∂²f/∂x∂y = ∂²f/∂y∂x = 0\n   --> H = [[ 2,  0],\n            [ 0, -2]]\n\n3. Evaluate Hessian Eigenvalues:\n   • λ₁ = +2 (positive curvature: curves UP like a bowl along x)\n   • λ₂ = -2 (negative curvature: curves DOWN like a dome along y)\n\nConclusion:\nBecause eigenvalues have mixed signs (+2 and -2), (0, 0) is conclusively a Saddle Point!",
    "pitfalls": "Common Trap: Assuming ∇L = 0 means you reached a local minimum. In high-dimensional deep learning, almost every flat spot is a saddle point! Relying on first-order gradients alone cannot tell whether you are trapped on a saddle or in a true minimum.",
    "core_logic": "The gradient tells us how quickly a function changes, while the Hessian tells us how that rate of change itself changes. When the gradient is zero (∇L = 0), the eigenvalues of the Hessian determine whether the point is a local minimum, maximum, or saddle point.",
    "architectural_logic": "While Newton's method is computationally prohibitive for deep networks (O(n²) memory and O(n³) inversion), modern optimizers like Adam and RMSprop use running averages of squared gradients as a diagonal curvature proxy. Meanwhile, SGD mini-batch noise acts as stochastic vibration, helping models escape high-dimensional saddle points.",
    "connected_logic": [
        {
            "title": "Why the Gradient Leaves Us Blind at ∇L = 0",
            "content": "• When ∇L(w) = 0, first-order slope cannot distinguish between a local minimum (bowl), maximum (dome), or saddle point (Pringle chip).\n• Second derivatives inside the Hessian matrix reveal how the surface bends, providing the curvature map needed to identify the true terrain."
        },
        {
            "title": "The Curse of O(n²) Memory and O(n³) Inversion",
            "content": "• Newton's Method (w ← w - H⁻¹∇f) adapts step sizes to curvature, but storing H requires n² memory and n³ operations to invert.\n• For a 1-billion parameter model, storing H would demand exabytes of RAM, making exact 2nd-order optimization impossible in deep learning."
        },
        {
            "title": "How Modern AI Approximates Curvature",
            "content": "• Quasi-Newton (L-BFGS): Tracks recent gradient histories to approximate curvature vectors without forming the full matrix.\n• Adaptive Optimizers (Adam, RMSprop): Track running averages of squared gradients (g²), serving as a cheap diagonal proxy for 2nd-order curvature."
        },
        {
            "title": "The Saddle Point Reality & Why SGD Succeeds",
            "content": "• In a 1-million parameter neural network, reaching a local minimum requires all 1,000,000 eigenvalues to be positive simultaneously (astronomically rare).\n• Mini-batch noise in SGD acts as natural physical vibration, shaking parameters away from saddle points to slide down negative curvature escape routes."
        }
    ],
    "key_takeaways": [
        "The Hessian matrix (H) contains all second-order partial derivatives and measures multivariable curvature.",
        "The Hessian is always symmetric (H = Hᵀ) by Clairaut's theorem, guaranteeing real eigenvalues.",
        "Hessian eigenvalues classify flat points: all positive = local minimum; all negative = local maximum; mixed = saddle point.",
        "Newton's method (w ← w - H⁻¹∇f) is computationally intractable for deep networks due to O(n²) memory and O(n³) inversion.",
        "Modern AI uses Adam/RMSprop as diagonal curvature proxies, while SGD batch noise helps escape high-dimensional saddle points."
    ],
    "definition_bullets": [
        "Hessian Matrix (H): Square matrix of second derivatives describing surface bending and curvature.",
        "Saddle Point: Stationary point with mixed positive and negative curvature (indefinite Hessian).",
        "Newton's Method: Second-order optimization using H⁻¹ to jump directly to minima, approximated by modern optimizers."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_hessian_matrix':
        concepts[idx] = hessian_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_hessian_matrix successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_hessian_matrix':
            all_concepts[idx] = hessian_concept
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
        if c['id'] == 'concept_hessian_matrix':
            math_concepts[idx] = hessian_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
