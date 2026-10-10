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

    softmax_data = {
        "id": "concept_multiclass_softmax",
        "title": "Multiclass Softmax",
        "topic_id": "ml_logistic",
        "topic_label": "Logistic Regression & Sigmoid",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Multiclass Softmax (Normalizing scores into probability distribution)",
        "def": "The Softmax function is an activation function for multiclass classification that converts a list of raw scores (logits) into a probability distribution where every probability is between 0 and 1, and all probabilities sum to exactly 1.0.",
        "formula": "$$P(y = i) = \\frac{e^{z_i}}{\\sum_{j=1}^K e^{z_j}}, \\quad \\sum_{i=1}^K P(y = i) = 1.0$$",
        "logic": "When a neural net classifies among 3 or more mutually exclusive classes (like Cat vs Dog vs Bird), its final layer outputs raw scores like [2.0, 1.0, 0.1]. Softmax exponentiates each score (e^z) to make them all positive, and then divides each by the sum of all exponentials so they form valid percentage probabilities that add up to 100%.",
        "example": "Animal image classifier: Raw logit scores for [Cat, Dog, Bird] are [2.0, 1.0, 0.1]. Exponentiating gives [7.39, 2.72, 1.11] with a total sum of 11.22. Dividing each by 11.22 yields [65.9% Cat, 24.2% Dog, 9.9% Bird]. The model predicts Cat with 65.9% confidence.",
        "tags": [
            "Softmax",
            "Multiclass",
            "Classification",
            "Logits",
            "Cross-Entropy",
            "Neural Networks"
        ],
        "definition": "The Softmax function is an activation function for multiclass classification that converts a list of raw scores (logits) into a probability distribution where every probability is between 0 and 1, and all probabilities sum to exactly 1.0.",
        "formula_explanation": "",
        "simple_summary": "Imagine cutting a whole pizza into slices. Raw model scores are like customer hunger levels: some are super hungry, some are a little hungry. Softmax takes everyone's hunger scores and divides up the pizza into percentage slices. The hungriest person gets the biggest slice, and all the slices added together always make up exactly 100% of the pizza.",
        "core_terms": [
            {
                "term": "What is the Softmax Function?",
                "what_is_it": "• The multiclass generalization of the Sigmoid function for single-choice classification across K classes.\n• Takes K arbitrary numbers from -∞ to +∞ and maps them onto a valid probability distribution where ∑ P(y=i) = 1.0.",
                "analogy": "Slicing up a pie: every candidate class gets a slice based on its score, and all slices combined always equal the whole 100% pie.",
                "why_it_matters": "The universal output layer for multiclass neural networks, computer vision classifiers (ImageNet), and language models (next-token prediction)."
            },
            {
                "term": "Why Exponentiation (e^z) Matters",
                "what_is_it": "• Exponentiating e^z guarantees all values are strictly positive, even if raw input scores are negative numbers (e.g. z = -3 ⟹ e^-3 ≈ 0.05).\n• It also magnifies differences: a score of 4 becomes 54.6, heavily rewarding the leading candidate over runner-ups.",
                "analogy": "A megaphone: it turns quiet whispers into audible sound and makes the loudest speaker clearly dominate the room.",
                "why_it_matters": "Prevents negative probabilities and creates a sharp, decisive output distribution."
            },
            {
                "term": "Coupled vs. Independent Probabilities",
                "what_is_it": "• In Softmax, all class probabilities are mathematically coupled through the shared denominator.\n• If one class's score rises, its probability grows, which automatically forces the probabilities of all other classes to drop!",
                "analogy": "A family monthly budget: spending more money on a new laptop automatically leaves less money for dining out and vacations.",
                "why_it_matters": "Explains why Softmax is strictly for mutually exclusive single-choice problems, not multi-label tagging."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "K",
                "meaning": "Number of Classes",
                "plain_english": "The total count of categories (e.g. 3 for Cat/Dog/Bird, 10 for MNIST digits)"
            },
            {
                "symbol": "z_i",
                "meaning": "Raw Logit for Class i",
                "plain_english": "The unconstrained score produced by the linear layer for category i"
            },
            {
                "symbol": "e",
                "meaning": "Euler's Constant",
                "plain_english": "A mathematical constant approximately equal to 2.71828"
            },
            {
                "symbol": "e^z_i",
                "meaning": "Exponentiated Score",
                "plain_english": "Makes the score strictly positive and amplifies the winning candidate"
            },
            {
                "symbol": "∑ e^z_j",
                "meaning": "Denominator Normalizer",
                "plain_english": "The sum of all exponentials across all K classes ensuring probabilities add up to 1.0"
            },
            {
                "symbol": "P(y = i)",
                "meaning": "Predicted Probability",
                "plain_english": "The final normalized probability assigned to class i"
            }
        ],
        "numerical_example": "Step-by-Step Calculation for a 3-Class Animal Classifier [Cat, Dog, Bird]:\nRaw Logits: z = [2.0 (Cat), 1.0 (Dog), 0.1 (Bird)]\n\nStep 1: Calculate Exponentials (e^z)\n• e^2.0 ≈ 7.389 (Cat)\n• e^1.0 ≈ 2.718 (Dog)\n• e^0.1 ≈ 1.105 (Bird)\n\nStep 2: Sum the Exponentials (The Denominator)\n• Sum = 7.389 + 2.718 + 1.105 = 11.212\n\nStep 3: Divide Each by the Sum to Get Probabilities\n• P(Cat)  = 7.389 / 11.212 ≈ 0.659 (65.9%)\n• P(Dog)  = 2.718 / 11.212 ≈ 0.242 (24.2%)\n• P(Bird) = 1.105 / 11.212 ≈ 0.099 (9.9%)\n\nVerification: 0.659 + 0.242 + 0.099 = 1.000 (Exactly 100%!)",
        "pitfalls": "Common Mistakes to Avoid:\n1. Applying Softmax before PyTorch's CrossEntropyLoss: nn.CrossEntropyLoss already includes LogSoftmax internally. Applying Softmax first causes double-normalization and degrades training stability.\n2. Using Softmax for multi-label classification: If an image can contain BOTH a dog and a cat, Softmax forces them to compete and divide up 100%. Use independent Sigmoid outputs for each tag instead!\n3. Confusing logits with probabilities: Raw logits like z = [5.0, -2.0] are unconstrained scores, not probabilities.\n4. Floating-point numerical overflow: Calculating e^1000 causes an inf / NaN crash. Always subtract the maximum logit (z_i - max(z)) before exponentiating.\n5. Assuming high probability guarantees correctness: Softmax can output 99% confidence on random out-of-distribution noise because exponentiation aggressively exaggerates the largest score.",
        "core_logic": "Why this matters: Single-choice classification requires a probability distribution that satisfies the Kolmogorov axioms: all probabilities must be non-negative and sum to 1. Softmax satisfies this requirement smoothly and differentiably, creating a seamless gradient pathway back to model weights when paired with Categorical Cross-Entropy.",
        "architectural_logic": "In PyTorch neural networks, the final layer should be a raw linear projection (nn.Linear(hidden_dim, num_classes)) with NO activation attached. Pass these raw logits directly into nn.CrossEntropyLoss() during training. At inference time, call torch.softmax(logits, dim=-1) only when probabilities are required.",
        "key_takeaways": [
            "Converts Scores to Probabilities: Normalizes K unconstrained logits into a probability distribution summing to 1.0.",
            "Mutually Exclusive Classes: Best for single-choice classification where only one class can be true at a time.",
            "Softmax vs Sigmoid: Use Softmax for 1-of-K exclusive choices; use independent Sigmoids for multi-label tags.",
            "Direct Logits in PyTorch: Pass raw logits directly to nn.CrossEntropyLoss without applying Softmax first."
        ],
        "definition_bullets": [
            "Softmax Function: A normalized exponential function converting a vector of K real numbers into a probability distribution summing to 1.",
            "Categorical Cross-Entropy: The standard loss function paired with Softmax that penalizes the negative log probability of the true class."
        ],
        "types_header": "Softmax vs. Sigmoid (Key Interview Comparison)",
        "types_badge": "Activation Selection Guide",
        "quick_types": [
            {
                "type": "Typical Use Case",
                "definition": "Softmax: Mutually exclusive multiclass classification (single choice: Cat vs Dog vs Horse). Sigmoid: Binary classification or multi-label tagging (where labels can coexist).",
                "looks_like": "Softmax: 1-of-K classes | Sigmoid: Independent yes/no"
            },
            {
                "type": "Input & Output Dimensions",
                "definition": "Softmax takes K logits and outputs K coupled probabilities. Sigmoid takes 1 logit per binary decision and outputs 1 independent probability.",
                "looks_like": "Softmax: K inputs → K outputs | Sigmoid: 1 input → 1 output"
            },
            {
                "type": "Sum Across Outputs",
                "definition": "Softmax outputs ALWAYS sum to exactly 1.0 (coupled). Sigmoid outputs do NOT sum to 1.0 (each is independent, e.g. 0.8 and 0.9 can both occur).",
                "looks_like": "Softmax: ∑ P = 1.0 | Sigmoid: each P ∈ [0, 1]"
            },
            {
                "type": "Loss Function Pairing",
                "definition": "Softmax pairs with Categorical Cross-Entropy. Sigmoid pairs with Binary Cross-Entropy (BCE).",
                "looks_like": "Softmax + CrossEntropyLoss | Sigmoid + BCEWithLogitsLoss"
            }
        ],
        "connected_logic": [
            {
                "title": "Softmax with Categorical Cross-Entropy Loss",
                "content": "• Softmax produces the probabilities; Categorical Cross-Entropy measures how well those probabilities match reality.\n• If the true class is c, its one-hot label has a 1 at index c and 0 everywhere else.\n• The loss formula simplifies to -ln(P(y = c)): it ignores all other classes and solely penalizes the negative log of the correct answer!"
            },
            {
                "title": "The Numerical Stability Trick (Log-Sum-Exp)",
                "content": "• If a model outputs large logits like z = 1000, computing e^1000 causes a floating-point overflow crash (Inf / NaN).\n• The mathematical solution: subtract the maximum logit from all scores before exponentiating: Softmax(z) = Softmax(z - max(z)).\n• Because subtracting a constant cancels out in the numerator and denominator, the output probabilities remain mathematically identical while preventing GPU crashes."
            },
            {
                "title": "Temperature Scaling in Large Language Models (LLMs)",
                "content": "• In LLMs (like GPT-4), Softmax converts token logits into word probabilities: P(token_i) = e^(z_i / T) / ∑ e^(z_j / T).\n• Temperature T < 1.0 (Cold): Sharpens the distribution, making the model deterministic and confident.\n• Temperature T > 1.0 (Hot): Flattens the distribution, giving unlikely words higher chances, producing creative and diverse text."
            },
            {
                "title": "Multi-Label vs. Multi-Class: The Golden Rule",
                "content": "• Single-label Multi-Class: Each sample belongs to exactly one category (e.g. MNIST digit is 0, 1, 2... 9). Use Softmax.\n• Multi-Label: Each sample can belong to multiple categories simultaneously (e.g. a YouTube video can be 'Gaming', 'Music', and 'Comedy'). Use Sigmoid on each output neuron with BCE loss."
            }
        ]
    }

    # 1. Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_multiclass_softmax":
            c.update(softmax_data)
            print("Updated concept_multiclass_softmax in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # 2. Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_multiclass_softmax":
            c.update(softmax_data)
            print("Updated concept_multiclass_softmax in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # 3. Update in concepts_ml.py
    pattern = r'\{\s*"id":\s*"concept_multiclass_softmax".*?\},(?=\s*\{\s*"id":\s*"concept_l2_ridge")'
    match = re.search(pattern, py_content, re.DOTALL)
    if match:
        lines = json.dumps(softmax_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        py_content = py_content[:match.start()] + indented_replacement + py_content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(py_content)
        print("Updated concept_multiclass_softmax in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
