import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    squared_loss_data = {
        "id": "concept_squared_loss",
        "title": "Squared Loss & L2 Loss",
        "topic_id": "ml_loss",
        "topic_label": "Loss Functions (L1, L2, MSE, MAE, Log Loss)",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Squared Loss / L2 Loss (Penalizes big mistakes harshly)",
        "def": "Squared loss (or L2 loss) calculates the error of a prediction by subtracting the model's guess from the true answer and squaring the result.",
        "formula": "$$L = (y - \\hat{y})^2 = \\|\\mathbf{y} - \\hat{\\mathbf{y}}\\|_2^2$$",
        "logic": "Squaring the error does two important things: it makes all errors positive (so positive and negative errors don't cancel out), and it penalizes large mistakes much more harshly than small mistakes.",
        "example": "House price prediction: If a house sells for $300k and the model predicts $290k, the error is 10k and squared loss is 100M. If the model predicts $250k, the error is 50k and squared loss explodes to 2,500M (25 times bigger penalty for a 5 times bigger mistake).",
        "tags": [
            "Squared Loss",
            "L2 Loss",
            "Loss Functions",
            "Residuals",
            "Regression"
        ],
        "definition": "Squared loss (or L2 loss) calculates the error of a prediction by subtracting the model's guess from the true answer and squaring the result.",
        "formula_explanation": "",
        "simple_summary": "Squared loss is the most common loss function in regression: L = (y - ŷ)². Because errors are squared, small errors get small penalties, but big mistakes get huge penalties. It has a smooth mathematical curve that makes it easy for gradient descent to calculate slopes and optimize weights. However, this also means extreme outliers can pull the model off course.",
        "core_terms": [
            {
                "term": "Squared Loss (L2 Loss)",
                "what_is_it": "• A loss function that measures prediction error by taking the difference between actual value and prediction, and squaring it.\n• Written as L = (y - ŷ)² for a single sample, or the squared L2 norm ||y - ŷ||₂² for a vector.",
                "analogy": "A strict teacher who forgives a 1-minute late assignment with a minor warning, but gives a zero on the test if you are 10 minutes late.",
                "why_it_matters": "The mathematical foundation of linear regression, ordinary least squares (OLS), and mean squared error."
            },
            {
                "term": "L2 Loss vs L2 Regularization",
                "what_is_it": "• A classic technical interview distinction that confuses many engineers.\n• L2 Loss measures prediction mistakes on data: (y - ŷ)². L2 Regularization penalizes large model weights to prevent overfitting: λ · w².",
                "analogy": "L2 Loss is grading how well you answered the test questions; L2 Regularization is penalizing you for writing an overly long, messy essay.",
                "why_it_matters": "L2 Loss fits the model to data, while L2 Regularization stops the model from memorizing noise."
            },
            {
                "term": "Smooth Differentiability",
                "what_is_it": "• The mathematical property where the loss function has a smooth, curved shape with no sharp corners.\n• Its derivative is simple: dLoss/dŷ = 2(ŷ - y), allowing optimizers to calculate exact gradients anywhere.",
                "analogy": "A smooth skateboard bowl where you can glide gently down to the bottom, rather than stairs with sharp edges.",
                "why_it_matters": "Makes gradient descent stable and fast, and allows linear regression to be solved in one step using the Normal Equation."
            }
        ],
        "types_header": "Comparison: L2 Loss vs L2 Regularization",
        "types_badge": "Core Distinctions",
        "quick_types": [
            {
                "type": "L2 Loss (Squared Error)",
                "definition": "Measures error between predictions and true labels; minimizes prediction mistakes.",
                "looks_like": "Loss = (y - y_hat)**2"
            },
            {
                "type": "L2 Regularization (Ridge Penalty)",
                "definition": "Penalizes large model weights; prevents overfitting by keeping coefficients small.",
                "looks_like": "Penalty = lambda * sum(w**2)"
            },
            {
                "type": "Ordinary Least Squares (OLS)",
                "definition": "Minimizes the sum of squared losses across all training examples simultaneously.",
                "looks_like": "model = LinearRegression()"
            },
            {
                "type": "Ridge Regression (Combined)",
                "definition": "Combines L2 prediction loss with L2 weight regularization in one objective.",
                "looks_like": "Objective = L2_Loss + lambda * L2_Penalty"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "y",
                "meaning": "True Label",
                "plain_english": "The actual correct value you want to predict"
            },
            {
                "symbol": "ŷ (y-hat)",
                "meaning": "Predicted Value",
                "plain_english": "The guess produced by the machine learning model"
            },
            {
                "symbol": "y - ŷ",
                "meaning": "Residual (Error)",
                "plain_english": "How far off the prediction was from the true value"
            },
            {
                "symbol": "|| · ||_2",
                "meaning": "L2 Norm",
                "plain_english": "The straight-line Euclidean distance measuring vector length"
            }
        ],
        "numerical_example": "How Squaring Penalizes Mistakes Harshly:\nSuppose we compare three different prediction errors:\n\nCase A: Small Error (Off by 2 units)\n• Error: y - ŷ = 2\n• Squared Loss: 2² = 4\n\nCase B: Medium Error (Off by 5 units)\n• Error: y - ŷ = 5\n• Squared Loss: 5² = 25 (Error grew by 2.5x, but penalty grew by 6.25x!)\n\nCase C: Large Outlier Error (Off by 20 units)\n• Error: y - ŷ = 20\n• Squared Loss: 20² = 400 (Error grew by 10x, but penalty exploded by 100x!)\n\nTakeaway: The model will work 100 times harder to fix the 20-unit error than the 2-unit error, which is why outliers have such a massive pull on squared loss.",
        "pitfalls": "Common Pitfall: Vulnerability to outliers. Because squared loss squares errors, a single corrupt data point (like a typo entering $10,000,000 instead of $100,000) generates a colossal penalty. The optimizer will bend the entire line toward that single outlier to reduce its huge squared error, ruining predictions for all normal points. If your dataset contains heavy outliers, consider using MAE (L1 loss) or Huber loss instead.",
        "core_logic": "Why this matters: Loss functions are the compass that guides model training. By defining how wrong a prediction is, the loss function tells gradient descent which direction to update the model's weights. Squared loss is the default choice for regression because its smooth mathematical derivative guarantees an easy path to the lowest point.",
        "architectural_logic": "In PyTorch and TensorFlow, squared loss is implemented as nn.MSELoss(reduction='none') for per-sample losses, or nn.MSELoss(reduction='mean') across batches. Because its gradient is linear with respect to error (dLoss/de = 2e), gradient steps automatically scale in proportion to how far off the prediction is.",
        "connected_logic": [
            {
                "title": "Why Squaring is Better Than Absolute Value for Math",
                "content": "• Squaring gives a smooth, continuous derivative at every single point.\n• Absolute error (|y - ŷ|) has a sharp corner at 0 where the derivative doesn't exist, making it slightly trickier to optimize."
            },
            {
                "title": "L2 Loss vs L2 Regularization in Ridge Regression",
                "content": "• Ridge regression combines both concepts: Total Loss = L2_Loss + λ · L2_Penalty.\n• L2 Loss forces the line to fit your training data; the L2 Penalty pulls weights closer to zero so the line doesn't wiggle crazily."
            },
            {
                "title": "The Gaussian Noise Connection",
                "content": "• Mathematically, minimizing squared loss is identical to finding the maximum likelihood estimate when data noise follows a normal (bell-curve) distribution.\n• If your measurement errors are naturally normally distributed, squared loss is theoretically the optimal choice."
            },
            {
                "title": "When to Switch from L2 to L1 or Huber Loss",
                "content": "• If your data has zero outliers, squared L2 loss converges quickly and reliably.\n• If your data has extreme spikes or financial anomalies, switch to Huber loss, which acts like L2 for small errors and L1 for large errors."
            }
        ],
        "key_takeaways": [
            "Squared Formula: L = (y - ŷ)²; squares the difference between truth and prediction.",
            "Harsh on Big Errors: Large mistakes receive exponentially bigger penalties than small ones.",
            "Sensitive to Outliers: A few extreme data points can skew the entire model.",
            "L2 Loss vs Regularization: L2 loss measures prediction errors; L2 regularization penalizes large weights."
        ],
        "definition_bullets": [
            "Squared Loss: A regression loss function that squares the prediction error to penalize larger mistakes more heavily.",
            "L2 Regularization: A complexity penalty added to the loss function that shrinks model weights toward zero."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_squared_loss":
            c.update(squared_loss_data)
            print("Updated concept_squared_loss in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_squared_loss":
            c.update(squared_loss_data)
            print("Updated concept_squared_loss in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_squared_loss".*?\},(?=\s*\{\s*"id":\s*"concept_mse")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(squared_loss_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_squared_loss in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
