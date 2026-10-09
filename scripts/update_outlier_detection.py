import json

OUTLIER_DETECTION_UPDATE = {
    "def": "Outliers are data points that deviate drastically from the rest of the observations. Detecting them prevents model weight corruption in sensitive algorithms (regression, K-Means) while isolating critical real-world signals like fraud and cyberattacks.",
    "definition": "Outliers are data points that deviate drastically from the rest of the observations. Detecting them prevents model weight corruption in sensitive algorithms (regression, K-Means) while isolating critical real-world signals like fraud and cyberattacks.",
    "formula": "$$\\text{IQR} = Q_3 - Q_1, \\quad \\text{Fence} = [Q_1 - 1.5 \\cdot \\text{IQR}, \\; Q_3 + 1.5 \\cdot \\text{IQR}], \\quad M_i = \\frac{0.6745 \\cdot (x_i - \\tilde{x})}{\\text{MAD}}$$",
    "formula_explanation": "",
    "logic": "Linear models and distance metrics break easily when outliers warp slopes and pull centroids. Statistical bounds (IQR, Modified Z-score) and unsupervised Isolation Forests identify anomalies across single and multiple dimensions.",
    "example": "Transaction monitoring: In a batch with median $23.50 and IQR $12, a $120 charge exceeds Tukey's upper fence ($48) and is flagged by IQR. In multi-feature space, Isolation Forest catches a 16-year-old with a $500k mortgage that univariate tests miss.",
    "simple_summary": "Outliers are extreme observations that warp linear models and K-Means, though decision trees tolerate them easily. IQR sets robust quartile fences, Modified Z-Score uses median MAD to avoid masking, and Isolation Forest isolates multi-dimensional anomalies via short tree paths.",
    "core_terms": [
        {
            "term": "IQR Rule & Tukey's Fences",
            "what_is_it": "• A non-parametric statistical method that measures the spread of the middle 50% of data: IQR = Q₃ - Q₁.\n• Sets boundaries at [Q₁ - 1.5×IQR, Q₃ + 1.5×IQR], flagging any point outside these fences without assuming a normal bell curve.",
            "analogy": "Exam grading: ignoring the top 25% and bottom 25% to focus on the core middle class score, drawing protective fences around typical performance.",
            "why_it_matters": "The gold standard for quick, robust univariate outlier filtering on skewed real-world distributions like income, house prices, and transaction sizes."
        },
        {
            "term": "Z-Score & Modified Z-Score (MAD)",
            "what_is_it": "• Standard Z-score measures how many standard deviations a point sits from the mean: Z = (x - μ) / σ, flagging points where |Z| > 3.0.\n• The Modified Z-Score replaces fragile mean and standard deviation with median and Median Absolute Deviation (MAD), preventing extreme outliers from masking themselves.",
            "analogy": "A height inspector: if someone is 7'8\", a standard ruler gets warped by their extreme height, whereas a median-based ruler stays anchored and catches the anomaly.",
            "why_it_matters": "Essential for identifying deviations in approximately Gaussian distributions (sensor readings, manufacturing tolerances, biological metrics)."
        },
        {
            "term": "Isolation Forest (iForest)",
            "what_is_it": "• An unsupervised ensemble tree algorithm that isolates anomalies rather than profiling normal data patterns.\n• Cuts randomly across features; because outliers reside in sparse peripheral regions, they require very few recursive cuts (short tree path lengths) to isolate.",
            "analogy": "Separating sheep in a field: sheep clustered together take dozens of fences to isolate individually, while a lone wolf far off in the meadow is isolated with a single fence.",
            "why_it_matters": "The premier algorithm for multivariate anomaly detection (fraud, cyberattacks, server telemetry) where anomalies only appear across feature interactions."
        }
    ],
    "types_header": "Outlier Detectors & Remediation Strategies",
    "types_badge": "Anomaly Tooling",
    "quick_types": [
        {
            "type": "IQR Tukey Fences",
            "definition": "Non-parametric quartile thresholds [Q₁ - 1.5×IQR, Q₃ + 1.5×IQR]. Best for univariate, skewed distributions.",
            "looks_like": "Tukey Fences: Outside [Q₁ - 1.5·IQR, Q₃ + 1.5·IQR]"
        },
        {
            "type": "Modified Z-Score (MAD)",
            "definition": "Replaces mean with median and standard deviation with MAD. Flags points where |Mᵢ| > 3.5 without distortion.",
            "looks_like": "Mᵢ = 0.6745 · (xᵢ - Median) / MAD > 3.5"
        },
        {
            "type": "Isolation Forest (iForest)",
            "definition": "Unsupervised decision tree ensemble identifying anomalies via short recursive isolation path lengths in multi-dimensional space.",
            "looks_like": "Anomaly Score: Short tree depth = Outlier"
        },
        {
            "type": "Winsorization (Capping)",
            "definition": "Caps extreme legitimate data at fixed percentiles (e.g. clipping all values above 99th percentile to the 99th percentile value).",
            "looks_like": "np.clip(df['val'], lower_1st, upper_99th)"
        },
        {
            "type": "Log Compression",
            "definition": "Applies log(x + 1) to right-skewed positive data, compressing extreme long tails and stabilizing variance.",
            "looks_like": "y_clean = np.log1p(x_raw)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "IQR",
            "meaning": "Interquartile Range",
            "plain_english": "Spread of the middle 50% of sorted data points (Q₃ minus Q₁)"
        },
        {
            "symbol": "Q_1, Q_3",
            "meaning": "25th & 75th Percentiles",
            "plain_english": "Cutoffs separating the lowest and highest quarters of observations"
        },
        {
            "symbol": "M_i",
            "meaning": "Modified Z-Score",
            "plain_english": "Robust deviation score based on median and MAD rather than mean and variance"
        },
        {
            "symbol": "x̃ (x-tilde)",
            "meaning": "Sample Median",
            "plain_english": "The middle value (50th percentile) unaffected by extreme values"
        },
        {
            "symbol": "MAD",
            "meaning": "Median Absolute Deviation",
            "plain_english": "Median of the absolute differences from the sample median: median(|xᵢ - x̃|)"
        },
        {
            "symbol": "Fence",
            "meaning": "Tukey's Boundaries",
            "plain_english": "Inner threshold range beyond which observations are flagged as outliers"
        }
    ],
    "numerical_example": "Detecting Outliers in Transaction Amounts:\nSorted Dataset: [12, 15, 18, 20, 22, 25, 28, 30, 32, 120] (N = 10 transactions in dollars)\n\n1. Quartile & IQR Calculation:\n   • Q₁ (25th percentile) = 18, Median Q₂ = 23.5, Q₃ (75th percentile) = 30\n   • IQR = Q₃ - Q₁ = 30 - 18 = 12\n\n2. Establishing Tukey's Fences:\n   • Lower Fence = Q₁ - 1.5 × IQR = 18 - 1.5(12) = 18 - 18 = $0\n   • Upper Fence = Q₃ + 1.5 × IQR = 30 + 1.5(12) = 30 + 18 = $48\n\n3. Outlier Evaluation:\n   • Values between $0 and $48 are considered inliers.\n   • The $120 transaction exceeds the upper fence ($120 > $48) and is flagged as an IQR outlier!\n\n4. Z-Score Masking Comparison:\n   • Mean μ = 32.2, Std Dev σ ≈ 31.4\n   • Z-score for 120 = (120 - 32.2) / 31.4 = 2.80 (Under |Z| < 3.0 threshold! The single 120 value pulled the mean up and inflated σ, masking itself, whereas IQR easily caught it).",
    "pitfalls": "Common Pitfall: Automatically dropping all detected outliers. In fraud detection, cyber defense, or medical diagnosis, outliers represent the highest-value predictive signals. Only delete proven corrupted data (e.g. negative age); otherwise apply Winsorization capping or log transforms.",
    "core_logic": "Why this matters: Mean Squared Error squares residual errors, granting extreme outliers enormous leverage over gradient updates in linear models and neural networks. Robust estimators and tree-based isolation protect optimization dynamics from catastrophic distortion.",
    "architectural_logic": "In enterprise ML pipelines, outlier detection is deployed both during ETL preprocessing (to cleanse training sets) and during production inference (serving as an out-of-distribution detector to alert engineers when incoming live payloads deviate from training boundaries).",
    "connected_logic": [
        {
            "title": "Algorithm Sensitivity: Fragile Models vs. Tree Immunity",
            "content": "• Linear regression, neural networks, and K-Means squared-loss models are heavily disrupted by outliers, warping decision boundaries and pulling cluster centers.\n• Tree-based architectures (Random Forests, XGBoost, LightGBM) are completely immune to monotonic scale shifts because splits only evaluate rank orderings."
        },
        {
            "title": "The Masking Effect: Why Mean & Standard Deviation Fail",
            "content": "• Extreme outliers pull the sample mean μ toward themselves and artificially inflate variance σ², lowering their own calculated Z-score.\n• In heavily skewed distributions (wealth, network traffic), standard Z-scores fail to flag genuine anomalies while falsely flagging valid high-volume observations."
        },
        {
            "title": "Multivariate Anomaly Traps: Why Univariate Filters Miss Fraud",
            "content": "• A 16-year-old individual is normal, and holding a $500,000 mortgage is normal; however, a 16-year-old holding a $500,000 mortgage is a massive anomaly.\n• Univariate tests (IQR, Z-score) evaluate features in isolation and miss joint anomalies, requiring multi-dimensional estimators like Isolation Forest."
        },
        {
            "title": "The Outlier Treatment Flowchart: Drop vs. Winsorize vs. Transform",
            "content": "• Corrupted noise (e.g. human age = -5 or 999) should be dropped or imputed, but genuine extremes (millionaire bank transactions) must be preserved.\n• Legitimate extremes should be Winsorized at the 1st/99th percentiles or compressed via log transforms, preserving real predictive signal without destabilizing weights."
        }
    ],
    "key_takeaways": [
        "Core Concept: Outliers can represent fatal data corruption (sensor errors) or high-value signals (fraud, security breaches).",
        "Technique Selection: Use IQR for skewed univariate checks, Modified Z-Score for Gaussian data, and Isolation Forest for multidimensional features.",
        "Model Impact: Destroys linear models, K-Means, and neural networks, while tree-based models (XGBoost) remain naturally robust.",
        "Treatment Rule: Never auto-delete outliers; distinguish between bad data (drop/impute) and real extremes (Winsorize/log-transform)."
    ],
    "definition_bullets": [
        "IQR Rule: A quartile-based filtering technique establishing bounds at 1.5 times the interquartile range from Q1 and Q3.",
        "Isolation Forest: An unsupervised ensemble model that isolates anomalies via shallow tree path lengths in high-dimensional feature spaces."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_outlier_detection':
            item.update(OUTLIER_DETECTION_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_outlier_detection not found in {filepath}")
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
        if item.get('id') == 'concept_outlier_detection':
            item.update(OUTLIER_DETECTION_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
