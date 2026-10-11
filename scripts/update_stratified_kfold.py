import json

STRATIFIED_KFOLD_UPDATE = {
    "def": "Stratified K-Fold Cross-Validation is a model evaluation protocol that partitions a classification dataset into K folds while preserving the exact percentage of each target class across every single fold.",
    "definition": "Stratified K-Fold Cross-Validation is a model evaluation protocol that partitions a classification dataset into K folds while preserving the exact percentage of each target class across every single fold.",
    "formula": "$$P(Y = c \\mid \\mathcal{F}_k) = P(Y = c \\mid \\mathcal{D}) = \\frac{N_c}{N}, \\quad \\text{CV}_{\\text{score}} = \\frac{1}{K}\\sum_{k=1}^K \\mathcal{M}\\big(f_{\\theta \\setminus k}, \\mathcal{F}_k\\big)$$",
    "formula_explanation": "",
    "logic": "Standard random K-Fold splitting can easily create validation folds with too few or even zero minority positive cases on imbalanced datasets. Stratified K-Fold forces every fold to mirror the global class ratio, ensuring fair, low-variance evaluation scores across binary and multi-class problems.",
    "example": "Credit card fraud detection: In a dataset with 1,000 transactions and only 50 fraud cases (5% minority), Stratified 5-Fold CV guarantees that every single fold contains exactly 10 fraud transactions and 190 legitimate transactions, preventing evaluation folds from being blind to fraud.",
    "simple_summary": "Stratified K-Fold is the gold standard for testing classification models. Instead of randomly slicing data (which can leave some test chunks with zero rare cases), it ensures every single fold has the exact same ratio of classes as your original dataset. On imbalanced data, always evaluate folds using ROC-AUC, PR-AUC, or F1-Score rather than simple Accuracy.",
    "core_terms": [
        {
            "term": "Stratified K-Fold Cross-Validation",
            "what_is_it": "• A model validation technique that splits a dataset into K folds while guaranteeing that each fold preserves the exact same class label percentages as the full dataset.\n• Solves the random-split failure where minority classes (e.g. 1% fraud or rare disease cases) get completely missed or clustered into a single fold.",
            "analogy": "Slicing a marble cake evenly: ensuring that every slice of cake has the exact same ratio of chocolate and vanilla swirl, rather than one slice getting all the chocolate and another getting none.",
            "why_it_matters": "The universal, default cross-validation standard for all classification problems in machine learning, ensuring honest, low-variance evaluation scores."
        },
        {
            "term": "The Cross-Validation Family Tree",
            "what_is_it": "• Stratified K-Fold: Balances class proportions across folds for classification.\n• GroupKFold: Keeps all records from the same user or patient in a single fold to prevent identity leakage.\n• TimeSeriesSplit: Strictly trains on past data and validates on future data without shuffling.\n• StratifiedGroupKFold: Combines both worlds—keeps patient records together while simultaneously balancing rare disease ratios across folds.",
            "analogy": "Organizing team tournaments: choosing whether to balance teams by skill level (Stratified), keep family members together on the same team (Group), or play chronological qualifiers (TimeSeries).",
            "why_it_matters": "Guides engineers to select the exact right validator for their domain, avoiding devastating evaluation mistakes."
        },
        {
            "term": "The Accuracy Paradox on Imbalanced Folds",
            "what_is_it": "• The statistical trap where a model achieves 99% accuracy on an imbalanced dataset by simply predicting the majority class 100% of the time, while detecting zero positive cases.\n• Stratified validation must always be paired with imbalance-aware scoring metrics like ROC-AUC, PR-AUC (Average Precision), or F1-Score rather than plain accuracy.",
            "analogy": "A smoke detector that has its battery removed: it is 99.9% accurate every day because houses rarely catch fire, but it is 100% useless when a real fire starts.",
            "why_it_matters": "Prevents deploying worthless baseline models that report deceptive 99% benchmark scores to business executives."
        }
    ],
    "types_header": "Cross-Validation Ensembles & Scoring Metrics",
    "types_badge": "Evaluation Protocols",
    "quick_types": [
        {
            "type": "StratifiedKFold(n_splits=5)",
            "definition": "Standard Scikit-Learn cross-validator enforcing balanced target class proportions across all K folds.",
            "looks_like": "StratifiedKFold(n_splits=5, shuffle=True, random_state=42)"
        },
        {
            "type": "StratifiedGroupKFold",
            "definition": "Hybrid cross-validator keeping patient/user groups intact while balancing minority class proportions.",
            "looks_like": "StratifiedGroupKFold(n_splits=5).split(X, y, groups=patient_id)"
        },
        {
            "type": "cross_val_score(scoring='roc_auc')",
            "definition": "Cross-validation runner measuring ranking separation rather than misleading accuracy on imbalanced folds.",
            "looks_like": "cross_val_score(model, X, y, cv=skf, scoring='roc_auc')"
        },
        {
            "type": "PR-AUC (Average Precision Scoring)",
            "definition": "The gold standard evaluation metric for severe class imbalance (< 1% minority cases).",
            "looks_like": "cross_val_score(model, X, y, cv=skf, scoring='average_precision')"
        },
        {
            "type": "RepeatedStratifiedKFold",
            "definition": "Multi-pass stratified cross-validation repeating K-fold splits across multiple random seeds for tiny datasets.",
            "looks_like": "RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "F_k",
            "meaning": "Validation Fold Partition k",
            "plain_english": "The holdout evaluation fold for round k, where 1 ≤ k ≤ K"
        },
        {
            "symbol": "Y = c",
            "meaning": "Target Class Label c",
            "plain_english": "The categorical class outcome, such as class 1 for Fraud and 0 for Legitimate"
        },
        {
            "symbol": "D",
            "meaning": "Full Dataset",
            "plain_english": "The entire labeled sample collection containing N total observations"
        },
        {
            "symbol": "N_c / N",
            "meaning": "Global Class Proportion",
            "plain_english": "The exact percentage of class c present across the global dataset"
        },
        {
            "symbol": "CV_score",
            "meaning": "Cross-Validation Metric",
            "plain_english": "The arithmetic average of the performance metric across all K validation runs"
        },
        {
            "symbol": "M(...)",
            "meaning": "Imbalance-Aware Evaluation Metric",
            "plain_english": "The evaluation scoring function, such as ROC-AUC, PR-AUC, or F1-Score"
        }
    ],
    "numerical_example": "Credit Card Fraud Detection Across 5 Folds (K = 5):\nDataset size N = 1,000 transactions.\n• Class 0 (Legitimate): 950 transactions (95.0%)\n• Class 1 (Fraud): 50 transactions (5.0% minority)\n\n1. Standard K-Fold Failure (Random Shuffling):\n   Random slicing might assign 22 fraud cases to Fold 1, but only 2 fraud cases to Fold 4. Evaluating a model on only 2 positive cases creates massive statistical noise and unreliable metric swings.\n\n2. Stratified 5-Fold Allocation:\n   Each fold receives exactly 1,000 / 5 = 200 transactions.\n   • Class 0 per fold: 950 / 5 = 190 legitimate transactions (95.0%)\n   • Class 1 per fold: 50 / 5 = 10 fraud transactions (5.0%)\n\n3. Cross-Validation Execution Across 5 Folds:\n   • Round 1: Train on Folds 2–5 (40 fraud, 760 legit) → Test Fold 1 (10 fraud, 190 legit) → ROC-AUC = 0.94\n   • Round 2: Train on Folds 1, 3–5 → Test Fold 2 → ROC-AUC = 0.91\n   • Round 3: Train on Folds 1, 2, 4, 5 → Test Fold 3 → ROC-AUC = 0.93\n   • Round 4: Train on Folds 1–3, 5 → Test Fold 4 → ROC-AUC = 0.95\n   • Round 5: Train on Folds 1–4 → Test Fold 5 → ROC-AUC = 0.92\n\n4. Compute Final Cross-Validation Generalization Score:\n   CV_ROC-AUC = (0.94 + 0.91 + 0.93 + 0.95 + 0.92) / 5 = 4.65 / 5 = 0.930\n\nOutcome: Every fold had an identical, robust 5% fraud representation, delivering a stable, low-variance estimate of production performance.",
    "pitfalls": "Common Pitfall: Using Accuracy as the scoring metric when running Stratified K-Fold on imbalanced data. A dummy model predicting 'Legitimate' 100% of the time achieves 95% Accuracy across all folds despite catching zero fraud. Always specify scoring='roc_auc', scoring='average_precision', or scoring='f1'. Also, ensure minority class count N_c >= n_splits, otherwise stratification cannot place at least one minority instance per fold.",
    "core_logic": "Why this matters: Random sampling introduces severe variance on imbalanced targets. Stratified K-Fold acts as a variance-reduction technique that guarantees representative sample distributions across all validation rounds, preventing noisy benchmark estimates and training-validation distribution divergence.",
    "architectural_logic": "In enterprise ML training pipelines, StratifiedKFold is combined with Scikit-Learn Pipelines or Imbalanced-Learn Pipelines. Imputer, scaler, and oversampling transformers (like SMOTE) are fitted strictly within the inner training folds of each split, preventing data leakage into holdout folds while preserving class balance.",
    "connected_logic": [
        {
            "title": "Scikit-Learn Automatic Stratification Dispatch",
            "content": "• In Scikit-Learn, passing an integer cv=5 and an estimator into cross_val_score() inspects the model type via is_classifier(estimator).\n• If the estimator is a classifier, Scikit-Learn automatically instantiates StratifiedKFold under the hood, whereas regressors default to standard unstratified KFold."
        },
        {
            "title": "The Minority Count Constraint (N_c ≥ K)",
            "content": "• Mathematical stratification requires allocating at least one minority instance per fold; if a rare class has only 3 examples, running 5-fold CV causes an impossible division (3 < 5).\n• When ultra-rare classes violate N_c >= K, practitioners must either decrease K, consolidate rare classes into an 'Other' bucket, or use Leave-One-Out Cross-Validation (LOOCV)."
        },
        {
            "title": "Stratified Group Hygiene in Clinical EHR Records",
            "content": "• In hospital readmission or oncology datasets, patients have dozens of electronic health records, while the target condition (e.g. septic shock) is rare (< 2%).\n• Standard GroupKFold ignores class distribution and can create validation folds with zero sepsis cases; StratifiedGroupKFold uses a greedy heuristic to balance class prevalence while maintaining strict patient isolation."
        },
        {
            "title": "Pipeline Encapsulation to Prevent Preprocessing Leakage",
            "content": "• Running feature scaling, SMOTE oversampling, or imputation before calling StratifiedKFold contaminates each validation fold with out-of-fold statistics.\n• Production workflows wrap transformers and classifiers inside imblearn.pipeline.Pipeline, guaranteeing that SMOTE oversampling and scaling are fitted exclusively on the (K-1) training folds during each cross-validation step."
        }
    ],
    "key_takeaways": [
        "Classification Gold Standard: Enforces identical class proportions across all K folds, eliminating fold-to-fold class distribution variance.",
        "Automatic Dispatch: Scikit-Learn cross_val_score automatically uses Stratified K-Fold when passed any classification estimator.",
        "Accuracy Trap: Never evaluate imbalanced folds with accuracy; use ROC-AUC, PR-AUC (Average Precision), or F1-Score.",
        "StratifiedGroupKFold Power: The premier cross-validator when dealing with both patient/user grouping and rare target classes simultaneously."
    ],
    "definition_bullets": [
        "Stratified K-Fold: A cross-validation technique that partitions classification data so that every fold contains the same percentage of each class as the complete dataset.",
        "StratifiedGroupKFold: A hybrid cross-validation protocol that prevents entity leakage by keeping groups intact while simultaneously balancing target class ratios."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_stratified_kfold':
            item.update(STRATIFIED_KFOLD_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_stratified_kfold not found in {filepath}")
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
        if item.get('id') == 'concept_stratified_kfold':
            item.update(STRATIFIED_KFOLD_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
