import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    cost_data = {
        "id": "concept_cost_sensitive_weighting",
        "title": "Cost-Sensitive Training & Loss Weighting",
        "topic_id": "data_split",
        "topic_label": "Datasets, Splitting & Class Imbalance",
        "category": "data",
        "category_label": "Data Preprocessing & EDA",
        "raw_subtopic": "Loss Weighting (Cost-sensitive training)",
        "def": "Cost-sensitive training is a technique that teaches a model to treat different mistakes as having different costs, penalizing severe mistakes more heavily in the loss function.",
        "formula": "$$L_{\\text{weighted}} = w_y \\times L, \\quad w_{\\text{minority}} = \\frac{N_{\\text{total}}}{2 \\times N_{\\text{minority}}}$$",
        "logic": "In real life, some mistakes are much worse than others—like missing a disease versus ordering an unnecessary follow-up test. Loss weighting multiplies the penalty whenever the model misses a rare case, forcing it to pay attention without needing to delete or fake any data.",
        "example": "Medical screening: Suppose missing a sick patient is 20 times worse than a false alarm. By giving sick patients a weight of 20 in the loss function, the model is penalized 20 times more for missing them, learning to catch almost all sick cases.",
        "tags": [
            "Cost-Sensitive",
            "Loss Weighting",
            "Class Weights",
            "Sample Weights",
            "scale_pos_weight"
        ],
        "definition": "Cost-sensitive training is a technique that teaches a model to treat different mistakes as having different costs, penalizing severe mistakes more heavily in the loss function.",
        "formula_explanation": "",
        "simple_summary": "Instead of deleting data (downsampling) or creating fake data (SMOTE), cost-sensitive training keeps your original dataset untouched and simply changes the penalties. Mistakes on rare, critical cases get a much higher penalty, so the model learns not to ignore them.",
        "core_terms": [
            {
                "term": "Class Weighting",
                "what_is_it": "• Assigning a fixed penalty weight to every example in a specific class.\n• For example, every fraud transaction gets a weight of 10, while normal transactions get a weight of 1.",
                "analogy": "A referee blowing the whistle with a yellow card for minor fouls, but giving an immediate red card for dangerous tackles.",
                "why_it_matters": "Easy to turn on with class_weight='balanced' in scikit-learn without changing dataset size or adding fake data."
            },
            {
                "term": "Sample Weighting",
                "what_is_it": "• Giving individual rows their own unique weights based on real-world business value.\n• For example, a $50,000 fraudulent transfer gets a much higher weight than a $5 fraudulent transfer.",
                "analogy": "An insurance adjuster spending hours carefully reviewing a million-dollar claim while doing a quick check on a $20 claim.",
                "why_it_matters": "Allows models to align directly with real financial or operational costs instead of treating all rows identically."
            },
            {
                "term": "The Zero-Resampling Advantage",
                "what_is_it": "• Solving class imbalance purely through the math of the loss function without altering your dataset.\n• Retains 100% of your real majority data and creates zero synthetic noise or memory bloat.",
                "analogy": "Adjusting the grading scale on an exam rather than throwing away student test papers or printing duplicate copies.",
                "why_it_matters": "Often the best first baseline in machine learning because it runs fast, saves RAM, and preserves true data distributions."
            }
        ],
        "types_header": "How Major Frameworks Implement Cost-Weighting",
        "types_badge": "Framework Syntax",
        "quick_types": [
            {
                "type": "Scikit-Learn Models",
                "definition": "Automatically calculates weights inversely proportional to class frequencies.",
                "looks_like": "LogisticRegression(class_weight='balanced')"
            },
            {
                "type": "Gradient Boosted Trees (XGBoost)",
                "definition": "Multiplies positive class gradients by the ratio of negative to positive samples.",
                "looks_like": "XGBClassifier(scale_pos_weight=neg_count / pos_count)"
            },
            {
                "type": "LightGBM",
                "definition": "Provides built-in automatic class balancing similar to scikit-learn.",
                "looks_like": "LGBMClassifier(is_unbalance=True)"
            },
            {
                "type": "PyTorch Neural Networks",
                "definition": "Multiplies the positive class loss directly inside binary cross-entropy.",
                "looks_like": "nn.BCEWithLogitsLoss(pos_weight=torch.tensor([w]))"
            },
            {
                "type": "Custom Sample Weights",
                "definition": "Passes an array of custom weights per row into the model's fit function.",
                "looks_like": "model.fit(X_train, y_train, sample_weight=custom_weights)"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "L_weighted",
                "meaning": "Weighted Loss",
                "plain_english": "The total penalty sent to the model after applying importance weights"
            },
            {
                "symbol": "w_y",
                "meaning": "Class Weight",
                "plain_english": "The multiplier applied to mistakes made on class y (e.g., 10x for fraud)"
            },
            {
                "symbol": "scale_pos_weight",
                "meaning": "XGBoost Positive Multiplier",
                "plain_english": "The ratio of negative samples divided by positive samples in XGBoost"
            },
            {
                "symbol": "pos_weight",
                "meaning": "PyTorch Positive Weight",
                "plain_english": "The tensor weight applied to positive class loss in BCEWithLogitsLoss"
            }
        ],
        "numerical_example": "How Class Weights Balance Training with Numbers:\nSuppose your training dataset has:\n• 9,500 legitimate transactions (Class 0)\n• 500 fraud transactions (Class 1)\nTotal = 10,000 transactions (a 19:1 ratio)\n\nStep 1: Calculate balanced weights using the standard formula:\n  w = Total_Samples / (2 × Class_Samples)\n  • Legitimate Weight: w_0 = 10,000 / (2 × 9,500) ≈ 0.53\n  • Fraud Weight: w_1 = 10,000 / (2 × 500) = 10.0\n\nStep 2: Compare mistake penalties:\n  • If the model misclassifies a legitimate transaction with basic loss = 1.0:\n    Penalty = 0.53 × 1.0 = 0.53\n  • If the model misclassifies a fraud transaction with basic loss = 1.0:\n    Penalty = 10.0 × 1.0 = 10.0\n\nResult: The model is penalized roughly 19 times more for missing fraud, forcing it to learn fraud patterns without deleting any legitimate data or making up fake rows.",
        "pitfalls": "Common Pitfall: Evaluating the model using overall accuracy instead of precision, recall, and F1-score. In an imbalanced dataset (e.g., 99% normal and 1% fraud), a model that guesses 'normal' every time gets 99% accuracy but fails completely. Always check recall (how many frauds were caught) and precision (how many flagged alerts were real). Also, remember that class weights shift predicted probabilities upward—calibrate probabilities if your application needs real-world percentage estimates.",
        "core_logic": "Why this matters: Standard algorithms minimize average error across all rows. When one class makes up 99% of the rows, the model can safely ignore the 1% rare class and still achieve 99% accuracy. Cost-sensitive weighting changes the loss math so errors on the rare class carry equal or greater total impact during training.",
        "architectural_logic": "In modern production pipelines (XGBoost, LightGBM, and PyTorch), cost-sensitive training is usually the first choice before trying resampling. It adds zero data preprocessing overhead, leaves validation and test distributions completely raw, and natively integrates into GPU loss computations.",
        "connected_logic": [
            {
                "title": "Class Weights vs Sample Weights",
                "content": "• Class weights apply the same multiplier to every row in a class (e.g., all frauds get 10x).\n• Sample weights assign a custom multiplier to each row individually, allowing you to weight a $100,000 fraud much more heavily than a $10 fraud."
            },
            {
                "title": "No Resampling Required",
                "content": "• Downsampling deletes majority rows, and SMOTE creates synthetic rows.\n• Cost-sensitive training keeps your original dataset 100% intact, avoiding both data destruction and synthetic noise."
            },
            {
                "title": "Integration in Tree Models (scale_pos_weight)",
                "content": "• In gradient boosted trees like XGBoost and LightGBM, set scale_pos_weight equal to negative_samples / positive_samples.\n• This directly scales the gradient and hessian values for positive rows during tree split calculations."
            },
            {
                "title": "Probability Calibration in Production",
                "content": "• Increasing positive weights makes the model predict higher probabilities for positive cases.\n• If your application displays probability percentages to users (e.g. '80% chance of churn'), recalibrate probabilities on untouched validation data using Platt scaling or isotonic regression."
            }
        ],
        "key_takeaways": [
            "No Data Changes: Balances learning by changing mistake penalties instead of deleting or duplicating rows.",
            "Native Support: Built directly into scikit-learn (class_weight='balanced'), XGBoost (scale_pos_weight), and PyTorch.",
            "Sample Weights: Can assign different weights to individual rows based on real business dollars or medical risk.",
            "Evaluate Properly: Always track recall, precision, and PR-AUC instead of standard accuracy."
        ],
        "definition_bullets": [
            "Cost-Sensitive Training: A method where the model is penalized more heavily for certain types of mistakes in the loss function.",
            "Class Weighting: Multiplying the loss for an entire class by a fixed weight to balance learning on rare classes."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_cost_sensitive_weighting":
            c.update(cost_data)
            print("Updated concept_cost_sensitive_weighting in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_cost_sensitive_weighting":
            c.update(cost_data)
            print("Updated concept_cost_sensitive_weighting in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Update in concepts_data_prep.py
    with open("scripts/data_sources/concepts_data_prep.py", "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'\{\s*"id":\s*"concept_cost_sensitive_weighting".*?\}\s*\]'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        lines = json.dumps(cost_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + "\n]"
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_data_prep.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_cost_sensitive_weighting in concepts_data_prep.py")
    else:
        print("Could not find regex match in concepts_data_prep.py")

if __name__ == "__main__":
    main()
