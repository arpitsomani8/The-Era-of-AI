import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    rmse_data = {
        "id": "concept_rmse",
        "title": "Root Mean Squared Error (RMSE)",
        "topic_id": "ml_loss",
        "topic_label": "Loss Functions (L1, L2, MSE, MAE, Log Loss)",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Root Mean Squared Error (RMSE, interpretable in original units)",
        "def": "Root Mean Squared Error (RMSE) is the square root of the Mean Squared Error, which converts the average squared error back into the original units of your data.",
        "formula": "$$\\text{RMSE} = \\sqrt{\\text{MSE}} = \\sqrt{\\frac{1}{n} \\sum_{i=1}^n (y_i - \\hat{y}_i)^2}$$",
        "logic": "Because MSE squares every error, its final number is stuck in squared units (like dollars squared). Taking the square root undoes the squaring, giving you an error score in real-world units that anyone can understand.",
        "example": "Predicting salaries: If your model has an MSE of 25,000,000 dollars squared, that number is impossible to explain to a manager. Taking the square root gives an RMSE of $5,000, clearly stating that the model's predictions are off by roughly $5,000.",
        "tags": [
            "RMSE",
            "Root Mean Squared Error",
            "Regression Metric",
            "Evaluation",
            "MSE"
        ],
        "definition": "Root Mean Squared Error (RMSE) is the square root of the Mean Squared Error, which converts the average squared error back into the original units of your data.",
        "formula_explanation": "",
        "simple_summary": "RMSE is simply the square root of MSE: calculate your errors, square them, find the average, and take the square root. While we train models using MSE because the math is smoother, we always report results using RMSE because it speaks in real units—like dollars, miles, or degrees Celsius.",
        "core_terms": [
            {
                "term": "Root Mean Squared Error (RMSE)",
                "what_is_it": "• The square root of the Mean Squared Error: RMSE = √(MSE).\n• Brings the error metric back into the exact same physical units as the original target variable.",
                "analogy": "Converting area back into length: taking the square root of 25 square feet tells you the room is 5 feet on each side.",
                "why_it_matters": "The single most common evaluation metric reported for regression models in business and Kaggle competitions."
            },
            {
                "term": "Why Train with MSE but Report RMSE",
                "what_is_it": "• The best weights for MSE are mathematically identical to the best weights for RMSE.\n• However, taking the square root during training causes the gradient to divide by zero (1 / 2√MSE) as error reaches zero, crashing the optimizer.",
                "analogy": "Cooking with Celsius in the kitchen because the thermometer is simple, but serving the dish with Fahrenheit on the menu for customers.",
                "why_it_matters": "The golden rule of engineering: optimize MSE during training for clean math, but report RMSE to humans for readability."
            },
            {
                "term": "The RMSE ≥ MAE Relationship",
                "what_is_it": "• RMSE is always greater than or equal to MAE: RMSE ≥ MAE.\n• The bigger the gap between RMSE and MAE, the more your model is making occasional huge outlier mistakes.",
                "analogy": "Comparing average income to average wealth: a large gap tells you a few billionaires are pulling the average up.",
                "why_it_matters": "Comparing RMSE and MAE on the same model instantly reveals whether errors are steady or plagued by wild spikes."
            }
        ],
        "types_header": "Comparing the Core Regression Metrics",
        "types_badge": "Metric Roles",
        "quick_types": [
            {
                "type": "RMSE (Evaluation Champion)",
                "definition": "Expressed in real target units while preserving quadratic penalties on large mistakes.",
                "looks_like": "np.sqrt(mean_squared_error(y_true, y_pred))"
            },
            {
                "type": "MSE (Training Champion)",
                "definition": "Used as the loss function during gradient descent because its derivative is clean and never explodes.",
                "looks_like": "criterion = nn.MSELoss()"
            },
            {
                "type": "MAE (Robust Alternative)",
                "definition": "Penalizes errors linearly; best when you want the median error and immunity to extreme outliers.",
                "looks_like": "mean_absolute_error(y_true, y_pred)"
            },
            {
                "type": "Standard Deviation of Residuals",
                "definition": "RMSE roughly equals the standard deviation of unexplained errors when prediction bias is near zero.",
                "looks_like": "RMSE ≈ std(y - y_hat)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "√ (Square Root)",
                "meaning": "Radical Symbol",
                "plain_english": "Undoes the squaring operation to restore original target units"
            },
            {
                "symbol": "MSE",
                "meaning": "Mean Squared Error",
                "plain_english": "The average of squared residuals before taking the root"
            },
            {
                "symbol": "y - ŷ",
                "meaning": "Prediction Residual",
                "plain_english": "How far off the model was on an individual example"
            },
            {
                "symbol": "n",
                "meaning": "Sample Size",
                "plain_english": "Total number of test records evaluated"
            }
        ],
        "numerical_example": "Calculating RMSE and Comparing with MAE:\nSuppose actual values are y = [10, 20, 30] and predictions are ŷ = [12, 18, 36]:\n\nStep 1: Calculate raw errors (y - ŷ):\n• Sample 1: 10 - 12 = -2\n• Sample 2: 20 - 18 = +2\n• Sample 3: 30 - 36 = -6\n\nStep 2: Calculate MSE:\n• Squared errors: (-2)² = 4, (+2)² = 4, (-6)² = 36\n• Sum = 4 + 4 + 36 = 44\n• MSE = 44 / 3 = 14.67 units squared\n\nStep 3: Calculate RMSE:\n• RMSE = √14.67 ≈ 3.83 units\n\nStep 4: Check MAE Comparison:\n• Absolute errors: 2 + 2 + 6 = 10\n• MAE = 10 / 3 = 3.33 units\n• Notice: RMSE (3.83) > MAE (3.33) because Sample 3's larger error was penalized more heavily!",
        "pitfalls": "Common Pitfall: Using RMSE as a loss function inside custom PyTorch training loops. As your model learns and MSE approaches zero, the derivative 1 / (2√MSE) attempts to divide by zero, causing gradients to explode and producing NaN weights! Always use MSELoss for training, and calculate RMSE only during evaluation by taking np.sqrt() after predictions are made.",
        "core_logic": "Why this matters: In classical statistics, if residuals follow a normal bell curve, RMSE is approximately equal to the standard deviation of your errors. This means you can use the 68-95-99.7 rule: roughly 68% of your model's future predictions will fall within ±1 RMSE of the true answer, and 95% will fall within ±2 RMSE.",
        "architectural_logic": "In modern libraries like Scikit-Learn 1.4+, you can compute RMSE directly using root_mean_squared_error(y_true, y_pred) instead of passing squared=False to mean_squared_error(). In MLflow and Weights & Biases, RMSE is tracked as the primary scalar metric across training epochs.",
        "connected_logic": [
            {
                "title": "Why RMSE ≥ MAE Always Holds",
                "content": "• By Jensen's inequality and the Cauchy-Schwarz theorem, the root-mean-square of any non-zero set of numbers is always greater than or equal to their arithmetic mean.\n• They are only equal if every single error has the exact same size; any variation pushes RMSE higher."
            },
            {
                "title": "The Gradient Exploding Hazard (Why We Avoid RMSE Loss)",
                "content": "• The derivative of RMSE with respect to weights is: d(RMSE)/dw = (1 / 2√MSE) · d(MSE)/dw.\n• When MSE is small, dividing by √MSE causes catastrophic numerical instability, which is why optimizers always train on MSE."
            },
            {
                "title": "The 68-95-99.7 Bell Curve Interpretation",
                "content": "• If errors are normally distributed around zero, RMSE acts as the error standard deviation.\n• You can explain to stakeholders that roughly 95% of predictions will be accurate within ±(2 × RMSE)."
            },
            {
                "title": "When to Prefer MAE Over RMSE",
                "content": "• If occasional large errors are acceptable and you want to reflect the typical middle error, use MAE.\n• If large mistakes carry severe business penalties (e.g., inventory stockouts or flight fuel planning), prioritize RMSE."
            }
        ],
        "key_takeaways": [
            "Root of MSE: RMSE = √(MSE); restores errors to original real-world target units.",
            "Train MSE, Report RMSE: Minimizing MSE minimizes RMSE without risking gradient explosion.",
            "Always ≥ MAE: RMSE is always greater than or equal to MAE; a large gap reveals extreme outliers.",
            "Bell Curve Meaning: For normal errors, about 68% of predictions land within ±1 RMSE of the true value."
        ],
        "definition_bullets": [
            "Root Mean Squared Error (RMSE): The square root of Mean Squared Error, measuring average prediction error in original target units.",
            "Residual Standard Deviation: The statistical spread of prediction errors, which RMSE closely approximates."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_rmse":
            c.update(rmse_data)
            print("Updated concept_rmse in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_rmse":
            c.update(rmse_data)
            print("Updated concept_rmse in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_rmse".*?\},(?=\s*\{\s*"id":\s*"concept_huber_loss")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(rmse_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_rmse in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
