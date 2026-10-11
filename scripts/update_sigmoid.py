import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    # 3. Load concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        py_content = f.read()

    sigmoid_data = {
        "id": "concept_sigmoid",
        "title": "Sigmoid Activation Function",
        "topic_id": "ml_logistic",
        "topic_label": "Logistic Regression & Sigmoid",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Sigmoid Function (S-curve mapping to [0, 1])",
        "def": "The Sigmoid activation function is a smooth, S-shaped mathematical function that squashes any real-valued number into a probability between 0 and 1.",
        "formula": "$$\\sigma(z) = \\frac{1}{1 + e^{-z}}, \\quad \\frac{d\\sigma}{dz} = \\sigma(z)(1 - \\sigma(z))$$",
        "logic": "A linear equation z = w^T x + b can produce any unbounded number from -∞ to +∞. Sigmoid converts this raw score into a calibrated probability percentage (0 to 1), where positive scores map above 0.5 and negative scores map below 0.5.",
        "example": "Predicting email spam: A model calculates a raw logit score of z = 2.197. Passing this through Sigmoid yields σ(2.197) = 1 / (1 + e^-2.197) = 0.90, giving an intuitive 90% spam probability.",
        "tags": [
            "Sigmoid",
            "Activation Function",
            "Logistic Regression",
            "Binary Classification",
            "Vanishing Gradient",
            "Logits"
        ],
        "definition": "The Sigmoid activation function is a smooth, S-shaped mathematical function that squashes any real-valued number into a probability between 0 and 1.",
        "formula_explanation": "",
        "simple_summary": "Think of Sigmoid as a volume limiter for numbers. A raw machine learning score can be anything from -1,000 to +5,000. Sigmoid smoothly squashes all those wild numbers into a clean percentage between 0% and 100%. A score of 0 lands right at 50% (uncertain), big positive scores rise close to 100%, and big negative scores drop close to 0%.",
        "core_terms": [
            {
                "term": "Raw Score / Logit (z)",
                "what_is_it": "• The unbounded linear combination calculated by a neuron: z = w₁x₁ + w₂x₂ + b.\n• Can be any real number from -∞ to +∞ before being squashed by an activation function.",
                "analogy": "The raw point score on an ungraded exam before being converted into a letter grade percentage.",
                "why_it_matters": "Represents the model's raw evidence; positive evidence favors class 1, while negative evidence favors class 0."
            },
            {
                "term": "Probability Squashing (0 to 1)",
                "what_is_it": "• The transformation σ(z) = 1 / (1 + e^-z) strictly bounds the output between 0.0 and 1.0.\n• It never reaches exactly 0 or 1 for any finite input, preventing false 100% certainty.",
                "analogy": "A dimmer switch on a lamp that smoothly adjusts brightness between completely off (0) and fully bright (1).",
                "why_it_matters": "Turns abstract mathematical scores into interpretable probability percentages that humans and decision systems can trust."
            },
            {
                "term": "The S-Curve Midpoint (z = 0)",
                "what_is_it": "• When the input is exactly 0, e^-0 = 1, giving σ(0) = 1 / (1 + 1) = 0.50.\n• Represents the point of maximum uncertainty where the evidence is equally split between both classes.",
                "analogy": "A perfectly balanced teeter-totter resting on its central fulcrum.",
                "why_it_matters": "Serves as the natural default threshold: scores with z > 0 predict Class 1, while scores with z < 0 predict Class 0."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "z",
                "meaning": "Raw Logit Score",
                "plain_english": "The linear sum (w^T x + b) fed into the sigmoid function"
            },
            {
                "symbol": "e",
                "meaning": "Euler's Number",
                "plain_english": "A mathematical constant approximately equal to 2.71828"
            },
            {
                "symbol": "e^-z",
                "meaning": "Exponential Decay Term",
                "plain_english": "Shrinks close to 0 for large positive z, and grows huge for large negative z"
            },
            {
                "symbol": "σ(z)",
                "meaning": "Sigmoid Probability",
                "plain_english": "The squashed output value strictly inside the interval (0, 1)"
            },
            {
                "symbol": "σ'(z)",
                "meaning": "Sigmoid Derivative",
                "plain_english": "σ(z)(1 - σ(z)): The slope used during backpropagation to update weights"
            }
        ],
        "numerical_example": "Evaluating 3 Distinct Raw Scores:\nFormula: σ(z) = 1 / (1 + e^-z)\n\n1. Zero Input (z = 0 — Perfectly Balanced / Uncertain):\n• σ(0) = 1 / (1 + e^0) = 1 / (1 + 1) = 0.50 (50% probability; a coin flip)\n\n2. Strong Positive Score (z = +2.0 — Confident Class 1):\n• e^-2.0 ≈ 0.1353\n• σ(2.0) = 1 / (1 + 0.1353) = 1 / 1.1353 ≈ 0.8808 (88.1% probability of Class 1)\n\n3. Strong Negative Score (z = -2.0 — Confident Class 0):\n• e^-(-2.0) = e^2.0 ≈ 7.389\n• σ(-2.0) = 1 / (1 + 7.389) = 1 / 8.389 ≈ 0.1192 (11.9% probability of Class 1, meaning 88.1% probability of Class 0!)\n\nTakeaway: Perfect symmetry around zero: σ(-z) = 1 - σ(z).",
        "pitfalls": "Common Mistakes to Avoid:\n1. Using Sigmoid in deep hidden layers: When |z| > 5, the curve saturates and flattens out, causing derivatives to vanish (σ' → 0) and freezing early layers. Use ReLU instead for hidden layers!\n2. Not being zero-centered: Sigmoid outputs are strictly positive (0 to 1), causing all gradients entering the next layer to share the same sign and producing zigzagging optimization paths.\n3. Separating Sigmoid and BCELoss in PyTorch: Running torch.sigmoid() followed by nn.BCELoss() can cause numerical underflow and NaN crashes; always use nn.BCEWithLogitsLoss() instead.\n4. Treating the 0.5 threshold as permanent: For imbalanced datasets (e.g., fraud occurring in only 0.1% of transactions), keeping the threshold at 0.5 misses most fraud cases; tune the decision threshold downwards.\n5. Assuming probabilities are perfectly calibrated: A model outputting σ(z) = 0.99 can still be overconfident if trained without regularization or under distribution shift.",
        "core_logic": "Why this matters: Machine learning models need non-linear activations to learn complex relationships beyond straight lines. Sigmoid was the original breakthrough activation function because it is smooth, continuous, differentiable everywhere, and maps unbounded linear combinations directly into valid Bernoulli probability distributions.",
        "architectural_logic": "In PyTorch models, avoid using nn.Sigmoid() on the final layer during training. Instead, output raw logits directly and pair them with nn.BCEWithLogitsLoss(). For production inference, apply torch.sigmoid(logits) only when presenting final probability percentages to end users.",
        "key_takeaways": [
            "Squashes to Probabilities: Maps any input from -∞ to +∞ strictly into the range (0, 1).",
            "Midpoint at Zero: A logit score of 0 produces exactly 0.50 probability (the natural binary boundary).",
            "Saturates on Extremes: Large positive or negative inputs cause vanishing gradients; use ReLU for deep hidden layers.",
            "Use BCEWithLogitsLoss: Always combine logits and binary cross-entropy in a single stable operation in PyTorch."
        ],
        "definition_bullets": [
            "Sigmoid Function: A non-linear mathematical activation function that squashes real-valued inputs into the range (0, 1).",
            "Saturation: The flat plateau regions of the Sigmoid curve (|z| > 5) where gradients approach zero and stall neural network learning."
        ],
        "types_header": "Where Sigmoid is Used in Modern AI",
        "types_badge": "Architectural Roles",
        "quick_types": [
            {
                "type": "Binary Output Layer (Logistic Regression & Neural Nets)",
                "definition": "Squashes the final single neuron into a probability p ∈ (0, 1) for yes/no classifications.",
                "looks_like": "output = torch.sigmoid(final_linear(x))"
            },
            {
                "type": "Multi-Label Classification Output",
                "definition": "Applied to every output neuron independently when an example can belong to multiple non-exclusive classes simultaneously.",
                "looks_like": "probs = torch.sigmoid(multi_tag_logits)"
            },
            {
                "type": "Recurrent Gating Mechanisms (LSTM & GRU)",
                "definition": "Used inside memory gates (input gate, forget gate) as a soft on/off switch deciding how much information to keep or erase.",
                "looks_like": "forget_gate = torch.sigmoid(W_f @ x + b_f)"
            },
            {
                "type": "BCEWithLogitsLoss (Fused Implementation)",
                "definition": "PyTorch's combined operator that computes Sigmoid and Log Loss together via the log-sum-exp trick for numerical stability.",
                "looks_like": "criterion = nn.BCEWithLogitsLoss()"
            }
        ],
        "connected_logic": [
            {
                "title": "The Vanishing Gradient Problem (Why ReLU Won)",
                "content": "• The derivative of Sigmoid is σ'(z) = σ(z)(1 - σ(z)), which peaks at only 0.25 when z = 0 and rapidly plummets to 0 when |z| > 5.\n• In a 10-layer network, multiplying ten gradients ≤ 0.25 causes the backpropagation signal to shrink by 0.25¹⁰ ≈ 10⁻⁶.\n• Early layers receive virtually zero gradient and freeze completely, which is why modern architectures use ReLU (f(z) = max(0, z)) for hidden layers."
            },
            {
                "title": "The Elegant Derivative Trick in Backpropagation",
                "content": "• You never need to recalculate expensive exponential functions e^-z during the backward pass!\n• Once you compute the forward activation a = σ(z), its derivative is obtained through a single cheap subtraction: a · (1 - a).\n• This algebraic shortcut makes backpropagation significantly faster on GPUs."
            },
            {
                "title": "Sigmoid vs. Softmax: What is the Difference?",
                "content": "• Sigmoid handles binary classification (1 neuron) or multi-label tasks (multiple independent yes/no tags where probabilities do NOT sum to 1.0).\n• Softmax handles multi-class single-choice problems across 3 or more mutually exclusive classes (e.g., cat vs dog vs bird), mathematically forcing all probabilities to sum to exactly 1.0."
            },
            {
                "title": "The S-Curve Symmetry Property (σ(-z) = 1 - σ(z))",
                "content": "• Because e^-z = 1 / e^z, Sigmoid is mathematically symmetric around the origin: σ(-z) = 1 - σ(z).\n• If a model predicts an 88% probability that an email is spam (z = +2.0), reversing the evidence sign to z = -2.0 yields exactly a 12% probability (1 - 0.88).\n• This ensures the model treats positive and negative evidence with identical mathematical balance."
            }
        ]
    }

    # 1. Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_sigmoid":
            c.update(sigmoid_data)
            print("Updated concept_sigmoid in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # 2. Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_sigmoid":
            c.update(sigmoid_data)
            print("Updated concept_sigmoid in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # 3. Update in concepts_ml.py
    pattern = r'\{\s*"id":\s*"concept_sigmoid".*?\},(?=\s*\{\s*"id":\s*"concept_decision_threshold")'
    match = re.search(pattern, py_content, re.DOTALL)
    if match:
        lines = json.dumps(sigmoid_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        py_content = py_content[:match.start()] + indented_replacement + py_content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(py_content)
        print("Updated concept_sigmoid in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
