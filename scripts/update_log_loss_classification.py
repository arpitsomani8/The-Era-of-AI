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

    log_loss_data = {
        "id": "concept_log_loss_classification",
        "title": "Log Loss Penalty in Classification",
        "topic_id": "ml_logistic",
        "topic_label": "Logistic Regression & Sigmoid",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Log Loss (Cross-Entropy penalty for incorrect confidence)",
        "def": "Log Loss (also called Binary Cross-Entropy) is the standard loss penalty used in classification that measures how closely a model's predicted probabilities match the actual true labels, heavily punishing confident wrong guesses.",
        "formula": "$$\\text{Log Loss} = -\\left[ y \\ln(p) + (1 - y) \\ln(1 - p) \\right]$$",
        "logic": "Classification models output probabilities rather than hard decisions. Log Loss measures the quality of these confidence numbers. If the true class is 1, the penalty simplifies to -ln(p); if the true class is 0, it simplifies to -ln(1-p). The closer the predicted probability is to the true class, the lower the loss.",
        "example": "Customer churn prediction: If a customer actually leaves (y = 1) and the model predicts 95% leave probability (p = 0.95), the loss is nearly zero (0.051). But if the model confidently guesses only 5% leave probability (p = 0.05), the loss skyrockets to 2.996—heavily penalizing the model for being confidently wrong.",
        "tags": [
            "Log Loss",
            "Classification Penalty",
            "Binary Cross-Entropy",
            "Confidence Scoring",
            "Loss vs Accuracy",
            "Logistic Regression"
        ],
        "definition": "Log Loss (also called Binary Cross-Entropy) is the standard loss penalty used in classification that measures how closely a model's predicted probabilities match the actual true labels, heavily punishing confident wrong guesses.",
        "formula_explanation": "",
        "simple_summary": "Think of Log Loss as a strict quiz grader who asks for your confidence on every answer. If you answer correctly and say you are 95% confident, you get full credit. If you guess wrong with low confidence, you lose a few points. But if you boast that you are 99% sure and get the question completely wrong, the grader penalizes you massively. It forces the model to be honest about its uncertainty.",
        "core_terms": [
            {
                "term": "What is Log Loss in Classification?",
                "what_is_it": "• The primary mathematical penalty function used to grade classification probabilities.\n• Unlike accuracy which only checks if the final guess was right or wrong, Log Loss evaluates how confident the model was.",
                "analogy": "A betting game: betting a tiny fraction of your money on a risky bet hurts very little, but betting your entire life savings on the wrong horse wipes you out completely.",
                "why_it_matters": "Provides the smooth, convex mathematical loss surface that gradient descent needs to train Logistic Regression and neural networks."
            },
            {
                "term": "The Penalty on Confident Mistakes",
                "what_is_it": "• As the probability assigned to the true outcome approaches zero (p → 0), the penalty -ln(p) shoots up toward infinity.\n• A timid wrong guess (p = 0.49) receives a modest penalty, but an arrogant wrong guess (p = 0.001) receives a devastating loss.",
                "analogy": "A weather forecaster saying: 'There is a 100% chance of sunshine today', right before a catastrophic blizzard hits town.",
                "why_it_matters": "Actively prevents classification models from developing dangerous, unjustified overconfidence in real-world systems."
            },
            {
                "term": "Loss Penalty vs. Regularization Penalty",
                "what_is_it": "• Log Loss is a loss penalty: it measures how far predicted probabilities are from true labels.\n• Regularization (L1/L2) is a complexity penalty: it penalizes large weights to keep the model simple.\n• A real-world training objective adds them together: Total Loss = Log Loss + λ × Regularization.",
                "analogy": "In car driving: a loss penalty is getting a speeding ticket for breaking traffic laws (prediction errors), while regularization is paying routine maintenance costs to keep the engine healthy (preventing complexity).",
                "why_it_matters": "Clarifies the crucial distinction between fitting the training data accurately and preventing the model from becoming overly complex."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "y",
                "meaning": "True Class Label",
                "plain_english": "Strictly 0 or 1, representing the actual ground-truth outcome"
            },
            {
                "symbol": "p",
                "meaning": "Predicted Probability",
                "plain_english": "The model's confidence for Class 1, strictly between 0.0 and 1.0"
            },
            {
                "symbol": "1 - p",
                "meaning": "Negative Class Probability",
                "plain_english": "The model's confidence that the outcome is Class 0"
            },
            {
                "symbol": "ln",
                "meaning": "Natural Logarithm",
                "plain_english": "Log base e; produces large positive penalties when taking the negative log of small decimals"
            },
            {
                "symbol": "-ln(p)",
                "meaning": "True Class Penalty",
                "plain_english": "The exact loss incurred when the actual label is y = 1"
            }
        ],
        "numerical_example": "How Log Loss Scores 3 Predictions for a True Customer Churn (y = 1):\nFormula: Loss = -ln(p)\n\n1. Confident & Correct (p = 0.95):\n• Loss = -ln(0.95) ≈ 0.051 (Tiny loss! Model is heavily rewarded)\n\n2. Uncertain / Coin Flip (p = 0.50):\n• Loss = -ln(0.50) ≈ 0.693 (Moderate loss)\n\n3. Confident & Dead Wrong (p = 0.01 — Model predicted 99% stay!):\n• Loss = -ln(0.01) ≈ 4.605 (Massive 90x bigger penalty than Case 1!)\n\n4. Extreme Blunder (p = 0.0001):\n• Loss = -ln(0.0001) ≈ 9.210 (Penalty climbs exponentially toward infinity!)\n\nTakeaway: Log Loss doesn't just grade whether you guessed right; it punishes arrogant mistakes exponentially harder than honest uncertainty.",
        "pitfalls": "Common Mistakes to Avoid:\n1. Passing hard class labels to log_loss: Passing binary arrays like [0, 1, 1] into scikit-learn's log_loss() instead of probabilities will cause any single mistake to evaluate as log(0) = -infinity! Always pass predicted probabilities from model.predict_proba().\n2. Assuming zero loss is realistic: A log loss of exactly 0.0 requires assigning 100% certainty to every single example; real-world models never achieve zero loss.\n3. Confusing Log Loss with Decision Thresholds: Log Loss evaluates raw probability quality with no threshold required; thresholds only come in later when converting probabilities into binary actions.\n4. Blindly trusting high accuracy: A model can achieve 90% accuracy on imbalanced data by guessing 0 every time, but its Log Loss will expose terrible, uncalibrated probability predictions.\n5. Computing logarithms of exact zero: Because log(0) is mathematically undefined, always ensure probabilities are clipped to [1e-15, 1 - 1e-15] or use BCEWithLogitsLoss in PyTorch.",
        "core_logic": "Why this matters: Accuracy is a step-function that is flat almost everywhere and non-differentiable, making it impossible to optimize with gradient descent. Log Loss provides a smooth, continuous, convex loss surface whose derivative (p - y) gives gradient descent the exact direction and step size needed to tune parameters.",
        "architectural_logic": "In Scikit-Learn, log_loss(y_true, y_pred) automatically clips probabilities to 1e-15 for numerical safety. In PyTorch deep learning pipelines, always use nn.BCEWithLogitsLoss rather than raw Sigmoid + nn.BCELoss to combine the sigmoid operation and binary cross-entropy calculation in a single numerically stable kernel.",
        "key_takeaways": [
            "Grades Confidence: Evaluates probability quality, not just hard right/wrong decisions.",
            "Exponential Blunder Penalty: Punishes confident mistakes with severe asymptotic penalties (-ln(p) → ∞).",
            "Threshold-Free: Evaluates continuous probabilities directly without needing an arbitrary 0.5 cutoff.",
            "Gradient Friendly: Provides the smooth convex mathematical surface required by gradient descent."
        ],
        "definition_bullets": [
            "Log Loss: A convex loss penalty that measures the difference between actual binary labels and predicted probabilities.",
            "Regularization Penalty: An added mathematical cost (L1 or L2) that discourages model complexity and large weights."
        ],
        "types_header": "Comparison: Accuracy vs. Log Loss",
        "types_badge": "Classification Metrics Compared",
        "quick_types": [
            {
                "type": "What It Measures",
                "definition": "Accuracy measures the fraction of correct class decisions (right vs wrong). Log Loss measures the quality and calibration of predicted probability percentages.",
                "looks_like": "Accuracy: count / total | Log Loss: -∑ y ln(p)"
            },
            {
                "type": "Threshold Requirement",
                "definition": "Accuracy strictly requires a decision threshold (like 0.5) to convert probabilities into labels. Log Loss needs NO threshold—it grades probabilities directly.",
                "looks_like": "Accuracy: y_hat = (p >= 0.5) | Log Loss: evaluates raw p"
            },
            {
                "type": "Handling Confident Mistakes",
                "definition": "Accuracy treats a 51% wrong guess and a 99% wrong guess identically (0 points). Log Loss penalizes a 99% wrong guess exponentially harder than a 51% guess.",
                "looks_like": "Accuracy: 0 vs 1 | Log Loss: 0.72 vs 4.61 penalty"
            },
            {
                "type": "Best Value & Primary Use",
                "definition": "Accuracy: higher is better (1.0 = best); used for final executive reporting. Log Loss: lower is better (0.0 = best); used for training models via gradient descent.",
                "looks_like": "Accuracy: % correct | Log Loss: gradient-friendly loss"
            }
        ],
        "connected_logic": [
            {
                "title": "Why Mean Squared Error (MSE) Fails for Classification",
                "content": "• If you train Logistic Regression using MSE, squaring Sigmoid probabilities creates a bumpy, non-convex landscape with flat local plateaus.\n• Furthermore, on huge blunders, Sigmoid's derivative flattens to zero, causing vanishing gradients that freeze training.\n• Log Loss cancels Sigmoid's plateau into a clean linear gradient (p - y), guaranteeing a strictly convex bowl with fast learning!"
            },
            {
                "title": "Extension to Multiclass Classification (Softmax)",
                "content": "• For binary problems, Log Loss balances two outcomes: p and 1 - p.\n• For multiclass problems (e.g. cat vs dog vs bird), Softmax converts raw scores into probabilities across all classes that sum to 1.0.\n• Multiclass Log Loss (Categorical Cross-Entropy) simply penalizes the negative log of the correct class: -ln(p_true), ignoring the rest."
            },
            {
                "title": "Probability Clipping in Scikit-Learn",
                "content": "• In Scikit-Learn, log_loss(y_true, y_pred) automatically clips probabilities to [ε, 1 - ε] where ε = 10⁻¹⁵.\n• This safety rail ensures that even if a model outputs p = 0.0 on a true positive, the loss is capped at ≈ 34.5 rather than crashing with an infinite error."
            },
            {
                "title": "Combining Log Loss with L1/L2 Regularization",
                "content": "• In standard Logistic Regression (e.g. sklearn.linear_model.LogisticRegression), the objective function combines Log Loss with an L2 penalty: min_w LogLoss(w) + (1 / (2C)) ||w||₂².\n• Log Loss pulls the weights to fit the probabilities, while the L2 penalty pulls weights toward zero to prevent overfitting."
            }
        ]
    }

    # 1. Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_log_loss_classification":
            c.update(log_loss_data)
            print("Updated concept_log_loss_classification in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # 2. Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_log_loss_classification":
            c.update(log_loss_data)
            print("Updated concept_log_loss_classification in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # 3. Update in concepts_ml.py
    pattern = r'\{\s*"id":\s*"concept_log_loss_classification".*?\},(?=\s*\{\s*"id":\s*"concept_logits_log_odds")'
    match = re.search(pattern, py_content, re.DOTALL)
    if match:
        lines = json.dumps(log_loss_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        py_content = py_content[:match.start()] + indented_replacement + py_content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(py_content)
        print("Updated concept_log_loss_classification in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
