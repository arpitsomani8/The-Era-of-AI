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
        "def": "An activation function transforms a neuron's raw input score into its final output. The Sigmoid function is a specific activation function that converts any real-valued number into a probability between 0 and 1.",
        "formula": "$$\\sigma(z) = \\frac{1}{1 + e^{-z}}, \\quad \\text{where } z = w_1 x_1 + w_2 x_2 + b$$",
        "logic": "A neuron first calculates a raw score (z) by multiplying input features by learned weights and adding a bias. Because this raw score can be any positive or negative number, the Sigmoid activation function squashes it into an S-shaped curve between 0 and 1, making it ideal for predicting probabilities in binary classification.",
        "example": "Detecting spam: A neuron calculates a raw score of z = 2.1 from email features. Passing this score through the Sigmoid function gives σ(2.1) = 1 / (1 + e^-2.1) ≈ 0.89, which means the model predicts an 89% probability that the email is spam.",
        "tags": [
            "Sigmoid",
            "Activation Function",
            "Logistic Regression",
            "Binary Classification",
            "Probability",
            "Neural Networks"
        ],
        "definition": "An activation function transforms a neuron's raw input score into its final output. The Sigmoid function is a specific activation function that converts any real-valued number into a probability between 0 and 1.",
        "formula_explanation": "",
        "simple_summary": "Inside a neural network or logistic regression model, a neuron first calculates a raw score by combining inputs, weights, and bias. An activation function takes that raw score and decides what the neuron should actually output. The Sigmoid function is an S-shaped curve that squashes any raw score—no matter how huge or negative—into a clean percentage between 0% and 100%. A score of 0 becomes 50%, positive scores rise toward 100%, and negative scores drop toward 0%.",
        "core_terms": [
            {
                "term": "What is an Activation Function?",
                "what_is_it": "• A mathematical function that takes a neuron's raw calculated score (z) and transforms it into its final output (a).\n• Without activation functions, neural networks would only be simple linear equations unable to learn complex patterns.",
                "analogy": "Like a brain cell deciding how strongly to fire: it receives electrical signals (inputs), processes them, and fires an output signal to the next cell.",
                "why_it_matters": "Introduces non-linearity into machine learning models, allowing them to learn curved decision boundaries and complex real-world data."
            },
            {
                "term": "What is the Sigmoid Function?",
                "what_is_it": "• A smooth, S-shaped activation function defined as σ(z) = 1 / (1 + e^-z).\n• Binds all outputs strictly between 0 and 1, making it the classic choice for binary classification (yes/no decisions).",
                "analogy": "A dimmer switch on a light: instead of only clicking hard ON or OFF, it smoothly adjusts brightness between 0% (off) and 100% (fully lit).",
                "why_it_matters": "The core mathematical function that powers Logistic Regression and output probability layers in binary neural networks."
            },
            {
                "term": "The Raw Score / Logit (z)",
                "what_is_it": "• The raw linear combination calculated before activation: z = w₁x₁ + w₂x₂ + b.\n• It can be any real number from -∞ to +∞ before being squashed by Sigmoid.",
                "analogy": "The raw point score on an ungraded exam before the teacher converts it into a final percentage grade.",
                "why_it_matters": "Represents the net evidence collected by the model: positive evidence favors Class 1, while negative evidence favors Class 0."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "x₁, x₂",
                "meaning": "Input Features",
                "plain_english": "The measurable data values fed into the neuron (e.g. email length, word count)"
            },
            {
                "symbol": "w₁, w₂",
                "meaning": "Learned Weights",
                "plain_english": "The importance values the model learned for each feature during training"
            },
            {
                "symbol": "b",
                "meaning": "Bias",
                "plain_english": "The baseline offset added to the score, independent of the inputs"
            },
            {
                "symbol": "z",
                "meaning": "Raw Score (Pre-Activation)",
                "plain_english": "The linear sum z = w₁x₁ + w₂x₂ + b before applying the activation function"
            },
            {
                "symbol": "σ(z)",
                "meaning": "Sigmoid Output (Probability)",
                "plain_english": "The final activated output value strictly between 0 and 1"
            },
            {
                "symbol": "e",
                "meaning": "Euler's Number",
                "plain_english": "A mathematical constant approximately equal to 2.71828"
            }
        ],
        "numerical_example": "Step-by-Step Calculation for a Single Neuron:\n\nSuppose a model predicts whether a bank transaction is fraud:\n• Input Features: Transaction Amount x₁ = 3.0, Distance from Home x₂ = 2.0\n• Learned Parameters: Weight w₁ = 0.5, Weight w₂ = 0.8, Bias b = -1.0\n\nStep 1: Calculate the Raw Score (z)\nz = (w₁ · x₁) + (w₂ · x₂) + b\nz = (0.5 · 3.0) + (0.8 · 2.0) - 1.0\nz = 1.5 + 1.6 - 1.0 = 2.1\n\nStep 2: Apply the Sigmoid Function\nσ(z) = 1 / (1 + e^-z) = 1 / (1 + e^-2.1)\nSince e^-2.1 ≈ 0.1225:\nσ(2.1) = 1 / (1 + 0.1225) = 1 / 1.1225 ≈ 0.8909\n\nResult: The raw score of 2.1 is converted into an 89.1% probability of fraud!",
        "pitfalls": "Common Mistakes to Avoid:\n1. Thinking Sigmoid can reach exactly 0 or 1: For any real number, Sigmoid stays strictly inside (0, 1); it gets infinitely close but never touches 0 or 1.\n2. Using Sigmoid in deep hidden layers: For large inputs (|z| > 5), the S-curve flattens out into saturation. Gradients become almost zero (Vanishing Gradient problem), causing earlier layers to stop learning. (Use ReLU instead for hidden layers!).\n3. Confusing raw score (z) with probability (σ(z)): Remember z can be any number (-10, +50), while σ(z) is strictly bounded between 0.0 and 1.0.\n4. Separating Sigmoid and BCELoss in PyTorch: Calling torch.sigmoid() followed by nn.BCELoss() can cause numerical underflow and NaN crashes; always use nn.BCEWithLogitsLoss() instead.\n5. Assuming 0.5 is always the best decision cutoff: While σ(0) = 0.5 is standard, imbalanced problems (like fraud occurring only 0.1% of the time) often require lowering the decision threshold to catch rare cases.",
        "core_logic": "Why this matters: Without non-linear activation functions, stacking 100 neural network layers would mathematically collapse into a single ordinary linear regression line. Activation functions give networks the power to bend, curve, and adapt. Sigmoid was the original breakthrough because it bridges linear algebra with probability theory.",
        "architectural_logic": "In PyTorch models, avoid using nn.Sigmoid() on the final layer during training. Instead, output raw logits directly and pair them with nn.BCEWithLogitsLoss(). For production inference, apply torch.sigmoid(logits) only when presenting final probability percentages to end users.",
        "key_takeaways": [
            "Converts Scores to Probabilities: Transforms any raw score from -∞ to +∞ into a clean probability between 0 and 1.",
            "Midpoint at Zero: A raw score of z = 0 produces exactly 0.50 probability (the natural 50/50 balance point).",
            "Foundational for Classification: Powers Logistic Regression and the final output layer of binary neural networks.",
            "Use BCEWithLogitsLoss: Always combine logits and binary cross-entropy in a single stable operation in PyTorch."
        ],
        "definition_bullets": [
            "Activation Function: A mathematical function in a neural network that transforms a neuron's raw input score into its final output.",
            "Sigmoid Function: An S-shaped activation function, σ(z) = 1 / (1 + e^-z), that squashes any real-valued number into the range (0, 1)."
        ],
        "types_header": "4 Key Mathematical Properties of Sigmoid",
        "types_badge": "Curve Characteristics",
        "quick_types": [
            {
                "type": "Property A: Bounded Output Range (0 < σ(z) < 1)",
                "definition": "The output is strictly between 0 and 1; it approaches 0 for negative inputs and 1 for positive inputs, without ever reaching either endpoint.",
                "looks_like": "0.0 < σ(z) < 1.0"
            },
            {
                "type": "Property B: The Midpoint at Zero (σ(0) = 0.5)",
                "definition": "When the raw score is zero, σ(0) = 1 / (1 + 1) = 0.5; this represents maximum uncertainty and serves as the standard decision threshold.",
                "looks_like": "σ(0) = 0.50 (50% probability)"
            },
            {
                "type": "Property C: Monotonicity (Always Increasing)",
                "definition": "As the raw score z increases, the sigmoid probability always increases; higher input evidence never produces a lower output score.",
                "looks_like": "z₁ > z₂ ⟹ σ(z₁) > σ(z₂)"
            },
            {
                "type": "Property D: Smoothness & Differentiability",
                "definition": "The curve is smooth and continuous everywhere with an elegant derivative, σ'(z) = σ(z)(1 - σ(z)), enabling smooth gradient descent updates.",
                "looks_like": "dσ/dz = σ(z)(1 - σ(z))"
            }
        ],
        "connected_logic": [
            {
                "title": "Why Neural Networks Need Activation Functions",
                "content": "• If you connect multiple neuron layers without activation functions, you are simply multiplying linear equations together.\n• Mathematically, a linear combination of linear combinations is still just a single straight line!\n• Activation functions introduce non-linear bends, enabling neural networks to learn complex curves, circles, and multi-dimensional decision boundaries."
            },
            {
                "title": "Sigmoid in Logistic Regression",
                "content": "• Sigmoid is not only for neural networks; it is the mathematical engine of Logistic Regression for binary classification.\n• Standard linear regression (y = wx + b) would predict negative numbers or numbers greater than 1, which make no sense as probabilities.\n• Wrapping that linear line inside Sigmoid (p = σ(wx + b)) guarantees valid, calibrated probability percentages between 0 and 1."
            },
            {
                "title": "The Vanishing Gradient Problem Explained Simply",
                "content": "• Looking at the Sigmoid S-curve: for extreme values (z < -5 or z > 5), the curve becomes virtually flat (saturation).\n• A flat curve means the slope (derivative) is almost zero (σ'(z) ≈ 0).\n• In deep networks, multiplying these tiny slopes backwards through many layers causes the learning gradient to vanish, freezing the early layers (which is why ReLU is preferred for hidden layers)."
            },
            {
                "title": "PyTorch Best Practice: BCEWithLogitsLoss",
                "content": "• During training in PyTorch, it is common to output raw logits (z) directly rather than applying Sigmoid first.\n• Pairing raw logits with nn.BCEWithLogitsLoss uses the log-sum-exp mathematical trick internally.\n• This prevents floating-point underflow and log(0) NaN crashes, making training faster and far more numerically stable."
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
