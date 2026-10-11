import json

BINNING_UPDATE = {
    "def": "Binning & Bucketing (Feature Discretization) converts continuous numerical variables into discrete intervals or buckets, enabling linear models to capture non-linear patterns, suppressing micro-noise, and neutralizing extreme outliers.",
    "definition": "Binning & Bucketing (Feature Discretization) converts continuous numerical variables into discrete intervals or buckets, enabling linear models to capture non-linear patterns, suppressing micro-noise, and neutralizing extreme outliers.",
    "formula": "$$w = \\frac{\\max(x) - \\min(x)}{K}, \\quad b(x) = k \\iff t_k \\le x < t_{k+1}, \\quad t_k = \\min(x) + k \\cdot w$$",
    "formula_explanation": "",
    "logic": "Continuous features force linear models into a single straight slope. Binning chops continuous features into discrete categories, allowing models to learn independent step weights for each interval (capturing U-shaped relationships) while absorbing extreme outliers into broad top-end buckets.",
    "example": "Credit scoring & age: Rather than assuming default risk changes linearly with every single birthday, age is binned into [18-25, 26-35, 36-50, 51-65, 65+]. This lets a logistic regression model learn that 18-25 and 65+ have different risk profiles without forcing a rigid straight line across all ages.",
    "simple_summary": "Binning (or bucketing) groups continuous numbers into categories or brackets, like turning exact ages into brackets (18–25, 26–35). This allows simple linear models to learn complex, curvy relationships and stops extreme outliers from throwing off predictions. However, it permanently throws away fine details and creates artificial boundary cliffs.",
    "core_terms": [
        {
            "term": "Binning & Bucketing (Feature Discretization)",
            "what_is_it": "• The process of converting smooth continuous numerical values into discrete intervals, brackets, or categories.\n• Turns exact numbers (like age 23, 27, 34) into bracketed groups (like '18–25' and '26–35'), allowing models to treat distinct numerical ranges as independent categorical states.",
            "analogy": "Sizing clothing into Small, Medium, and Large instead of tailoring every single shirt down to the exact millimeter.",
            "why_it_matters": "Enables simple linear models to learn complex non-linear curves (like U-shaped patterns) and suppresses noisy micro-fluctuations in sensor or market data."
        },
        {
            "term": "Equal-Width vs. Equal-Frequency (Quantile) Bins",
            "what_is_it": "• Equal-Width divides the numerical distance between min and max into equal spans (e.g. every $10,000), but can leave empty buckets if data is skewed.\n• Equal-Frequency (Quantiles) places an identical number of records into every bucket regardless of width, making it completely resilient to outliers and skew.",
            "analogy": "Cutting a pizza into equal degree angles (Equal-Width) versus slicing it so that every hungry kid gets the exact same amount of toppings (Equal-Frequency).",
            "why_it_matters": "Equal-frequency binning prevents outlier compression and guarantees that every bucket has enough training samples for statistically reliable model learning."
        },
        {
            "term": "The Boundary Cliff & Information Loss Tradeoff",
            "what_is_it": "• The primary downside of discretization where continuous detail is permanently erased, creating an artificial 'cliff' between adjacent data points.\n• Someone aged 39 years and 364 days lands in Bucket 1 while someone aged 40 years and 1 day lands in Bucket 2, receiving drastically different predictions despite a 48-hour difference.",
            "analogy": "A strict theme park height requirement: a child 1 millimeter below the line is forbidden from riding, while a child 1 millimeter taller rides, despite having virtually identical builds.",
            "why_it_matters": "Explains why manual binning is ideal for linear models and credit scorecards, but should be avoided for tree ensembles (XGBoost) which natively build optimal continuous splits."
        }
    ],
    "types_header": "Binning Strategies & Discretization Tools",
    "types_badge": "Feature Discretization",
    "quick_types": [
        {
            "type": "pd.cut(x, bins=K) [Equal-Width / Custom]",
            "definition": "Pandas function for dividing features into equal numerical distances or custom domain-defined cutpoints.",
            "looks_like": "df['age_group'] = pd.cut(df['age'], bins=[0, 18, 65, 100])"
        },
        {
            "type": "pd.qcut(x, q=K) [Equal-Frequency / Quantiles]",
            "definition": "Pandas quantile function creating buckets that contain the exact same count of observations.",
            "looks_like": "df['income_tier'] = pd.qcut(df['income'], q=4, labels=False)"
        },
        {
            "type": "KBinsDiscretizer(strategy='uniform')",
            "definition": "Scikit-Learn transformer that divides the feature dynamic range into equal-width numerical intervals.",
            "looks_like": "KBinsDiscretizer(n_bins=5, strategy='uniform')"
        },
        {
            "type": "KBinsDiscretizer(strategy='quantile')",
            "definition": "Scikit-Learn transformer dividing features into equal-sample quantile buckets for outlier resilience.",
            "looks_like": "KBinsDiscretizer(n_bins=5, strategy='quantile')"
        },
        {
            "type": "KBinsDiscretizer(strategy='kmeans')",
            "definition": "Algorithmic binning using 1D K-Means clustering to discover organic natural cluster group boundaries.",
            "looks_like": "KBinsDiscretizer(n_bins=4, strategy='kmeans')"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "b(x)",
            "meaning": "Assigned Bin Index",
            "plain_english": "The integer bucket label k ∈ {0, ..., K-1} assigned to observation x"
        },
        {
            "symbol": "x",
            "meaning": "Continuous Input Feature",
            "plain_english": "The raw un-binned numerical measurement, such as age or income"
        },
        {
            "symbol": "w",
            "meaning": "Equal-Width Interval Span",
            "plain_english": "The constant numerical distance allocated to each bucket across the feature range"
        },
        {
            "symbol": "K",
            "meaning": "Total Number of Bins",
            "plain_english": "The chosen count of discrete buckets or partitions (e.g. K = 5)"
        },
        {
            "symbol": "t_k",
            "meaning": "Bin Edge Threshold k",
            "plain_english": "The boundary cutoff separating bucket k-1 from bucket k"
        },
        {
            "symbol": "max(x), min(x)",
            "meaning": "Feature Extrema",
            "plain_english": "The maximum and minimum observed numerical values in the training feature"
        }
    ],
    "numerical_example": "Binning Customer Ages Across 10 Individuals: [18, 22, 25, 30, 34, 38, 42, 50, 68, 78]\n• Minimum observed: min(x) = 18 years\n• Maximum observed: max(x) = 78 years\n• Dynamic range: 78 - 18 = 60 years\n\n1. Equal-Width Binning (K = 3 bins):\n   • Interval width: w = (78 - 18) / 3 = 60 / 3 = 20 years\n   • Boundary edges: t₀ = 18, t₁ = 38, t₂ = 58, t₃ = 78\n   • Bucket 0 [18 to 38): [18, 22, 25, 30, 34] → 5 customers\n   • Bucket 1 [38 to 58): [38, 42, 50] → 3 customers\n   • Bucket 2 [58 to 78]: [68, 78] → 2 customers\n\n2. Equal-Frequency Quantile Binning (K = 2 bins, 50% Median Split):\n   • Median threshold: t₁ = (34 + 38) / 2 = 36.0 years\n   • Bucket 0 [18 to 36): [18, 22, 25, 30, 34] → Exactly 5 customers (50%)\n   • Bucket 1 [36 to 78]: [38, 42, 50, 68, 78] → Exactly 5 customers (50%)\n\nOutcome: A linear model can now fit independent step weights to Bucket 0, Bucket 1, and Bucket 2, successfully capturing non-linear relationships (e.g. higher insurance purchasing in young and retired demographics compared to middle-aged workers).",
    "pitfalls": "Common Pitfall: Manually binning continuous features before training modern gradient boosted trees (LightGBM, XGBoost, CatBoost). Tree algorithms already perform optimal internal histogram binning during training; manual binning strips away fine-grained continuous detail and usually causes a net drop in predictive accuracy. Reserve manual binning for linear models, scorecards, and human-interpretable rules.",
    "core_logic": "Why this matters: Linear models cannot learn non-linear relationships without feature transformations. Discretizing continuous features into one-hot encoded bins allows linear and logistic regressions to fit non-monotonic response curves (like U-shaped risk curves) while suppressing noise and absorbing extreme outliers.",
    "architectural_logic": "In production machine learning systems, KBinsDiscretizer is embedded inside a Scikit-Learn ColumnTransformer or Feature Store pipeline. Bin boundaries (t_k) are fitted strictly on the training partition and serialized into the model artifact, ensuring that online inference APIs map streaming continuous numbers into identical categorical buckets.",
    "connected_logic": [
        {
            "title": "Unlocking Non-Linearity in Generalized Linear Models (GLMs)",
            "content": "• In standard linear and logistic regression, continuous features are constrained to a single global slope weight (β · x).\n• One-hot encoding binned features transforms a single continuous variable into K step functions, allowing the model to fit U-shaped curves, plateaus, and non-monotonic risk profiles without polynomial expansion."
        },
        {
            "title": "Native Histogram Binning in Modern Gradient Boosters",
            "content": "• Tree algorithms like LightGBM and XGBoost natively build 256-bin feature histograms internally to accelerate continuous split finding (O(N) vs O(N log N)).\n• Manually pre-binning continuous features before training XGBoost deprives the trees of fine-grained gradient histograms and usually causes a net drop in predictive accuracy."
        },
        {
            "title": "Regulatory Credit Scorecards & WoE (Weight of Evidence)",
            "content": "• In consumer credit risk and banking underwriting, financial regulations often require explainable scorecard models where each applicant receives interpretable point buckets.\n• Binning combined with Weight of Evidence (WoE) ensures strict monotonicity in default risk, allows dedicated bins for missing values, and produces transparent audit trails for regulatory compliance."
        },
        {
            "title": "Strict Train-Test Pipeline Encapsulation",
            "content": "• Computing quantile cutoffs or K-Means cluster centers across the full dataset before cross-validation leaks test target distributions and boundaries.\n• In production ML pipelines, KBinsDiscretizer is fitted strictly on the training partition and saved inside the pipeline artifact to ensure identical bucket boundaries during live inference."
        }
    ],
    "key_takeaways": [
        "Non-Linear Step Transformation: Converts continuous variables into discrete buckets, letting linear models fit non-linear curves via separate weights.",
        "Equal-Width vs. Quantile: Equal-width divides by distance (can leave empty bins); Equal-frequency (quantiles) guarantees equal sample counts per bucket and resists skew.",
        "The Boundary Cliff Penalty: Permanent loss of continuous detail creates artificial cliffs between adjacent values separated by tiny margins.",
        "Model Suitability: Essential for linear models, generalized additive models, and credit scorecards; redundant and often harmful for modern tree ensembles (XGBoost, LightGBM)."
    ],
    "definition_bullets": [
        "Binning (Bucketing): A feature preprocessing technique that groups continuous numerical values into discrete intervals or categorical brackets.",
        "Feature Discretization: Partitioning continuous feature spaces into categorical bins to suppress noise, capture non-linearity, and neutralize outliers."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_binning_bucketing':
            item.update(BINNING_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_binning_bucketing not found in {filepath}")
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
        if item.get('id') == 'concept_binning_bucketing':
            item.update(BINNING_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
