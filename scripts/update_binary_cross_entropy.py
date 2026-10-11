import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    bce_data = {
        "id": "concept_binary_cross_entropy",
        "title": "Log Loss & Binary Cross-Entropy",
        "topic_id": "ml_loss",
        "topic_label": "Loss Functions (L1, L2, MSE, MAE, Log Loss)",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Log Loss / Binary Cross-Entropy (For probabilistic classification)",
        "def": "Log Loss (Binary Cross-Entropy) measures how well a model predicts probabilities for yes-or-no outcomes, heavily penalizing confident wrong guesses.",
        "formula": "$$L = -[y \\ln(p) + (1 - y) \\ln(1 - p)]$$",
        "logic": "If the true answer is 1, the formula simplifies to -ln(p). If the true answer is 0, it simplifies to -ln(1-p). When the model is confidently right, the loss is close to zero; but if the model is confidently wrong, the loss skyrockets toward infinity.",
        "example": "Spam detection: If an email is spam (y=1) and the model predicts 99% spam probability, loss is tiny (0.01). But if the model confidently guesses only 1% spam probability, loss explodes to 4.61, heavily punishing the blunder.",
        "tags": [
            "Log Loss",
            "Binary Cross-Entropy",
            "BCE",
            "Logistic Regression",
            "Probabilities",
            "Maximum Likelihood Estimation"
        ],
        "definition": "Log Loss (Binary Cross-Entropy) measures how well a model predicts probabilities for yes-or-no outcomes, heavily penalizing confident wrong guesses.",
        "formula_explanation": "",
        "simple_summary": "Log Loss (Binary Cross-Entropy) is the gold-standard loss function for binary classification (like spam vs legitimate, disease vs healthy). Instead of just checking if the model guessed 0 or 1, it grades the predicted confidence percentage. Correct, confident guesses give almost 0 loss; uncertain guesses give a moderate loss; but confident wrong guesses receive an asymptotically infinite penalty.",
        "core_terms": [
            {
                "term": "Binary Cross-Entropy (BCE)",
                "what_is_it": "• The primary loss function for two-class problems that scores predicted probabilities between 0.0 and 1.0.\n• Formula: L = -[y ln(p) + (1 - y) ln(1 - p)]; mathematically identical to Negative Log-Likelihood (NLL) and Log Loss.",
                "analogy": "A multiple-choice quiz where wagering money on your answers: betting 99% of your cash on the wrong choice wipes out your bank account.",
                "why_it_matters": "Powers logistic regression and binary neural networks; creates a strictly convex bowl with a guaranteed global minimum when paired with Sigmoid."
            },
            {
                "term": "Asymptotic Penalty on Overconfidence",
                "what_is_it": "• Log Loss has a minimum of 0, but no finite upper limit. As predicted probability p approaches 0 for a true positive (y = 1), loss approaches infinity.\n• Unlike MSE which caps error at 1.0, Log Loss punishes confident mistakes exponentially harder than small errors.",
                "analogy": "A doctor saying: 'I am 100% sure this patient is completely fine', when the patient actually has a medical emergency.",
                "why_it_matters": "Forces classification models to output honest, well-calibrated probabilities instead of making reckless, overconfident guesses."
            },
            {
                "term": "BCEWithLogitsLoss & Probability Clipping",
                "what_is_it": "• Taking log(0) is undefined and causes software crashes (NaN).\n• Libraries like Scikit-Learn clip probabilities to [1e-15, 1 - 1e-15], while PyTorch's torch.nn.BCEWithLogitsLoss computes the Sigmoid and Log Loss together safely using the log-sum-exp trick.",
                "analogy": "A safety valve on a pressure cooker that automatically vents steam before the dial hits the danger zone.",
                "why_it_matters": "Crucial deep learning best practice: always use BCEWithLogitsLoss with raw model outputs (logits) to guarantee numerical stability."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "L",
                "meaning": "Loss per Example",
                "plain_english": "The penalty score computed for a single prediction"
            },
            {
                "symbol": "y",
                "meaning": "Actual Binary Label",
                "plain_english": "The true ground truth, strictly either 0 or 1"
            },
            {
                "symbol": "p (or p̂)",
                "meaning": "Predicted Probability",
                "plain_english": "The model's predicted confidence that y=1, strictly between 0.0 and 1.0"
            },
            {
                "symbol": "log (or ln)",
                "meaning": "Natural Logarithm",
                "plain_english": "Log base e; outputs large positive penalties when taking the negative log of small probabilities"
            },
            {
                "symbol": "(1/N) ∑ L_i",
                "meaning": "Mean Log Loss",
                "plain_english": "The average loss calculated across all N examples in the dataset"
            },
            {
                "symbol": "p̂ - y",
                "meaning": "Linear Error Gradient",
                "plain_english": "The clean derivative produced when Sigmoid is paired with BCE, preventing vanishing gradients"
            }
        ],
        "numerical_example": "How Log Loss Scores 3 Predictions:\nFormula: L = -[y ln(p) + (1 - y) ln(1 - p)]\n\nCase A: Actual Label is y = 1 (formula simplifies to L = -ln(p))\n• Confident & Correct: Model predicts p = 0.99 ➔ L = -ln(0.99) = 0.010 (Near zero loss!)\n• Uncertain / Coin Flip: Model predicts p = 0.50 ➔ L = -ln(0.50) = 0.693 (Moderate loss)\n• Confident & Dead Wrong: Model predicts p = 0.01 ➔ L = -ln(0.01) = 4.605 (Huge 460x penalty!)\n\nCase B: Actual Label is y = 0 (formula simplifies to L = -ln(1 - p))\n• Model predicts p = 0.05 ➔ L = -ln(1 - 0.05) = -ln(0.95) = 0.051 (Great prediction)\n• Model predicts p = 0.95 ➔ L = -ln(1 - 0.95) = -ln(0.05) = 2.996 (Heavy penalty)\n\nTakeaway: The loss penalizes the probability assigned to the wrong outcome without upper limit.",
        "pitfalls": "Common Mistakes to Avoid:\n1. Using hard class labels instead of probabilities: Log Loss requires predicted probabilities (like 0.85), not just 0 or 1. Passing hard labels into log_loss() can result in log(0) and infinite error crashes.\n2. Confusing probability (p) with the actual label (y): Remember p is the model's confidence for class 1; y is the true known outcome.\n3. Thinking lower loss is always enough: On imbalanced datasets, a model predicting 0 for everything might show a low average loss while failing completely on rare positive cases. Always check Precision, Recall, and ROC-AUC.\n4. Mixing up loss and regularization: BCE measures prediction quality on the data; regularization (L1/L2) is an added penalty that discourages overly complex weights.\n5. Using MSE with Sigmoid for classification: Pairing MSE with Sigmoid creates a non-convex surface and causes vanishing gradients (σ' → 0) on big blunders, freezing training. Log Loss cancels this plateau into a fast-learning linear gradient (p̂ - y).",
        "core_logic": "Why this matters: When Sigmoid σ(z) is combined with Log Loss, the complex calculus simplifies into an elegant gradient: dL/dz = p̂ - y. This means the gradient step is directly proportional to how far off the predicted probability was! If the model makes a massive blunder, the gradient is massive (p̂ - y → 1.0), triggering rapid weight correction. Once the prediction is accurate, the gradient smoothly glides to zero.",
        "architectural_logic": "In PyTorch, torch.nn.BCEWithLogitsLoss combines Sigmoid and BCE into a single layer using the log-sum-exp trick: L = max(z, 0) - z*y + log(1 + exp(-|z|)). This mathematically prevents floating-point overflow from computing exp(z) on large logits and avoids taking log(0).",
        "key_takeaways": [
            "Grades Probabilities: Evaluates confidence percentages (p ∈ [0, 1]), not just final hard categories.",
            "Asymptotically Punishes Blunders: Confident wrong guesses receive penalties approaching infinity (-ln(p) → ∞).",
            "Eliminates Vanishing Gradients: Pairing BCE with Sigmoid yields a clean linear gradient (p̂ - y) for fast learning.",
            "Use BCEWithLogitsLoss: Always use numerically stable combined logits in PyTorch to avoid log(0) NaN crashes."
        ],
        "definition_bullets": [
            "Log Loss (Binary Cross-Entropy): The standard convex loss function for binary classification that scores predicted probabilities against actual binary labels.",
            "Logits: Unbounded raw score outputs (-∞ to +∞) produced by a model before applying the Sigmoid activation function."
        ],
        "types_header": "Comparison: MSE vs. Log Loss (Binary Cross-Entropy)",
        "types_badge": "Regression vs Classification Loss",
        "quick_types": [
            {
                "type": "Log Loss / BCE (Classification)",
                "definition": "Primary Task: Binary classification (probabilities). Output Range: strictly bounded [0.0, 1.0]. Landscape: strictly convex when paired with Sigmoid (guaranteed global minimum!).",
                "looks_like": "torch.nn.BCEWithLogitsLoss()"
            },
            {
                "type": "Mean Squared Error (Regression)",
                "definition": "Primary Task: Regression (continuous numbers). Output Range: (-∞, +∞). Landscape: non-convex when paired with Sigmoid; causes vanishing gradients on big errors.",
                "looks_like": "torch.nn.MSELoss()"
            },
            {
                "type": "Negative Log-Likelihood (NLL)",
                "definition": "The statistical derivation of Log Loss originating directly from Maximum Likelihood Estimation (MLE) of the Bernoulli distribution.",
                "looks_like": "NLL ≡ Log Loss ≡ BCE"
            },
            {
                "type": "Categorical Cross-Entropy",
                "definition": "The multi-class extension of Binary Cross-Entropy paired with Softmax for predicting across 3 or more mutually exclusive classes.",
                "looks_like": "torch.nn.CrossEntropyLoss()"
            }
        ],
        "connected_logic": [
            {
                "title": "Comparison: MSE vs. Log Loss (Binary Cross-Entropy)",
                "content": "• Primary Task: MSE is for continuous regression; Log Loss is for binary classification probabilities.\n• Output Range: MSE outputs (-∞, +∞); Log Loss operates strictly on bounded probabilities [0.0, 1.0].\n• Gradient on Big Error: MSE paired with Sigmoid vanishes (σ' → 0) on big mistakes; Log Loss yields a massive linear gradient (p̂ - y → 1.0), ensuring fast learning!\n• Punishment for Blunders: MSE punishes quadratically (e²); Log Loss punishes asymptotically toward infinity (-ln(p) → ∞)."
            },
            {
                "title": "From Maximum Likelihood Estimation (MLE) to BCE",
                "content": "• For a binary event with probability p, the Bernoulli likelihood is P(y|p) = p^y · (1 - p)^(1 - y).\n• Taking the negative natural log gives: -ln P(y|p) = -[y ln(p) + (1 - y) ln(1 - p)].\n• Therefore: Negative Log-Likelihood (NLL) ≡ Log Loss ≡ Binary Cross-Entropy!"
            },
            {
                "title": "Numerical Stability & Probability Clipping",
                "content": "• Because log(0) is mathematically undefined and returns negative infinity, ML packages automatically clip probabilities.\n• Scikit-Learn clips p to [1e-15, 1 - 1e-15], capping maximum single-sample loss at ≈ 34.5.\n• In PyTorch, BCEWithLogitsLoss calculates loss directly from logits without ever computing an intermediate raw probability."
            },
            {
                "title": "Binary Cross-Entropy vs Multi-Class Cross-Entropy",
                "content": "• BCE handles binary (two-class) problems or multi-label problems where each tag is an independent binary decision.\n• For single-choice multi-class problems (e.g. cat vs dog vs bird), Categorical Cross-Entropy pairs with Softmax instead of Sigmoid."
            }
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_binary_cross_entropy":
            c.update(bce_data)
            print("Updated concept_binary_cross_entropy in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_binary_cross_entropy":
            c.update(bce_data)
            print("Updated concept_binary_cross_entropy in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_binary_cross_entropy".*?\},(?=\s*\{\s*"id":\s*"concept_learning_rate")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(bce_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_binary_cross_entropy in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
