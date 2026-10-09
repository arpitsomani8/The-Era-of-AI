import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

partial_concept = {
    "id": "concept_partial_derivatives",
    "title": "Partial Derivatives & Slopes",
    "topic_id": "math_calc",
    "topic_label": "Calculus & Optimization Dynamics",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Partial Derivatives & Univariate Slopes",
    "def": "A partial derivative measures the rate of change of a multivariable function with respect to one single variable while holding all other variables constant as fixed values.",
    "formula": "$$\\frac{\\partial f}{\\partial w_i} = \\lim_{h \\to 0} \\frac{f(\\dots, w_i + h, \\dots) - f(\\dots, w_i, \\dots)}{h}, \\quad w_i \\leftarrow w_i - \\eta \\frac{\\partial \\text{Loss}}{\\partial w_i}$$",
    "logic": "Every time an AI learns from its mistakes, it calculates slopes. Partial derivatives isolate the individual sensitivity of the total loss to small perturbations of each specific weight, guiding gradient descent updates.",
    "example": "Predicting car price from mileage and age: ∂Price/∂Mileage tells you how much the price drops per extra mile driven, keeping car age strictly fixed.",
    "tags": [
        "Calculus",
        "Derivatives",
        "Partial Derivatives",
        "Gradient Descent",
        "Optimization",
        "Loss Function"
    ],
    "raw_sub": "Partial Derivatives & Univariate Slopes",
    "definition": "A slope measures rate of change (Rise / Run). A partial derivative (∂f/∂wᵢ) measures that slope for one specific variable while holding all other variables completely frozen as constants.",
    "formula_explanation": "∂Loss/∂wᵢ measures how fast the model's error changes when weight wᵢ is nudged while other weights remain frozen. Gradient descent updates wᵢ in the negative slope direction scaled by learning rate η.",
    "simple_summary": "In AI, learning means reducing errors. A partial derivative asks: 'If I tweak just this one weight by a tiny amount, does the error go up or down, and by how much?' The model then steps in the downhill direction.",
    "core_terms": [
        {
            "term": "Slope & Ordinary Derivative (df/dx)",
            "what_is_it": "• The rate of change of an output compared to an input: Rise / Run = Δy / Δx.\n• Answers: 'If I nudge x by a microscopic amount, by how much does y change, and in which direction?'",
            "analogy": "A car's speedometer: it doesn't tell you where you are, it tells you how fast your position changes per second.",
            "why_it_matters": "In single-variable functions, the sign tells you whether you are moving uphill (> 0), downhill (< 0), or on flat ground (= 0)."
        },
        {
            "term": "Partial Derivative (∂f / ∂wᵢ)",
            "what_is_it": "• The slope with respect to one variable while holding all other variables completely frozen as constants.\n• The Golden Rule: Treat every other variable as if it were a plain static number (like 5 or 10).",
            "analogy": "Baking a cake: if you add 1 extra gram of sugar while keeping flour, eggs, and oven temperature strictly identical, how much sweeter does the cake get?",
            "why_it_matters": "Neural networks have millions of weights; partial derivatives allow the model to measure and tweak each weight independently."
        },
        {
            "term": "The Gradient (∇f)",
            "what_is_it": "• A vector that bundles together all individual partial derivatives for every single weight in the network.\n• It always points in the direction of steepest increase (fastest way uphill).",
            "analogy": "Standing on a foggy mountain: the gradient vector is an arrow pointing straight up the steepest cliff.",
            "why_it_matters": "Taking the negative gradient (-∇f) points directly downhill to minimize model prediction error."
        }
    ],
    "types_header": "Slope Signs & Derivatives: What the AI Does",
    "types_badge": "Optimization Direction",
    "quick_types": [
        {
            "type": "Positive Slope (∂Loss/∂wᵢ > 0)",
            "definition": "Increasing weight wᵢ increases error (uphill slope).",
            "looks_like": "AI Action: Decrease wᵢ (step backward)"
        },
        {
            "type": "Negative Slope (∂Loss/∂wᵢ < 0)",
            "definition": "Increasing weight wᵢ decreases error (downhill slope).",
            "looks_like": "AI Action: Increase wᵢ (step forward)"
        },
        {
            "type": "Zero Slope (∂Loss/∂wᵢ = 0)",
            "definition": "Flat ground! Changing wᵢ causes zero change in error.",
            "looks_like": "AI Action: Stop / local minimum reached"
        },
        {
            "type": "Ordinary Derivative (df/dx)",
            "definition": "Rate of change in single-variable functions where only one input exists.",
            "looks_like": "Single variable: y = f(x)"
        },
        {
            "type": "Gradient Vector (∇f)",
            "definition": "Vector collecting all partial derivatives across every weight [∂f/∂w₁, ..., ∂f/∂wₙ]ᵀ.",
            "looks_like": "Direction of steepest uphill climb"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "∂ (del / partial)",
            "meaning": "Partial derivative symbol",
            "plain_english": "Indicates you are varying only one input while holding all others frozen"
        },
        {
            "symbol": "∂Loss / ∂wᵢ",
            "meaning": "Sensitivity of Loss with respect to weight wᵢ",
            "plain_english": "Rate at which prediction error changes when weight wᵢ nudges"
        },
        {
            "symbol": "wᵢ",
            "meaning": "Weight parameter i",
            "plain_english": "An individual learnable weight in the neural network"
        },
        {
            "symbol": "η (eta)",
            "meaning": "Learning rate",
            "plain_english": "Step size hyperparameter determining how far downhill to step"
        },
        {
            "symbol": "h (limit nudge)",
            "meaning": "Infinitesimal step size",
            "plain_english": "A microscopic nudge (as h → 0) used to calculate the instantaneous slope"
        }
    ],
    "numerical_example": "Differentiating f(x, y) = 3x²y + 5y³ step-by-step:\n\n1. Partial Derivative with respect to x (∂f/∂x):\n   • Freeze y as a constant.\n   • Differentiate x² → 2x, giving 3(2x)y = 6xy.\n   • 5y³ contains no x, so its derivative is 0!\n   --> ∂f/∂x = 6xy\n\n2. Partial Derivative with respect to y (∂f/∂y):\n   • Freeze x as a constant.\n   • In 3x²y, derivative of y is 1, leaving 3x²(1).\n   • In 5y³, derivative of y³ is 3y², giving 5(3y²) = 15y².\n   --> ∂f/∂y = 3x² + 15y²\n\n3. Evaluating at point (x = 1, y = 2):\n   • ∂f/∂x = 6(1)(2) = 12 (uphill along x)\n   • ∂f/∂y = 3(1)² + 15(2)² = 3 + 60 = 63 (steep uphill along y)\n   --> Gradient ∇f = [12, 63]ᵀ",
    "pitfalls": "Common Trap: Forgetting to freeze non-target variables as constants! When differentiating with respect to x, any term composed purely of y (like 5y³) has a derivative of exactly 0.",
    "core_logic": "Neural networks possess millions or billions of parameters. Partial derivatives isolate the individual sensitivity of the total loss to small perturbations of each specific weight.",
    "architectural_logic": "In backpropagation, autograd engines evaluate partial derivatives layer by layer using the chain rule. Every modern optimizer (SGD, Adam, RMSprop) directly consumes these partial derivatives to iteratively minimize loss.",
    "connected_logic": [
        {
            "title": "The Heartbeat of Machine Learning",
            "content": "• In AI, the Loss function measures prediction error: Loss = (Prediction - Target)².\n• Calculating ∂Loss/∂wᵢ tells the optimizer whether nudging each weight increases or decreases error, transforming guessing into mathematical optimization."
        },
        {
            "title": "The Golden Rule: Freeze All Other Variables",
            "content": "• When calculating ∂f/∂x, treat all other variables (y, z, w) as fixed constants.\n• Any pure constant term drops to 0, isolating the exact, independent sensitivity of that single parameter."
        },
        {
            "title": "The Gradient Descent Update Rule",
            "content": "• Weight update rule: wᵢ ← wᵢ - η · (∂Loss/∂wᵢ) uses the negative slope to step downhill.\n• Learning rate η controls step size: too large causes overshooting; too small crawls too slowly."
        },
        {
            "title": "From Single Slopes to the Full Gradient (∇f)",
            "content": "• Packaging all partial derivatives into a vector produces the Gradient ∇f, pointing in the steepest uphill direction.\n• Stepping in the negative gradient direction (-∇f) is the fastest way downhill to minimize loss."
        }
    ],
    "key_takeaways": [
        "A slope measures rate of change: Rise / Run = ΔOutput / ΔInput.",
        "A partial derivative (∂f/∂wᵢ) isolates the slope for one variable while freezing all other variables as constants.",
        "The sign of ∂Loss/∂w dictates the update: positive slope steps backward, negative slope steps forward.",
        "Gradient descent updates weights via wᵢ ← wᵢ - η · (∂Loss/∂wᵢ), where η is the learning rate.",
        "The Gradient (∇f) bundles all partial derivatives; the negative gradient (-∇f) points steepest downhill."
    ],
    "definition_bullets": [
        "Slope / Derivative: Rate of change (rise over run) describing output sensitivity to input changes.",
        "Partial Derivative (∂f/∂wᵢ): Slope along one parameter while holding all other parameters frozen.",
        "Gradient (∇f): Vector of all partial derivatives pointing in the direction of steepest ascent."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_partial_derivatives':
        concepts[idx] = partial_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_partial_derivatives successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_partial_derivatives':
            all_concepts[idx] = partial_concept
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
        if c['id'] == 'concept_partial_derivatives':
            math_concepts[idx] = partial_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
