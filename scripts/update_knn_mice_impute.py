import json

KNN_MICE_UPDATE = {
    "def": "Multivariate imputation techniques (KNN and Iterative MICE) predict missing values in an incomplete column using the observed values of all other correlating features in that row, preserving natural covariance and feature relationships.",
    "definition": "Multivariate imputation techniques (KNN and Iterative MICE) predict missing values in an incomplete column using the observed values of all other correlating features in that row, preserving natural covariance and feature relationships.",
    "formula": "$$\\hat{x}_{ij} = \\frac{\\sum_{k \\in \\mathcal{N}_i} \\frac{1}{d(x_i, x_k)} x_{kj}}{\\sum_{k \\in \\mathcal{N}_i} \\frac{1}{d(x_i, x_k)}}, \\quad d(x_i, x_k) = \\sqrt{\\sum_{l \\in \\mathcal{O}_{ik}} (x_{il} - x_{kl})^2}, \\quad x_j^{(t+1)} = f_j\\big(X_{-j}^{(t)}; \\theta_j\\big)$$",
    "formula_explanation": "",
    "logic": "Univariate imputation flattens variance and destroys correlations. KNN averages the most similar geometric rows (requires scaled features), while MICE trains a round-robin chain of regression models to maintain natural real-world dependencies.",
    "example": "Clinical trial records: Predicting a missing blood pressure value using a patient's age, weight, and cholesterol. KNN finds the k most similar patients to average their readings, while MICE models blood pressure directly via chained regression.",
    "simple_summary": "Univariate imputation ignores other columns; Multivariate imputation uses correlating features to predict missing cells. KNN averages the nearest matching rows (scaling is mandatory!), while MICE trains round-robin regression models to preserve true correlations and variance.",
    "core_terms": [
        {
            "term": "Multivariate Imputation",
            "what_is_it": "• An advanced imputation strategy that predicts missing values in one feature using the observed values of all other correlating features in that row.\n• Unlike univariate mean or median fills that collapse feature correlations, multivariate techniques preserve natural real-world dependencies (e.g. predicting missing height using age and weight).",
            "analogy": "A detective reconstructing a missing receipt amount by checking what items were purchased and the customer's typical spending habits, rather than assuming everyone spends exactly $50.",
            "why_it_matters": "Preserves covariance matrices and natural feature interactions, preventing downstream models from suffering from correlation dilution."
        },
        {
            "term": "KNN Imputer & The Mandatory Scaling Rule",
            "what_is_it": "• Identifies the k most geometrically similar rows using Euclidean distance over observed features, imputing missing values via neighbor averaging.\n• Because distance metrics are sensitive to numerical magnitude, failing to scale features causes large columns (e.g. Salary in thousands) to completely drown out smaller columns (e.g. Age in tens).",
            "analogy": "Finding your closest neighbors: if distance is measured in miles for North/South but inches for East/West, you would only ever search along one axis unless you standardize your units.",
            "why_it_matters": "Delivers accurate local neighborhood estimates for clustered tabular data, provided data is strictly scaled with StandardScaler beforehand."
        },
        {
            "term": "Iterative MICE Imputation",
            "what_is_it": "• Multiple Imputation by Chained Equations (MICE) models each incomplete feature as a regression target of all other features in a round-robin cycle.\n• Updates missing values iteratively across multiple passes until predictions stabilize, capturing complex feature dependencies and preserving natural variance.",
            "analogy": "A group of translators iteratively refining a collaborative document: each specialist updates their section based on the latest revisions of the others until the text reads harmoniously.",
            "why_it_matters": "The academic gold standard for clinical trials, tabular machine learning, and statistical modeling where preserving natural variance and correlations is mandatory."
        }
    ],
    "types_header": "Multivariate Imputation Engines & Constraints",
    "types_badge": "Algorithm Comparison",
    "quick_types": [
        {
            "type": "KNN Imputer (Geometric)",
            "definition": "Averages observed values from the k most similar rows based on Euclidean distance. Preserves local non-linear clusters.",
            "looks_like": "KNNImputer(n_neighbors=5)"
        },
        {
            "type": "Iterative MICE Imputer",
            "definition": "Trains a round-robin cycle of regression models predicting each incomplete column from all others. Preserves global covariance.",
            "looks_like": "IterativeImputer(max_iter=10)"
        },
        {
            "type": "Mandatory Pre-KNN Scaling",
            "definition": "Scaling numerical features with StandardScaler or MinMaxScaler is required; otherwise high-magnitude features dwarf distances.",
            "looks_like": "StandardScaler() → KNNImputer()"
        },
        {
            "type": "Multiple Imputation Uncertainty",
            "definition": "MICE generates m multiple completed datasets with stochastic noise to calculate robust standard errors and confidence intervals.",
            "looks_like": "m=5 Imputed Datasets pooled via Rubin's Rules"
        },
        {
            "type": "Train-Only Imputation Pipe",
            "definition": "Fitting the multivariate model strictly on training folds and transforming test sets prevents fatal cross-fold data leakage.",
            "looks_like": "pipeline = make_pipeline(imputer, model)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x̂_ij",
            "meaning": "Imputed Cell Value",
            "plain_english": "Predicted replacement value for missing feature j in row i"
        },
        {
            "symbol": "N_i",
            "meaning": "K-Nearest Neighbors",
            "plain_english": "The set of k most similar rows to row i based on shared observed features"
        },
        {
            "symbol": "d(x_i, x_k)",
            "meaning": "Euclidean Distance",
            "plain_english": "Geometric distance between row i and neighbor k across mutually observed columns"
        },
        {
            "symbol": "O_ik",
            "meaning": "Shared Observed Indices",
            "plain_english": "The subset of feature columns that are non-null in both row i and row k"
        },
        {
            "symbol": "x_j^(t+1)",
            "meaning": "MICE Updated Column",
            "plain_english": "Feature j's updated predictions at iteration t+1 of the chained equations"
        },
        {
            "symbol": "f_j(X_-j; θ)",
            "meaning": "Chained Regression Model",
            "plain_english": "Estimator (e.g. Ridge or Bayesian) predicting column j using all other features"
        }
    ],
    "numerical_example": "KNN Imputation on Scaled Patient Records (k = 2 Neighbors):\nColumns: [Age (scaled), Weight (scaled), Blood Pressure (raw)]\n• Patient 1: [0.20, 0.40, 120]\n• Patient 2: [0.25, 0.45, 125]\n• Patient 3: [0.80, 0.90, 160]\n• Patient Target (Missing BP): [0.22, 0.42, NaN]\n\n1. Calculate Distances across Observed Features (Age, Weight):\n   • Distance to Patient 1: d = √[(0.22 - 0.20)² + (0.42 - 0.40)²] = √[0.0004 + 0.0004] = √0.0008 ≈ 0.028\n   • Distance to Patient 2: d = √[(0.22 - 0.25)² + (0.42 - 0.45)²] = √[0.0009 + 0.0009] = √0.0018 ≈ 0.042\n   • Distance to Patient 3: d = √[(0.22 - 0.80)² + (0.42 - 0.90)²] = √[0.3364 + 0.2304] = √0.5668 ≈ 0.753\n\n2. Select k = 2 Nearest Neighbors:\n   • Neighbors are Patient 1 (d = 0.028) and Patient 2 (d = 0.042).\n\n3. Impute Blood Pressure:\n   • Simple Average: BP = (120 + 125) / 2 = 122.5 mmHg.\n   • Distance-weighted alternative places slightly more influence on Patient 1, estimating ~122.0 mmHg (far more accurate than population mean 135 mmHg!).",
    "pitfalls": "Common Pitfall: Running KNN Imputation without scaling numerical features first. Unscaled columns with wide ranges (e.g. Income $20k-$200k) create massive squared differences that completely drown out small-range columns (e.g. Age 18-80), making distance checks 100% blind to age. Always prepend StandardScaler.",
    "core_logic": "Why this matters: In complex tabular modeling, missing values contain non-random multivariate signals. KNN uses local neighborhood geometry to preserve non-linear clusters, while MICE preserves global covariance matrices and statistical variance, outperforming flat univariate means.",
    "architectural_logic": "In production machine learning pipelines, IterativeImputer (MICE) is preferred for high-value offline model training where accuracy is paramount, whereas KNN is often replaced with precomputed grouped medians in online inference pipelines to avoid O(N²) latency bottlenecks.",
    "connected_logic": [
        {
            "title": "Covariance Preservation: Overcoming Correlation Collapse",
            "content": "• Univariate mean/median imputation replaces missing entries with flat constants, diluting cross-feature covariances Cov(X_i, X_j) toward zero.\n• MICE preserves multivariate relationships by modeling features conditionally, ensuring downstream tree splits and regression coefficients retain natural correlation slopes."
        },
        {
            "title": "The O(N²) Computational Bottleneck in KNN Imputation",
            "content": "• KNN Imputer performs pairwise distance calculations across all rows, scaling quadratically with sample size (O(N² · d)).\n• On datasets exceeding 100,000 rows, KNN causes severe memory thrashing and slow pipeline runtimes, making MICE or grouped medians the pragmatic production choice."
        },
        {
            "title": "Chained Equation Convergence & Iteration Limits",
            "content": "• MICE cycles sequentially through features; early passes use rough mean initializations that gradually refine into stable conditional distributions.\n• Most tabular datasets reach empirical convergence within 10 to 15 iterations; adding early-stopping tolerances prevents excessive training delays."
        },
        {
            "title": "Cross-Validation Pipeline Encapsulation",
            "content": "• Fitting KNN or MICE on the entire dataset prior to K-Fold cross-validation leaks validation target relationships into training folds.\n• Production pipelines encapsulate multivariate imputers directly inside Scikit-Learn Pipeline objects, guaranteeing that imputer weights fit strictly within training folds."
        }
    ],
    "key_takeaways": [
        "Core Distinction: Univariate imputation ignores other columns; Multivariate imputation (KNN, MICE) predicts missing cells using correlations.",
        "Scaling Prerequisite: KNN relies strictly on geometric distance; failing to scale features completely blinds the algorithm to smaller-range columns.",
        "Covariance Gold Standard: MICE round-robin regressions preserve natural inter-feature correlations and real-world variance.",
        "Complexity Tradeoff: KNN scales at O(N²) and slows on big data; MICE scales with iteration passes and suits complex clinical/tabular datasets."
    ],
    "definition_bullets": [
        "KNN Imputation: A distance-based technique replacing missing entries with the average of the k closest matching rows across observed features.",
        "MICE Imputation: Multiple Imputation by Chained Equations, an iterative algorithm modeling each missing feature as a function of all other features."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_knn_mice_impute':
            item.update(KNN_MICE_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_knn_mice_impute not found in {filepath}")
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
        if item.get('id') == 'concept_knn_mice_impute':
            item.update(KNN_MICE_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
