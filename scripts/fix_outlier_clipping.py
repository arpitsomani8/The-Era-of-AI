import json

OUTLIER_CLIPPING_REFINED = {
    "def": "Outlier clipping means setting values outside chosen limits to the nearest limit, rather than deleting the records. Winsorization is a form of clipping where those limits are chosen using percentiles (such as the 1st and 99th percentiles).",
    "definition": "Outlier clipping means setting values outside chosen limits to the nearest limit, rather than deleting the records. Winsorization is a form of clipping where those limits are chosen using percentiles (such as the 1st and 99th percentiles).",
    "formula": "$$x_{\\text{clipped}} = \\min(\\max(x, L), U) = \\begin{cases} L & \\text{if } x < L \\\\ x & \\text{if } L \\le x \\le U \\\\ U & \\text{if } x > U \\end{cases}, \\quad L = P_{\\alpha}, \\quad U = P_{1 - \\alpha}$$",
    "formula_explanation": "",
    "logic": "Extreme outliers exert excessive leverage on regression lines and destabilize gradient updates. Rather than deleting rows (trimming) and discarding valuable accompanying features, clipping pulls extreme values inward to specified percentile or statistical fences, stabilizing mean and variance while keeping sample size 100% intact.",
    "example": "E-commerce checkout: A single B2B bulk purchase of $50,000 in a retail dataset with median $50. Rather than deleting the customer record, 99th-percentile Winsorization caps the order value at $500, preserving the customer's age, location, and browsing history without wrecking model gradients.",
    "simple_summary": "Instead of throwing away rows with extreme numbers (trimming), Outlier Clipping caps them at fixed limits. Winsorization is simply clipping using percentiles (like the 1st% and 99th%). This protects your model from extreme spikes while keeping 100% of your data rows and all their other columns.",
    "core_terms": [
        {
            "term": "Outlier Clipping (Capping / Clamping)",
            "what_is_it": "• Setting any value that falls outside your chosen lower and upper limits to the nearest boundary, instead of deleting the row.\n• If a number is too small (below lower limit L), it is pulled up to L; if it is too big (above upper limit U), it is capped down to U.",
            "analogy": "A speed limiter on an electric scooter: no matter how hard you push the throttle downhill, your speed is capped at 25 km/h.",
            "why_it_matters": "Protects machine learning models from wild numerical spikes without throwing away the rest of the customer or patient record."
        },
        {
            "term": "Winsorization (Percentile-Based Capping)",
            "what_is_it": "• A simple, automated way to clip data using percentiles (most commonly the 1st percentile at the bottom and the 99th percentile at the top).\n• Any number in the top 1% gets capped down to the 99th percentile value, and any number in the bottom 1% gets pulled up to the 1st percentile value.",
            "analogy": "In a class test where one student scores 500 bonus points while everyone else gets under 100, the teacher caps the top score at 98 so the class curve isn't ruined.",
            "why_it_matters": "You don't have to guess manual limits—the dataset's own percentiles automatically pick fair, clean boundaries for you."
        },
        {
            "term": "Trimming vs. Winsorizing (Delete vs. Keep)",
            "what_is_it": "• Trimming completely deletes the outlier rows from your dataset, making your table smaller and throwing away all other columns in that row.\n• Winsorizing keeps every single row, only adjusting the extreme number so you preserve 100% of your data and feature relationships.",
            "analogy": "Trimming is throwing out an entire apple because of one small bruised spot; Winsorizing is slicing off the bruised tip and keeping the rest of the good apple.",
            "why_it_matters": "Stops unnecessary data loss—if a customer spent $50,000, you don't want to discard their age, location, and account history just because of one big order!"
        }
    ],
    "types_header": "Clipping Techniques & Boundary Selection",
    "types_badge": "Tail Management",
    "quick_types": [
        {
            "type": "Pandas Series.clip(lower, upper)",
            "definition": "Vectorized method in Pandas bounding column series between defined numerical lower and upper limits.",
            "looks_like": "df['age'] = df['age'].clip(lower=0, upper=105)"
        },
        {
            "type": "Scipy mstats.winsorize",
            "definition": "Percentile-based Winsorizer setting lower and upper probability cutoff fractions (e.g. top and bottom 1%).",
            "looks_like": "scipy.stats.mstats.winsorize(X, limits=[0.01, 0.01])"
        },
        {
            "type": "Tukey IQR Clipping Fences",
            "definition": "Non-parametric bounds derived from quartiles: lower = Q1 - 1.5·IQR, upper = Q3 + 1.5·IQR.",
            "looks_like": "df['fare'].clip(lower=Q1 - 1.5*IQR, upper=Q3 + 1.5*IQR)"
        },
        {
            "type": "Z-Score Standard Deviation Capping",
            "definition": "Parametric bounds capping observations that fall outside 3 standard deviations: [μ - 3σ, μ + 3σ].",
            "looks_like": "df['metric'].clip(lower=mu - 3*std, upper=mu + 3*std)"
        },
        {
            "type": "Domain Physics & Business Caps",
            "definition": "Hard limits defined by physical sensor constraints, percentage boundaries [0, 100], or legal rules.",
            "looks_like": "df['pct_score'].clip(lower=0.0, upper=100.0)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x_clipped",
            "meaning": "Clipped Output Value",
            "plain_english": "The capped observation constrained strictly within the lower and upper limits [L, U]"
        },
        {
            "symbol": "x",
            "meaning": "Original Observation",
            "plain_english": "The raw unconstrained input feature measurement"
        },
        {
            "symbol": "L",
            "meaning": "Lower Bound",
            "plain_english": "Lower clipping fence, often empirical percentile P_alpha or Tukey fence"
        },
        {
            "symbol": "U",
            "meaning": "Upper Bound",
            "plain_english": "Upper clipping fence, often empirical percentile P_1-alpha or domain max"
        },
        {
            "symbol": "P_α (P_alpha)",
            "meaning": "Lower Percentile Cutoff",
            "plain_english": "Lower threshold percentile (e.g. 1st or 5th percentile calculated on training fold)"
        },
        {
            "symbol": "P_{1-α}",
            "meaning": "Upper Percentile Cutoff",
            "plain_english": "Upper threshold percentile (e.g. 99th or 95th percentile calculated on training fold)"
        }
    ],
    "numerical_example": "Web E-Commerce Checkout Basket Totals ($) across 10 customers:\nRaw transactions: [$12, $25, $38, $45, $50, $60, $75, $90, $110, $5,000]\nNotice the extreme outlier ($5,000) from a wholesale buyer.\n\n1. Calculate 90% Winsorization Fences (5th and 95th percentiles):\n   • Lower Floor L (5th percentile): $15\n   • Upper Ceiling U (95th percentile): $105\n\n2. Apply Piecewise Clipping Function (x_clipped = min(max(x, L), U)):\n   • Customer 1 ($12 < L=15): x_clipped = L = $15\n   • Customer 2 ($25 between 15 and 105): x_clipped = $25\n   • Customer 5 ($50 between 15 and 105): x_clipped = $50\n   • Customer 9 ($110 > U=105): x_clipped = U = $105\n   • Customer 10 ($5,000 > U=105): x_clipped = U = $105\n\n3. Distribution Impact:\n   • Unclipped Mean: ($12 + ... + $5,000) / 10 = $550.50 (completely distorted by one user!)\n   • Clipped Mean: ($15 + $25 + $38 + $45 + $50 + $60 + $75 + $90 + $105 + $105) / 10 = $60.80 (accurate representation of typical customer purchasing power).\n   • Sample size N remains 10 (no customer data lost).",
    "pitfalls": "Common Pitfall: Computing clipping percentiles dynamically on test or validation splits instead of applying the fixed training set thresholds. If a small test batch has a lower 99th percentile than the training set, dynamic capping alters the definition of the feature space, introducing test-time data drift. Always compute L and U strictly on training data.",
    "core_logic": "Why this matters: In machine learning models with gradient updates or squared-error loss functions, extreme outliers exert disproportionate leverage on parameter estimates. Clipping stabilizes distribution moments (mean, variance) without the information destruction caused by deleting entire records.",
    "architectural_logic": "In enterprise ML engineering, clipping bounds (L, U) are computed on the training partition and compiled into custom Scikit-Learn FunctionTransformers or Feature Store pipelines, ensuring identical capping boundaries during batch scoring and low-latency REST API inference.",
    "connected_logic": [
        {
            "title": "High-Leverage Points & Ordinary Least Squares (OLS)",
            "content": "• In linear regression, outliers far out in feature space exert extreme leverage (h_ii = x_i (X^T X)^(-1) x_i^T), pivoting the regression slope dramatically toward themselves.\n• Winsorizing caps extreme coordinates at fence thresholds, limiting maximum Cook's distance leverage and preventing a single whale customer from dictating global model weights."
        },
        {
            "title": "Preserving Multi-Attribute Signals vs. Destructive Trimming",
            "content": "• When an extreme event occurs (e.g. a fraudulent credit card transaction of $50,000), trimming removes the entire row, throwing away crucial fraud signals in merchant ID, IP geolocation, and time of day.\n• Clipping retains the entire observation row and all accompanying attributes, acknowledging that the transaction was maximally large without destabilizing numerical variance."
        },
        {
            "title": "Boundary Spike Artifacts in Tree-Based Models vs. Linear Models",
            "content": "• Clipping piles extreme values directly onto boundary values L and U, creating sharp point-mass probability spikes at the cutoffs.\n• While linear models benefit from stabilized gradients, tree-based models (XGBoost, LightGBM) easily detect these boundary spikes and can construct dedicated split thresholds at x = U to isolate clipped populations."
        },
        {
            "title": "Strict Train-Test Pipeline Encapsulation",
            "content": "• Calculating clipping percentiles (such as P_99) on the entire dataset leaks future test distribution bounds into the training phase.\n• In production ML pipelines, threshold limits (L, U) are fitted strictly on the training partition and saved within the transformation pipeline to clip validation, test, and live inference payloads identically."
        }
    ],
    "key_takeaways": [
        "Row Preservation: Winsorization caps values at boundary limits rather than deleting rows, maintaining 100% of sample size N and preserving correlating features.",
        "Moment Stabilization: Pulls extreme outliers inward, instantly stabilizing empirical mean and variance against high-leverage distortions.",
        "Boundary Point Masses: Creates point-mass frequency spikes at limits L and U, which tree models readily isolate through threshold splits.",
        "Training Encapsulation: Thresholds L and U must be derived strictly from training folds to prevent data leakage during inference."
    ],
    "definition_bullets": [
        "Outlier Clipping: Setting numbers that are too high or too low to the nearest boundary limit, keeping the record intact.",
        "Winsorization: A specific type of clipping that uses fixed percentiles (such as the 1st and 99th percentiles) as the boundaries."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_outlier_clipping':
            item.update(OUTLIER_CLIPPING_REFINED)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_outlier_clipping not found in {filepath}")
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
        if item.get('id') == 'concept_outlier_clipping':
            item.update(OUTLIER_CLIPPING_REFINED)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
