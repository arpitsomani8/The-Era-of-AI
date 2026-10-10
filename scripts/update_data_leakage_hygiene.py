import json

DATA_LEAKAGE_HYGIENE_UPDATE = {
    "def": "Train, Val & Test Hygiene refers to the strict protocol of isolating dataset partitions to prevent Data Leakage—the catastrophic error where information outside the training set influences model training, producing deceptively high test scores that collapse in production.",
    "definition": "Train, Val & Test Hygiene refers to the strict protocol of isolating dataset partitions to prevent Data Leakage—the catastrophic error where information outside the training set influences model training, producing deceptively high test scores that collapse in production.",
    "formula": "$$\\mathcal{D}_{\\text{train}} \\cap \\mathcal{D}_{\\text{test}} = \\emptyset, \\quad \\theta_{\\text{pre}} = \\text{Fit}(\\mathcal{D}_{\\text{train}}), \\quad \\tilde{\\mathbf{X}}_{\\text{test}} = \\text{Transform}(\\mathcal{D}_{\\text{test}}; \\theta_{\\text{pre}})$$",
    "formula_explanation": "",
    "logic": "Data leakage occurs when a model has access to data during training that would not be available at inference time. Fitting scalers, imputers, or encoders on the full dataset before splitting leaks holdout distribution statistics. Bundling preprocessing inside Scikit-Learn Pipeline ensures all transformations are fit strictly on training splits.",
    "example": "Medical imaging diagnosis: If a patient has 5 chest X-rays and they are split randomly across train and test sets, the neural network memorizes the patient's individual rib cage and pacemaker rather than detecting pneumonia. Enforcing patient-level GroupKFold hygiene ensures models learn disease pathology.",
    "simple_summary": "Data leakage is like giving a student the exam questions before the test—they get a 100% in school, but fail completely in the real world. To prevent it, always split your data first before touching any scaler or imputer. Fit your transformations strictly on the training set, and bundle everything into a Scikit-Learn Pipeline so cross-validation never leaks.",
    "core_terms": [
        {
            "term": "Data Leakage (The Phantom Accuracy Trap)",
            "what_is_it": "• The fatal machine learning defect where information from outside the training dataset (such as test labels, future timestamps, or global distribution statistics) contaminates the model training process.\n• Creates an illusion of near-perfect accuracy on evaluation benchmarks that completely collapses when the model is deployed to real-world production users.",
            "analogy": "Giving a student the actual exam questions and answer key to study the night before the test: they score 100% on the exam, but fail completely when faced with new problems in the real world.",
            "why_it_matters": "The number one cause of production ML failure; models that look brilliant in Jupyter notebooks fail silently or catastrophically upon live deployment."
        },
        {
            "term": "The 4 Types of Data Leakage",
            "what_is_it": "• Preprocessing Leakage: Computing scalers, imputers, or encoders on the full dataset before splitting.\n• Temporal / Lookahead Leakage: Shuffling time-series data so future information leaks into the past.\n• Group / Entity Leakage: Splitting records from the same customer or patient across both train and test partitions.\n• Target Leakage: Including features that are created only after the prediction event has already occurred (e.g. 'Sent to Collections' predicting loan default).",
            "analogy": "A time-travel paradox: reading tomorrow's newspaper to place bets on today's football match, or diagnosing an illness by checking if the doctor already prescribed the cure.",
            "why_it_matters": "Provides engineers with an exhaustive audit checklist to inspect feature stores, data extraction queries, and preprocessing DAGs before training."
        },
        {
            "term": "Atomic Pipelines (The Leak-Proof Architecture)",
            "what_is_it": "• Encapsulating all preprocessing steps (imputers, encoders, scalers) and the estimator inside a single unified Scikit-Learn Pipeline object.\n• Guarantees that during K-Fold Cross-Validation, transformers are fit strictly on the training partition of each fold and applied to validation splits without ever seeing validation statistics.",
            "analogy": "A sterile surgical airlock: tools and samples are sealed inside an airtight containment chamber, ensuring outside germs can never contaminate the operation.",
            "why_it_matters": "Makes data leakage physically impossible in code, turning messy multi-step scripts into robust, reproducible production pipelines."
        }
    ],
    "types_header": "Validation Splitters & Hygiene Guards",
    "types_badge": "Partitioning Protocols",
    "quick_types": [
        {
            "type": "Scikit-Learn Pipeline",
            "definition": "Combines preprocessing transformers and model into a single atomic estimator, preventing fold leakage.",
            "looks_like": "make_pipeline(StandardScaler(), LogisticRegression())"
        },
        {
            "type": "TimeSeriesSplit (Chronological)",
            "definition": "Expanding-window validator that strictly trains on past records to predict future folds without time travel.",
            "looks_like": "TimeSeriesSplit(n_splits=5)"
        },
        {
            "type": "GroupKFold (Entity Isolation)",
            "definition": "Cross-validator ensuring all records from the same group/patient reside in either train or test, never both.",
            "looks_like": "GroupKFold(n_splits=5).split(X, y, groups=patient_id)"
        },
        {
            "type": "StratifiedKFold (Class Balance)",
            "definition": "Cross-validator maintaining identical target class ratios across every training and validation fold.",
            "looks_like": "StratifiedKFold(n_splits=5, shuffle=True, random_state=42)"
        },
        {
            "type": "Target Leakage Audit",
            "definition": "Verifying that all feature timestamps strictly precede the prediction event time in the production ingestion DAG.",
            "looks_like": "assert feature_timestamp <= event_timestamp"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "D_train",
            "meaning": "Training Partition",
            "plain_english": "The dedicated training subset used strictly to learn model parameters and preprocessing statistics"
        },
        {
            "symbol": "D_test",
            "meaning": "Holdout Test Partition",
            "plain_english": "The strictly isolated evaluation set simulating unseen future deployment data"
        },
        {
            "symbol": "∅ (empty set)",
            "meaning": "Zero Overlap Constraint",
            "plain_english": "The formal hygiene guarantee that no sample, identity, or future timestamp crosses partitions"
        },
        {
            "symbol": "θ_pre (theta_pre)",
            "meaning": "Learned Preprocessing Parameters",
            "plain_english": "Fitted scaling, imputation, or encoding parameters computed exclusively on D_train"
        },
        {
            "symbol": "X̃_test (X_tilde_test)",
            "meaning": "Transformed Test Features",
            "plain_english": "Test data transformed using parameters θ_pre without fitting on test statistics"
        }
    ],
    "numerical_example": "Preprocessing Leakage Demo on a 5-Sample Dataset:\nRaw continuous values: [10, 20, 30, 40, 100]\nPartition: Train = [10, 20, 30] (N_train = 3), Test = [40, 100] (N_test = 2)\n\n1. The Leaky Mistake (Fit Before Split):\n   • Global Mean: μ_global = (10 + 20 + 30 + 40 + 100) / 5 = 200 / 5 = 40.0\n   • Global Std: σ_global = √[((10-40)² + ... + (100-40)²) / 5] ≈ 32.25\n   • Transformed Train Sample 1 (10): (10 - 40) / 32.25 = -0.93\n   (LEAKAGE! The training sample was artificially shifted because the test outlier 100 pulled the mean to 40.0!).\n\n2. The Correct Protocol (Split First, Fit Strictly on Train):\n   • Train Mean: μ_train = (10 + 20 + 30) / 3 = 60 / 3 = 20.0\n   • Train Std: σ_train = √[((10-20)² + (20-20)² + (30-20)²) / 3] = √[200/3] ≈ 8.165\n   • Transformed Train Samples:\n     - Sample 1 (10): (10 - 20) / 8.165 = -1.22\n     - Sample 2 (20): (20 - 20) / 8.165 = 0.00\n     - Sample 3 (30): (30 - 20) / 8.165 = +1.22\n   • Transformed Test Samples (Using θ_pre = {μ_train=20.0, σ_train=8.165}):\n     - Sample 4 (40): (40 - 20) / 8.165 = +2.45\n     - Sample 5 (100): (100 - 20) / 8.165 = +9.80\n\nOutcome: The training phase remained 100% blind to test data distributions, producing honest, leak-free evaluations.",
    "pitfalls": "Common Pitfall: Scaling or imputing the entire dataset prior to cross-validation. When you execute scaler.fit_transform(X) and then call cross_val_score(cv=5), all 5 validation folds were already used to calculate the mean and variance, creating subtle preprocessing leakage. Always bundle preprocessing inside a Scikit-Learn Pipeline so transformations refit strictly within each inner fold.",
    "core_logic": "Why this matters: An ML model is only as credible as its evaluation hygiene. Leaking test information produces inflated validation benchmarks that conceal overfitting. Enforcing strict partition isolation ensures that model metrics faithfully predict real-world production performance.",
    "architectural_logic": "In production enterprise feature stores (e.g. Feast, Tecton) and CI/CD pipelines, feature values are joined using point-in-time 'as-of' timestamp logic to eliminate lookahead leakage. Modeling workflows encapsulate all transformations inside Scikit-Learn Pipelines or MLflow recipes, guaranteeing zero data contamination between training folds and live inference.",
    "connected_logic": [
        {
            "title": "Target Leakage in Fraud & Credit Underwriting",
            "content": "• In loan default prediction, incorporating columns like 'Account Sent to Collections' or 'Late Notice Timestamp' produces 99.9% AUC because these actions only occur after the borrower defaults.\n• High-performing real-world risk systems enforce strict feature availability SLAs, querying feature stores strictly with as_of(event_timestamp) point-in-time joins to eliminate retrospective hindsight."
        },
        {
            "title": "Group & Entity Leakage in Clinical Imaging",
            "content": "• In medical AI (e.g. chest X-ray pneumonia detection), patients often have multiple scans taken across consecutive days.\n• If a patient's scans are split randomly across train and test sets, the convolutional network memorizes specific patient anatomy (bone density, jewelry, pacemaker shape) rather than pathology; GroupKFold enforces patient-level isolation."
        },
        {
            "title": "Lookahead Leakage in Financial Time-Series Forecasting",
            "content": "• Financial time-series models evaluated with standard randomized train_test_split() use future stock prices to predict past trends, producing completely fictitious trading profits.\n• Production algorithmic trading platforms enforce walk-forward cross-validation (TimeSeriesSplit), ensuring that training data strictly precedes test periods with an optional embargo buffer to avoid auto-correlation leakage."
        },
        {
            "title": "Atomic Pipeline Integration with Hyperparameter Search",
            "content": "• When tuning hyperparameters with GridSearchCV or Optuna, running preprocessing outside the cross-validation loop leaks validation fold distributions into tuning decisions.\n• Wrapping ColumnTransformer and the estimator in an atomic Pipeline guarantees that every search iteration refits imputation, scaling, and encoding from scratch on each inner training split."
        }
    ],
    "key_takeaways": [
        "Three Distinct Roles: Train fits parameters; Validation tunes hyperparameters; Test provides final, untouched generalization audit.",
        "Split-First Mandate: Always split raw data into partitions before executing any scaler, imputer, or feature-selection transformer.",
        "The 4 Leakage Vectors: Guard against Preprocessing leakage, Temporal lookahead, Group identity leakage, and retrospective Target leakage.",
        "Pipeline Protection: Packaging transformations inside Scikit-Learn Pipeline makes cross-validation leakage physically impossible."
    ],
    "definition_bullets": [
        "Data Leakage: The introduction of invalid information from outside the training dataset into the model training pipeline, creating falsely optimistic evaluations.",
        "Partition Hygiene: The rigorous isolation of training, validation, and holdout datasets across all preprocessing, feature extraction, and modeling steps."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_data_leakage_hygiene':
            item.update(DATA_LEAKAGE_HYGIENE_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_data_leakage_hygiene not found in {filepath}")
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
        if item.get('id') == 'concept_data_leakage_hygiene':
            item.update(DATA_LEAKAGE_HYGIENE_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
