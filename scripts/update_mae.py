import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    mae_data = {
        "id": "concept_mae",
        "title": "Mean Absolute Error (MAE & L1 Loss)",
        "topic_id": "ml_loss",
        "topic_label": "Loss Functions (L1, L2, MSE, MAE, Log Loss)",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Mean Absolute Error (MAE / L1 loss, outlier resistant)",
        "def": "Mean Absolute Error (MAE) measures the average size of prediction errors by stripping away the negative signs, adding up the differences, and dividing by the number of examples.",
        "formula": "$$\\text{MAE} = \\frac{1}{n} \\sum_{i=1}^n |y_i - \\hat{y}_i|$$",
        "logic": "Unlike squared loss which blows up large mistakes into huge numbers, MAE treats all errors equally and linearly. A mistake of 10 is penalized exactly twice as much as a mistake of 5, making it much more resistant to outliers.",
        "example": "Predicting daily electricity usage: If the true usage is 50 kWh and your model predicts 42 kWh, the absolute error is |50 - 42| = 8 kWh. If MAE across the month is 5 kWh, it means your model is off by an average of 5 kWh per day.",
        "tags": [
            "MAE",
            "L1 Loss",
            "Outlier Resistant",
            "Regression Metric",
            "Lasso"
        ],
        "definition": "Mean Absolute Error (MAE) measures the average size of prediction errors by stripping away the negative signs, adding up the differences, and dividing by the number of examples.",
        "formula_explanation": "",
        "simple_summary": "MAE is the most intuitive error metric in machine learning: calculate how far off each prediction was, turn negative errors positive, and find the average. It is measured in the exact same units as your data (like dollars or kilograms). Because it doesn't square errors, rare extreme spikes won't distort your model the way they do with MSE.",
        "core_terms": [
            {
                "term": "Mean Absolute Error (MAE)",
                "what_is_it": "• The average size of mistakes across a dataset, ignoring whether each guess was too high or too low.\n• Formula: take absolute values of all errors |y - ŷ|, add them together, and divide by n.",
                "analogy": "A golf coach telling you: 'On average, your shots landed 10 feet away from the pin', without caring if you were 10 feet left or 10 feet right.",
                "why_it_matters": "Easy to explain to non-technical business stakeholders because it stays in the exact same units as the real target."
            },
            {
                "term": "Outlier Resistance (Robust Loss)",
                "what_is_it": "• MAE grows linearly (1x, 2x, 3x) instead of quadratically (1x, 4x, 9x).\n• If an outlier is off by 90 units, MAE adds 90 to the total error, while MSE adds a massive 8,100.",
                "analogy": "A judge giving a fair fixed fine for every mile over the speed limit, rather than sending you to prison for driving 10 mph too fast.",
                "why_it_matters": "Keeps your model from being hijacked by a few corrupt sensor readings or extreme financial anomalies."
            },
            {
                "term": "L1 Loss vs L1 Regularization",
                "what_is_it": "• A classic technical interview question.\n• L1 Loss measures prediction error on data: |y - ŷ|. L1 Regularization (Lasso) penalizes model weights: λ · |w|.",
                "analogy": "L1 Loss grades how closely you hit the target; L1 Regularization penalizes you for using too many unnecessary golf clubs.",
                "why_it_matters": "L1 Loss fits the model, while L1 Regularization pushes unneeded feature weights to zero for feature selection."
            }
        ],
        "types_header": "MAE vs MSE: Choosing the Right Metric",
        "types_badge": "Metric Comparison",
        "quick_types": [
            {
                "type": "Mean Absolute Error (MAE)",
                "definition": "Penalizes errors linearly; robust to outliers and easy to interpret in real-world units.",
                "looks_like": "mean_absolute_error(y_true, y_pred)"
            },
            {
                "type": "Mean Squared Error (MSE)",
                "definition": "Penalizes errors quadratically; smooth math for gradient descent, but heavily influenced by outliers.",
                "looks_like": "mean_squared_error(y_true, y_pred)"
            },
            {
                "type": "L1 Loss (Per-Sample)",
                "definition": "The absolute error of an individual prediction, written as L = |y - ŷ|.",
                "looks_like": "torch.nn.L1Loss()"
            },
            {
                "type": "L1 Regularization (Lasso)",
                "definition": "Adds the sum of absolute weight magnitudes to the loss function to encourage sparse features.",
                "looks_like": "Lasso(alpha=0.1)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "| · |",
                "meaning": "Absolute Value",
                "plain_english": "Removes the negative sign (e.g., |-5| becomes +5)"
            },
            {
                "symbol": "n",
                "meaning": "Number of Predictions",
                "plain_english": "Total count of records evaluated"
            },
            {
                "symbol": "y_i - ŷ_i",
                "meaning": "Raw Residual",
                "plain_english": "The actual value minus the model's guess"
            },
            {
                "symbol": "L1 Norm (|| · ||_1)",
                "meaning": "Manhattan Distance",
                "plain_english": "Sum of absolute coordinates along grid lines"
            }
        ],
        "numerical_example": "How MAE Resists Outliers Better Than MSE:\nSuppose actual values are: y = [10, 10, 10]\nModel predictions are: ŷ = [10, 10, 100] (Two perfect guesses, One wild outlier!)\n\nStep 1: Calculate Individual Errors:\n• Sample 1: |10 - 10| = 0\n• Sample 2: |10 - 10| = 0\n• Sample 3: |10 - 100| = 90\n\nStep 2: Calculate MAE:\n• Sum = 0 + 0 + 90 = 90\n• MAE = 90 / 3 = 30 units\n\nStep 3: Compare with MSE:\n• Squared errors: 0² + 0² + 90² = 8,100\n• MSE = 8,100 / 3 = 2,700 units squared!\n\nTakeaway: The outlier caused MSE to explode to 2,700, while MAE only climbed to 30. MAE gave a much more reasonable picture of typical error.",
        "pitfalls": "Common Pitfall: Using MAE with standard gradient descent without being aware of the sharp corner at zero. Because the absolute value function |e| has a sharp V-shape at zero, its derivative jumps instantly from -1 to +1, which can cause weights to bounce back and forth instead of settling smoothly. If you need outlier robustness with smooth optimization, use Huber Loss instead. Also, MAE doesn't show direction—check mean signed error to see if your model consistently overpredicts or underpredicts.",
        "core_logic": "Why this matters: While minimizing MSE estimates the mean (average) of the target distribution, minimizing MAE mathematically estimates the median! Because the median is unaffected by extreme outliers, models trained on MAE naturally ignore occasional freak measurements.",
        "architectural_logic": "In PyTorch and TensorFlow, MAE is implemented as nn.L1Loss(). Its gradient is simply the sign of the error: +1 if ŷ > y, and -1 if ŷ < y. Because this gradient has a constant magnitude of 1 regardless of how far off the prediction is, the learning rate must be tuned carefully to avoid overshooting near the minimum.",
        "connected_logic": [
            {
                "title": "Median vs Mean Optimization",
                "content": "• Minimizing MSE guides the model to predict the conditional mean of the data.\n• Minimizing MAE guides the model to predict the conditional median, which explains its natural resistance to extreme outliers."
            },
            {
                "title": "L1 Loss vs L1 Regularization (Lasso)",
                "content": "• L1 Loss measures prediction error: |y - ŷ|.\n• L1 Regularization adds λ · ∑|w| to the loss, creating a diamond-shaped constraint in weight space that zeroes out unimportant features."
            },
            {
                "title": "The Optimization Corner at Zero",
                "content": "• The slope of |x| is -1 for negative numbers and +1 for positive numbers, but undefined at exactly 0.\n• Optimizers use subgradients (choosing 0 at the corner), but weights can still oscillate slightly around the minimum."
            },
            {
                "title": "When to Use MAE over MSE",
                "content": "• Use MAE when extreme outliers are expected (real estate prices, web traffic spikes, delivery times).\n• Use MSE when large errors are disproportionately dangerous and must be penalized heavily."
            }
        ],
        "key_takeaways": [
            "Intuitive Units: Measured in the exact same units as the target variable (dollars, kWh, hours).",
            "Outlier Resistant: Penalizes errors linearly, preventing a single wild outlier from ruining the score.",
            "Estimates the Median: Optimizing MAE learns the median of the target, whereas MSE learns the mean.",
            "L1 Loss vs Regularization: L1 loss measures prediction error; L1 regularization creates sparse weights."
        ],
        "definition_bullets": [
            "Mean Absolute Error (MAE): The average of absolute differences between actual values and predicted values.",
            "L1 Loss: The absolute value of the prediction error, measured linearly without squaring."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_mae":
            c.update(mae_data)
            print("Updated concept_mae in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_mae":
            c.update(mae_data)
            print("Updated concept_mae in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_mae".*?\},(?=\s*\{\s*"id":\s*"concept_rmse")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(mae_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_mae in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
