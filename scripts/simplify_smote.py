import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    # Target data for concept_smote_oversampling
    smote_update = {
        "def": "SMOTE (Synthetic Minority Over-sampling Technique) is a preprocessing technique used to handle imbalanced datasets by creating new, realistic synthetic examples of the rare (minority) class instead of simply duplicating existing rows.",
        "formula": "$$\\mathbf{x}_{\\text{new}} = \\mathbf{x}_i + \\lambda \\cdot (\\mathbf{x}_{zi} - \\mathbf{x}_i), \\quad \\lambda \\sim \\text{Uniform}(0, 1)$$",
        "logic": "Simply copying rare examples makes models memorize them (overfitting), while deleting common examples throws away useful data. SMOTE solves this by creating new, realistic examples between nearby rare points, helping the model learn a broader pattern for the rare class.",
        "example": "Fraud detection: Suppose you have two rare fraud transactions: Point A ($150, 40 km away) and Point B ($350, 100 km away). SMOTE creates a new artificial fraud example between them at ($230, 64 km), teaching the model to catch fraud patterns in that middle range.",
        "definition": "SMOTE (Synthetic Minority Over-sampling Technique) is a preprocessing technique used to handle imbalanced datasets by creating new, realistic synthetic examples of the rare (minority) class instead of simply duplicating existing rows.",
        "formula_explanation": "",
        "simple_summary": "Instead of copying existing rare examples (which causes overfitting) or deleting common data (which throws away useful information), SMOTE creates new, realistic examples between nearby rare points. Golden rule: always apply SMOTE only to your training data—never let synthetic points touch your test set!",
        "core_terms": [
            {
                "term": "SMOTE (Synthetic Minority Over-sampling)",
                "what_is_it": "• A technique used to balance datasets by creating new, realistic examples of the rare class instead of simply duplicating existing rows.\n• It picks a rare data point, finds its closest neighbor of the same class, and places a new synthetic example on the line between them.",
                "analogy": "Blending colors: instead of photocopying a few blue dots onto a white canvas, you paint a fresh blue dot on the line between two existing blue dots.",
                "why_it_matters": "Helps models detect rare events (like fraud, disease, or customer churn) without throwing away valuable majority data."
            },
            {
                "term": "The Pre-Split Leakage Trap",
                "what_is_it": "• The common mistake of running SMOTE on your entire dataset before splitting into train and test sets.\n• When you do this, information from the test set leaks into the training data through synthetic points, giving you fake high scores that fail in the real world.",
                "analogy": "Looking at the final exam questions while making your study flashcards: you score 100% in practice, but fail the real exam.",
                "why_it_matters": "Always split your data first, and apply SMOTE strictly to the training set."
            },
            {
                "term": "Cost-Sensitive Learning (class_weight='balanced')",
                "what_is_it": "• A popular alternative to SMOTE that adjusts the penalty for mistakes instead of creating artificial rows.\n• It penalizes the model much more heavily when it misses a rare example, forcing it to pay attention without making up fake data.",
                "analogy": "A security checkpoint: missing an ordinary commuter is a minor delay, but missing a real threat carries an immediate severe penalty.",
                "why_it_matters": "Often works better than SMOTE for modern tree models (like XGBoost and LightGBM) because it introduces no artificial noise."
            }
        ],
        "types_header": "SMOTE Variations & Cost-Sensitive Alternatives",
        "types_badge": "Resampling Strategies",
        "quick_types": [
            {
                "type": "Standard SMOTE",
                "definition": "Creates synthetic examples by finding nearest neighbors in the minority class and picking points between them.",
                "looks_like": "from imblearn.over_sampling import SMOTE; SMOTE(k_neighbors=5)"
            },
            {
                "type": "Borderline-SMOTE",
                "definition": "Creates synthetic points only near the decision boundary where the model is most unsure.",
                "looks_like": "BorderlineSMOTE(kind='borderline-1')"
            },
            {
                "type": "SMOTE-NC (Categorical & Continuous)",
                "definition": "A version of SMOTE designed for mixed datasets containing both numbers and categories.",
                "looks_like": "SMOTENC(categorical_features=[0, 2])"
            },
            {
                "type": "SMOTE-Tomek (Cleaned Hybrid)",
                "definition": "Generates points using SMOTE, then cleans up confusing boundary points that overlap with the majority class.",
                "looks_like": "from imblearn.combine import SMOTETomek; SMOTETomek()"
            },
            {
                "type": "class_weight='balanced'",
                "definition": "Penalizes mistakes on rare classes more heavily without generating any artificial data rows.",
                "looks_like": "RandomForestClassifier(class_weight='balanced')"
            }
        ],
        "symbol_guide": [
            {
                "symbol": "x_new",
                "meaning": "Synthetic Data Point",
                "plain_english": "The new artificial example created by SMOTE"
            },
            {
                "symbol": "x_i",
                "meaning": "Original Rare Example",
                "plain_english": "An existing data point from the rare (minority) class"
            },
            {
                "symbol": "x_zi",
                "meaning": "Nearest Neighbor",
                "plain_english": "One of the closest rare examples to x_i in the dataset"
            },
            {
                "symbol": "λ (lambda)",
                "meaning": "Random Multiplier (0 to 1)",
                "plain_english": "A random number between 0 and 1 that picks where along the line to place the new point"
            }
        ],
        "numerical_example": "Creating a Synthetic Fraud Example between Two Points:\nSuppose two rare fraud points in your dataset are:\n• Point A: (2, 4) — for example, $200 amount, 4 attempts\n• Point B: (6, 8) — for example, $600 amount, 8 attempts\n\nStep 1: Find the difference between them:\n  Difference = Point B - Point A = (6 - 2, 8 - 4) = (4, 4)\n\nStep 2: Pick a random number between 0 and 1:\n  Suppose random weight λ = 0.5 (exactly halfway)\n\nStep 3: Calculate the new synthetic point:\n  New Point = Point A + λ × Difference\n  New Point = (2, 4) + 0.5 × (4, 4) = (2 + 2, 4 + 2) = (4, 6)\n\nResult: SMOTE created a brand-new, realistic synthetic example at (4, 6) on the line connecting the two existing fraud transactions.",
        "pitfalls": "Common Pitfall: Applying SMOTE before splitting your data into train and test sets. This causes data leakage because synthetic training points are created using test data, leading to artificially high scores that fail in production. Always split your raw data first, and run SMOTE only on the training set. Also, remember that standard SMOTE only works on continuous numeric features—use SMOTE-NC if your data includes categorical columns.",
        "core_logic": "Why this matters: Standard machine learning models focus on maximizing overall accuracy. In imbalanced data (like 99% non-fraud and 1% fraud), a model can get 99% accuracy by simply guessing 'non-fraud' every time. SMOTE adds synthetic examples of the rare class so the model actually learns how to recognize it.",
        "architectural_logic": "In Python, always use imblearn.pipeline.Pipeline instead of Scikit-Learn's standard pipeline when using SMOTE. This guarantees that during cross-validation, SMOTE is fitted only on the training folds and never touches the validation folds.",
        "connected_logic": [
            {
                "title": "Using imblearn Pipeline in Cross-Validation",
                "content": "• Scikit-Learn's standard pipeline does not resample data during cross-validation.\n• Using imblearn.pipeline.Pipeline automatically applies SMOTE only to training folds while keeping validation folds untouched."
            },
            {
                "title": "The Outlier and Noise Problem",
                "content": "• If a rare example is actually an outlier or noise located inside the majority class, standard SMOTE might draw points right into the majority region.\n• Pairing SMOTE with cleaning techniques (like SMOTE-Tomek or SMOTE-ENN) removes these confusing noisy points."
            },
            {
                "title": "Tree Models and Class Weights",
                "content": "• Modern tree models like XGBoost, LightGBM, and CatBoost have built-in parameters (like scale_pos_weight or class_weight='balanced').\n• These parameters often achieve great results directly without needing to generate artificial rows."
            },
            {
                "title": "Probability Calibration After SMOTE",
                "content": "• Because SMOTE artificially increases the proportion of rare examples in training, predicted probabilities may be higher than real-world probabilities.\n• The model will still rank examples well, but if you need exact probabilities, calibrate them on untouched validation data."
            }
        ],
        "key_takeaways": [
            "Creates New Points: Synthesizes new examples between nearby rare points instead of copy-pasting existing rows.",
            "Train Set Only: Always apply SMOTE strictly to the training data after splitting; never touch test data.",
            "Use imblearn Pipeline: Guarantees no data leakage during cross-validation folds.",
            "Evaluate Proper Metrics: Look at recall, precision, and F1-score rather than simple overall accuracy."
        ],
        "definition_bullets": [
            "SMOTE: A technique that balances datasets by creating new, realistic synthetic examples between nearby points of the rare class.",
            "Cost-Sensitive Learning: An alternative approach that increases the penalty for misclassifying rare examples instead of creating fake data."
        ]
    }

    # Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_smote_oversampling":
            c.update(smote_update)
            print("Updated concept_smote_oversampling in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_smote_oversampling":
            c.update(smote_update)
            print("Updated concept_smote_oversampling in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # Now update concepts_data_prep.py
    with open("scripts/data_sources/concepts_data_prep.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Find the smote block in concepts_data_prep.py and replace it
    # We can serialize the updated smote dict to python code or replace the block
    pattern = r'\{\s*"id":\s*"concept_smote_oversampling".*?\},(?=\s*\{\s*"id":\s*"concept_resampling_strategies")'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # Find the concept object from concepts
        smote_obj = [c for c in concepts if c.get("id") == "concept_smote_oversampling"][0]
        replacement = json.dumps(smote_obj, indent=8, ensure_ascii=False) + ","
        # Format indentation to match python file (4 spaces indentation for dict)
        # Indent every line with 4 spaces except first
        lines = json.dumps(smote_obj, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        new_content = content[:match.start()] + indented_replacement + content[match.end():]
        with open("scripts/data_sources/concepts_data_prep.py", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Updated concept_smote_oversampling in concepts_data_prep.py")
    else:
        print("Could not find regex match in concepts_data_prep.py")

if __name__ == "__main__":
    main()
