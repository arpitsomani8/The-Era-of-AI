import json

SMOTE_UPDATE = {
    "def": "SMOTE (Synthetic Minority Over-sampling Technique) is an imbalanced data preprocessing algorithm that synthesizes new, plausible minority instances by interpolating along the line segments connecting k-nearest minority neighbors in feature space.",
    "definition": "SMOTE (Synthetic Minority Over-sampling Technique) is an imbalanced data preprocessing algorithm that synthesizes new, plausible minority instances by interpolating along the line segments connecting k-nearest minority neighbors in feature space.",
    "formula": "$$\\mathbf{x}_{\\text{new}} = \\mathbf{x}_i + \\lambda \\cdot (\\mathbf{x}_{zi} - \\mathbf{x}_i), \\quad \\lambda \\sim \\text{Uniform}(0, 1), \\quad \\mathbf{x}_{zi} \\in \\mathcal{N}_k(\\mathbf{x}_i)$$",
    "formula_explanation": "",
    "logic": "Randomly duplicating minority samples causes models to memorize and overfit to exact copies, while random undersampling throws away valuable majority data. SMOTE expands decision boundaries around rare classes by generating artificial intermediate samples along feature vectors, forcing classifiers to generalize broader minority regions.",
    "example": "Credit card fraud detection: Two genuine fraudulent transactions occur near each other in feature space: Point A ($150, 40 km from home) and Point B ($350, 100 km). SMOTE selects Point B as A's neighbor and interpolates a new synthetic fraud sample at ($230, 64 km), teaching the model to recognize intermediate fraud patterns.",
    "simple_summary": "Instead of copy-pasting existing rare examples (which causes severe overfitting) or deleting majority data (which throws away valuable info), SMOTE invents brand-new, realistic minority points by drawing lines between nearest neighbors. Golden rule: apply SMOTE strictly to your training set—never let synthetic points touch your test set!",
    "core_terms": [
        {
            "term": "SMOTE (Synthetic Minority Over-sampling)",
            "what_is_it": "• A technique for handling severe class imbalance that generates brand-new, plausible minority examples by interpolating along lines connecting existing minority points in feature space.\n• Instead of copy-pasting the same rare examples over and over (which causes models to memorize and overfit), it creates realistic intermediate points along nearest-neighbor vectors.",
            "analogy": "Blending colors: rather than photocopying a few blue dots onto a white canvas, painting fresh shades of blue along the lines connecting existing blue dots.",
            "why_it_matters": "Expands the decision boundary around rare events (fraud, cancer, customer churn) without throwing away valuable majority data."
        },
        {
            "term": "The Deadly Pre-Split Leakage Trap",
            "what_is_it": "• The catastrophic mistake of running SMOTE on the entire dataset before performing a train/test split.\n• Because synthetic points are generated using nearest neighbors, test set characteristics are baked directly into the training data, producing fake 99% accuracy scores that collapse in production.",
            "analogy": "Looking at the final exam's answer key to write study flashcards: you score 100% on the practice test, but fail when faced with genuinely new real-world questions.",
            "why_it_matters": "The #1 technical interview blunder; enforces the golden rule: split raw data first, and apply SMOTE strictly to the training fold inside an imblearn pipeline."
        },
        {
            "term": "Cost-Sensitive Learning (class_weight='balanced')",
            "what_is_it": "• The modern, clean alternative to SMOTE that balances training by modifying the model's loss function rather than inventing artificial rows.\n• Multiplies the loss penalty for misclassifying a minority instance (e.g. by 100x), forcing the optimizer to pay equal attention to rare cases without introducing synthetic noise.",
            "analogy": "A high-stakes security checkpoint: missing an ordinary commuter is a minor delay, but missing a prohibited weapon carries an immediate 100x severe disciplinary penalty.",
            "why_it_matters": "Often outperforms SMOTE in modern gradient-boosted trees (XGBoost, LightGBM) by avoiding artificial boundary noise and preserving real-world sample distributions."
        }
    ],
    "types_header": "Advanced SMOTE Algorithms & Cost Alternatives",
    "types_badge": "Resampling Strategies",
    "quick_types": [
        {
            "type": "SMOTE (Standard Interpolation)",
            "definition": "Generates synthetic minority examples by linear interpolation among k-nearest minority neighbors.",
            "looks_like": "from imblearn.over_sampling import SMOTE; SMOTE(k_neighbors=5)"
        },
        {
            "type": "Borderline-SMOTE",
            "definition": "Synthesizes points strictly along the decision boundary where the classifier is most uncertain.",
            "looks_like": "BorderlineSMOTE(kind='borderline-1')"
        },
        {
            "type": "SMOTE-NC (Nominal & Continuous)",
            "definition": "Variant handling mixed tabular datasets by using median/mode logic on categorical columns.",
            "looks_like": "SMOTENC(categorical_features=[0, 2])"
        },
        {
            "type": "SMOTE-Tomek (Cleaned Hybrid)",
            "definition": "Two-stage pipeline oversampling with SMOTE then pruning overlapping boundary noise using Tomek links.",
            "looks_like": "from imblearn.combine import SMOTETomek; SMOTETomek()"
        },
        {
            "type": "class_weight='balanced'",
            "definition": "Cost-sensitive loss weighting alternative that penalizes minority errors without synthesizing fake data.",
            "looks_like": "RandomForestClassifier(class_weight='balanced')"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x_new",
            "meaning": "Synthetic Minority Sample",
            "plain_english": "The newly generated artificial data point created in feature space"
        },
        {
            "symbol": "x_i",
            "meaning": "Seed Minority Observation",
            "plain_english": "An original minority class observation selected for oversampling"
        },
        {
            "symbol": "x_zi",
            "meaning": "Nearest Minority Neighbor",
            "plain_english": "One of the k closest minority-class neighbors to x_i in Euclidean feature space"
        },
        {
            "symbol": "λ (lambda)",
            "meaning": "Random Interpolation Weight",
            "plain_english": "A random scalar sampled from Uniform(0, 1) determining distance along the segment"
        },
        {
            "symbol": "N_k(x_i)",
            "meaning": "K-Nearest Minority Neighbors",
            "plain_english": "The set of k nearest minority neighbors evaluated within the minority subset"
        }
    ],
    "numerical_example": "Generating a Synthetic Fraud Transaction in 2D Feature Space:\nFeatures: [Amount ($), Distance from Home (km)]\n• Seed Fraud Sample x_i: [$150, 40 km]\n• Nearest Fraud Neighbor x_zi: [$350, 100 km]\n\n1. Calculate Vector Difference (Direction Segment):\n   Δ = x_zi - x_i = [350 - 150, 100 - 40] = [200, 60]\n\n2. Sample Random Uniform Interpolator:\n   Draw λ ~ Uniform(0, 1) → Suppose λ = 0.40\n\n3. Calculate Synthetic Point Coordinates:\n   x_new = x_i + λ · Δ\n   x_new = [150, 40] + 0.40 · [200, 60]\n   x_new = [150 + 80, 40 + 24] = [$230, 64 km]\n\nOutcome: SMOTE created a realistic new synthetic fraud instance at ($230, 64 km) lying directly along the linear manifold connecting genuine fraud cases, teaching the model to cover the intermediate risk zone.",
    "pitfalls": "Common Pitfall: Applying SMOTE to the entire dataset before train/test splitting. This creates catastrophic data leakage because synthetic points derived from test instances are injected into the training set, fabricating false 99% accuracy scores. Always split first, fit SMOTE strictly on the training partition, and evaluate on an untouched, naturally imbalanced test set. Also, never run standard SMOTE on categorical columns without using SMOTE-NC.",
    "core_logic": "Why this matters: Standard maximum likelihood algorithms maximize overall accuracy, causing them to neglect rare minority classes. SMOTE populates sparse minority feature space, expanding classification decision boundaries toward the majority class to balance recall and precision.",
    "architectural_logic": "In production machine learning pipelines, SMOTE is encapsulated inside imblearn.pipeline.Pipeline rather than Scikit-Learn Pipeline. This ensures that during cross-validation, SMOTE runs strictly on inner training folds while leaving holdout validation folds 100% untouched.",
    "connected_logic": [
        {
            "title": "Imbalanced-Learn Pipeline & Cross-Validation Isolation",
            "content": "• In cross-validation, using Scikit-Learn's standard Pipeline fails because SMOTE transforms both features X and labels y.\n• Production workflows use imblearn.pipeline.Pipeline, which applies SMOTE strictly during fit on inner training folds while leaving holdout validation folds 100% un-resampled during predict."
        },
        {
            "title": "The Outlier Bridge Problem in Overlapping Classes",
            "content": "• If a rare fraud transaction is actually a mislabeled outlier sitting deep inside the majority legitimate cluster, standard SMOTE draws interpolation bridges across majority space.\n• This pollutes the legitimate cluster with synthetic fraud points; pairing SMOTE with Edited Nearest Neighbors (SMOTE-ENN) automatically prunes these conflicting noisy bridge samples."
        },
        {
            "title": "Tree Models & scale_pos_weight in Gradient Boosters",
            "content": "• Gradient boosted decision trees (XGBoost, LightGBM, CatBoost) build leaf splits based on sum of first and second-order gradients (G, H).\n• Setting scale_pos_weight = N_neg / N_pos scales positive sample gradients directly, training optimal decision boundaries without increasing dataset row count or introducing interpolation artifacts."
        },
        {
            "title": "Post-Resampling Probability Calibration",
            "content": "• Artificially inflating minority prevalence (e.g. from 1% to 50%) shifts the base rate modeled by logistic regressions and neural networks.\n• While ranking metrics (ROC-AUC) remain intact, raw output probabilities become heavily overestimated; applying Platt scaling or Isotonic Regression on untouched validation data recalibrates true posterior probabilities."
        }
    ],
    "key_takeaways": [
        "Feature Space Interpolation: Generates synthetic minority points along line segments connecting nearest neighbors instead of duplicating rows.",
        "Leakage Prevention: Apply SMOTE strictly to the training fold; test sets must remain 100% raw, untouched, and naturally imbalanced.",
        "Pipeline Integration: Use imblearn.pipeline.Pipeline to prevent data leakage during K-Fold cross-validation.",
        "Cost-Sensitive Alternative: In modern gradient boosters, class_weight='balanced' or scale_pos_weight often achieves equal performance without synthetic noise."
    ],
    "definition_bullets": [
        "SMOTE: An oversampling technique that synthesizes novel minority class observations by interpolating between nearest neighbors in feature space.",
        "Cost-Sensitive Learning: A training methodology that assigns disproportionately higher loss penalties to minority class errors to combat imbalance."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_smote_oversampling':
            item.update(SMOTE_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_smote_oversampling not found in {filepath}")
        return False
        
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {filepath}")
    return True

# Update concepts.json and all_concepts.json
update_json_file('src/data/concepts.json')
update_json_file('scripts/data_sources/all_concepts.json')

# Update concepts_data_prep.py
def update_concepts_data_prep():
    filepath = 'scripts/data_sources/concepts_data_prep.py'
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_data_prep", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    for item in mod.DATA_CONCEPTS:
        if item.get('id') == 'concept_smote_oversampling':
            item.update(SMOTE_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
