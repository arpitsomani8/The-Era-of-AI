import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    mse_data = {
        "id": "concept_mse",
        "title": "Mean Squared Error (MSE)",
        "topic_id": "ml_loss",
        "topic_label": "Loss Functions (L1, L2, MSE, MAE, Log Loss)",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Mean Squared Error (MSE across all training examples)",
        "def": "Mean Squared Error (MSE) is the average of the squared differences between actual values and predicted values across an entire dataset.",
        "formula": "$$\\text{MSE} = \\frac{1}{n} \\sum_{i=1}^n (y_i - \\hat{y}_i)^2$$",
        "logic": "To measure how well a model performs across a whole dataset, we calculate each prediction error, square it, add them all up, and divide by the number of examples. Squaring ensures positive and negative errors don't cancel each other out.",
        "example": "Evaluating 3 house price predictions: House 1 is off by $10k (squared: 100M), House 2 is off by $20k (squared: 400M), and House 3 is off by $0k (squared: 0). The MSE is (100M + 400M + 0) / 3 = 166.7M dollars squared.",
        "tags": [
            "MSE",
            "Mean Squared Error",
            "Regression Metric",
            "Loss Function",
            "R-Squared"
        ],
        "definition": "Mean Squared Error (MSE) is the average of the squared differences between actual values and predicted values across an entire dataset.",
        "formula_explanation": "",
        "simple_summary": "MSE is the standard scorecard for regression models. It finds the error for every row, squares each one so negatives become positive, and calculates the overall average. A lower MSE means better predictions. Because its units are squared (like 'dollars squared'), engineers often take its square root to get RMSE, which brings the error back to normal dollars.",
        "core_terms": [
            {
                "term": "Mean Squared Error (MSE)",
                "what_is_it": "• The average squared difference between true labels and predictions across all rows in a dataset.\n• The 4-step recipe: find each error → square it → add them up → divide by n.",
                "analogy": "A class average on a math test, but where every student's mistake is squared before averaging so big slip-ups drag the average down much faster.",
                "why_it_matters": "The primary loss function used to train regression models in scikit-learn, PyTorch, and TensorFlow."
            },
            {
                "term": "The Squared Units Problem (Why RMSE Exists)",
                "what_is_it": "• Because errors are squared, MSE is reported in squared units (e.g., dollars squared, square degrees Celsius).\n• Taking the square root gives Root Mean Squared Error (RMSE), returning the metric back to original, readable units.",
                "analogy": "Saying your luggage is 25 square pounds over the weight limit instead of just 5 pounds.",
                "why_it_matters": "Engineers optimize MSE during training because it has simpler math, but report RMSE to business stakeholders so the numbers make sense."
            },
            {
                "term": "R² Score (Coefficient of Determination)",
                "what_is_it": "• A normalized metric that compares your model's MSE against simply guessing the average target every time.\n• R² = 1.0 means perfect predictions (100% variance explained); R² = 0.0 means no better than guessing the mean.",
                "analogy": "A golf handicap or percentage grade: tells you how close your performance is to perfection regardless of course difficulty.",
                "why_it_matters": "Allows you to judge model quality without worrying about target units, since MSE has no universal scale."
            }
        ],
        "types_header": "MSE: Roles & Connected Metrics",
        "types_badge": "Metric Variations",
        "quick_types": [
            {
                "type": "MSE as Training Loss",
                "definition": "Guides gradient descent to update weights during model fitting.",
                "looks_like": "criterion = nn.MSELoss()"
            },
            {
                "type": "MSE as Evaluation Metric",
                "definition": "Measures overall prediction accuracy on an unseen test dataset.",
                "looks_like": "mean_squared_error(y_test, y_pred)"
            },
            {
                "type": "RMSE (Root Mean Squared Error)",
                "definition": "The square root of MSE; expresses error in the original units of the target variable.",
                "looks_like": "np.sqrt(mean_squared_error(y, y_pred))"
            },
            {
                "type": "R² Score (Variance Explained)",
                "definition": "Scales MSE between 0 and 1; 1.0 means the model explains 100% of data variation.",
                "looks_like": "r2_score(y_test, y_pred)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "n (or N)",
                "meaning": "Sample Size",
                "plain_english": "Total number of predictions evaluated"
            },
            {
                "symbol": "y_i",
                "meaning": "Actual Value",
                "plain_english": "The true ground-truth value for example i"
            },
            {
                "symbol": "ŷ_i",
                "meaning": "Predicted Value",
                "plain_english": "The model's predicted value for example i"
            },
            {
                "symbol": "∑",
                "meaning": "Summation",
                "plain_english": "Add up all squared errors across all n examples"
            }
        ],
        "numerical_example": "Calculating MSE Step-by-Step for 3 Predictions:\nSuppose we want to evaluate 3 student test scores:\n• Student 1: Actual y = 80, Predicted ŷ = 85\n• Student 2: Actual y = 90, Predicted ŷ = 90\n• Student 3: Actual y = 70, Predicted ŷ = 60\n\nStep 1: Calculate individual errors (y - ŷ):\n• Student 1 error: 80 - 85 = -5\n• Student 2 error: 90 - 90 = 0\n• Student 3 error: 70 - 60 = +10\n\nStep 2: Square each error:\n• (-5)² = 25\n• (0)² = 0\n• (10)² = 100\n\nStep 3: Add them up (Sum of Squared Errors):\n• Sum = 25 + 0 + 100 = 125\n\nStep 4: Divide by n = 3 to get the Mean:\n• MSE = 125 / 3 = 41.67 test points squared\n• (Bonus RMSE: √41.67 ≈ 6.45 test points off on average)",
        "pitfalls": "Common Pitfall: Comparing raw MSE across different datasets. Because MSE depends directly on the units and scale of your target variable, an MSE of 50 might be great for house prices but terrible for human body temperature! Always compare models on the exact same test dataset. Also, remember that a model with lower training MSE isn't necessarily better if it is overfitting—always evaluate MSE on unseen test data.",
        "core_logic": "Why this matters: In the Bias-Variance tradeoff, a model's expected MSE can be split into three parts: Bias² + Variance + Irreducible Noise. Minimizing MSE requires balancing a model simple enough to have low variance, yet flexible enough to have low bias.",
        "architectural_logic": "In deep learning frameworks, MSE is implemented in vectorized C++/CUDA. In PyTorch, nn.MSELoss() computes the sum of squared differences and divides by the batch size in parallel across GPU threads, providing the gradients needed for backpropagation.",
        "connected_logic": [
            {
                "title": "Why MSE Squares Instead of Taking Absolute Values",
                "content": "• Squaring ensures that underpredictions (-5) and overpredictions (+5) don't cancel each other out to zero.\n• Unlike absolute values, squaring produces smooth derivatives everywhere, making gradient descent mathematically simpler."
            },
            {
                "title": "The Bias-Variance Decomposition of MSE",
                "content": "• Mathematically, Expected MSE = Bias² + Variance + Irreducible Noise.\n• If a model is too simple, high Bias drives up MSE; if a model is too complex and memorizes noise, high Variance drives up test MSE."
            },
            {
                "title": "From MSE to R² Score",
                "content": "• Formula: R² = 1 - (MSE_model / Variance_data).\n• If the model predicts the mean for every row, MSE equals dataset variance and R² = 0. If the model makes zero errors, MSE = 0 and R² = 1.0."
            },
            {
                "title": "When to Use MAE Instead of MSE",
                "content": "• MSE gives heavy weight to large errors; if you have extreme outliers, MSE gets dominated by a few wild points.\n• In datasets with frequent bad measurements or financial outliers, Mean Absolute Error (MAE) provides a more robust summary."
            }
        ],
        "key_takeaways": [
            "The 4 Steps: Find errors → square each → add up → divide by n.",
            "No Canceling: Squaring makes all errors positive and penalizes larger mistakes more heavily.",
            "RMSE for Units: Take the square root of MSE to get errors back in original business units.",
            "Compare Fairly: Always evaluate MSE on the same held-out test dataset, not training data."
        ],
        "definition_bullets": [
            "Mean Squared Error (MSE): The average of squared differences between actual targets and model predictions.",
            "Root Mean Squared Error (RMSE): The square root of MSE, measuring the average error in original target units."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_mse":
            c.update(mse_data)
            print("Updated concept_mse in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_mse":
            c.update(mse_data)
            print("Updated concept_mse in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_mse".*?\},(?=\s*\{\s*"id":\s*"concept_mae")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(mse_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_mse in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
