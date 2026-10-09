import json

MIN_MAX_SCALING_UPDATE = {
    "def": "Min-Max Normalization (Linear Scaling) rescales numerical features into a fixed bounded interval—typically [0, 1] or [-1, 1]—preserving relative proportions and original rank ordering across observations.",
    "definition": "Min-Max Normalization (Linear Scaling) rescales numerical features into a fixed bounded interval—typically [0, 1] or [-1, 1]—preserving relative proportions and original rank ordering across observations.",
    "formula": "$$\\hat{x}_i = \\frac{x_i - x_{\\min}}{x_{\\max} - x_{\\min}}, \\quad x_{\\text{scaled}} = a + \\frac{x_i - x_{\\min}}{x_{\\max} - x_{\\min}} (b - a) \\in [a, b]$$",
    "formula_explanation": "",
    "logic": "Features with large numerical ranges (e.g. Salary in tens of thousands) dominate distance metrics and distort loss surfaces into elongated canyons. Min-Max scaling rounds loss landscapes into circular bowls, accelerating gradient descent convergence while equalizing feature contributions in distance- and margin-based algorithms.",
    "example": "Computer vision pipelines: Raw 8-bit image RGB pixels ranging from 0 to 255 are linearly divided by 255.0 to map them into [0.0, 1.0], stabilizing weight gradients in convolutional neural networks.",
    "simple_summary": "Min-Max Normalization squashes numbers into a bounded range (usually 0 to 1) without altering their relative ranking. It prevents large numbers from drowning out smaller ones in distance-based models (KNN, K-Means) and transforms steep, narrow loss canyons into round bowls so Gradient Descent converges up to 100x faster. However, it is highly sensitive to outliers, which crush normal values into tiny bands.",
    "core_terms": [
        {
            "term": "Min-Max Normalization (Linear Rescaling)",
            "what_is_it": "• A feature scaling method that linearly shifts and compresses numerical values into a fixed bound, typically between 0 and 1.\n• Preserves the relative proportional distances and exact rank ordering between data points while placing all variables on an identical scale.",
            "analogy": "Converting test scores from different exams (one scored out of 50, another out of 200, another out of 10) into standardized percentages out of 100%.",
            "why_it_matters": "Prevents features with large raw numerical magnitudes (e.g. Income $80,000) from completely drowning out features with small magnitudes (e.g. Experience 5 years)."
        },
        {
            "term": "Loss Surface Conditioning (Canyons vs. Bowls)",
            "what_is_it": "• The geometric shape of the objective function landscape navigated by gradient descent optimizers during model training.\n• Unscaled features warp the loss surface into steep, elongated ravines where gradients oscillate violently across canyon walls; scaled features create a balanced spherical bowl where gradients point straight to the minimum.",
            "analogy": "Rolling a marble down a round ceramic bowl (rolls straight to the bottom) versus rolling it between two steep, jagged canyon cliffs (bounces violently from wall to wall).",
            "why_it_matters": "Accelerates gradient descent convergence by 10x to 100x and allows the use of larger, stable learning rates without causing numerical divergence."
        },
        {
            "term": "The Outlier Compression Trap",
            "what_is_it": "• The critical structural weakness of Min-Max scaling caused by strictly anchoring the transformation bounds to the absolute sample minimum and maximum.\n• If a column contains even a single extreme outlier (e.g. a billionaire in an average income column), the entire regular population gets squashed into a microscopic, indistinguishable band between 0.00 and 0.01.",
            "analogy": "Stretching a measuring tape from zero to the height of the Empire State Building to measure a pencil, an apple, and a chair: at that scale, all three items appear to have identical zero height.",
            "why_it_matters": "Dictates when to switch scaling strategies: when data features contain heavy tails or extreme anomalies, use StandardScaler or RobustScaler instead."
        }
    ],
    "types_header": "Scaling Ranges & Model Sensitivity",
    "types_badge": "Normalization Schemes",
    "quick_types": [
        {
            "type": "Standard Unit Interval [0, 1]",
            "definition": "Default MinMaxScaler configuration that maps the empirical minimum to 0 and empirical maximum to 1.",
            "looks_like": "MinMaxScaler(feature_range=(0, 1))"
        },
        {
            "type": "Bipolar Centered Range [-1, 1]",
            "definition": "Zero-centered linear rescaling commonly utilized for zero-symmetric neural activation functions like Tanh.",
            "looks_like": "MinMaxScaler(feature_range=(-1, 1))"
        },
        {
            "type": "Computer Vision Pixel Scaling",
            "definition": "Direct linear normalization dividing 8-bit integer RGB channels by 255.0 to map pixel tensors into [0.0, 1.0].",
            "looks_like": "X_norm = image_array / 255.0"
        },
        {
            "type": "Inference Out-of-Bounds Clipping",
            "definition": "Scikit-Learn parameter enforcing strict clipping so test values beyond training bounds do not exceed [0, 1].",
            "looks_like": "MinMaxScaler(clip=True)"
        },
        {
            "type": "Scale-Invariant Tree Ensembles",
            "definition": "Algorithms (Random Forest, XGBoost, LightGBM) whose monotonic axis-aligned splits are 100% immune to feature scale.",
            "looks_like": "XGBClassifier() / RandomForestRegressor()"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x_i",
            "meaning": "Raw Feature Observation",
            "plain_english": "The original unscaled numerical measurement for data instance i"
        },
        {
            "symbol": "x_min",
            "meaning": "Feature Minimum Value",
            "plain_english": "The smallest observed numerical value in the training distribution"
        },
        {
            "symbol": "x_max",
            "meaning": "Feature Maximum Value",
            "plain_english": "The largest observed numerical value in the training distribution"
        },
        {
            "symbol": "x̂_i",
            "meaning": "Unit Normalized Value",
            "plain_english": "The transformed feature observation mapped into the standard [0, 1] interval"
        },
        {
            "symbol": "a, b",
            "meaning": "Custom Bound Parameters",
            "plain_english": "The desired lower and upper target boundaries (e.g. a = -1, b = 1)"
        },
        {
            "symbol": "x_scaled",
            "meaning": "Rescaled Target Feature",
            "plain_english": "The final numerical value linearly transformed into the custom [a, b] range"
        }
    ],
    "numerical_example": "Salary Rescaling across Job Applicants:\nTraining data salaries: [$30,000, $50,000, $70,000, $110,000]\n• Minimum observed: x_min = $30,000\n• Maximum observed: x_max = $110,000\n• Dynamic Range: x_max - x_min = $110,000 - $30,000 = $80,000\n\n1. Standard Normalization to [0, 1]:\n   • Candidate 1 ($50,000): x̂₁ = (50,000 - 30,000) / 80,000 = 20,000 / 80,000 = 0.25\n   • Candidate 2 ($70,000): x̂₂ = (70,000 - 30,000) / 80,000 = 40,000 / 80,000 = 0.50\n   • Candidate 3 ($110,000): x̂₃ = (110,000 - 30,000) / 80,000 = 80,000 / 80,000 = 1.00\n\n2. Custom Rescaling to [-1, 1] (a = -1, b = 1):\n   • Candidate 1: x_scaled = -1 + 0.25 · (1 - (-1)) = -1 + 0.25 · 2 = -0.50\n   • Candidate 2: x_scaled = -1 + 0.50 · 2 = 0.00 (perfect center!)\n   • Candidate 3: x_scaled = -1 + 1.00 · 2 = +1.00\n\nOutcome: All applicant salaries are bounded symmetrically, preserving exact proportional intervals without distorting distance measurements.",
    "pitfalls": "Common Pitfall: Applying Min-Max Normalization on datasets containing heavy-tailed distributions or extreme outliers. Because the denominator relies strictly on x_max - x_min, a single billion-dollar net worth compresses 99.9% of regular observations into a narrow band between [0.00, 0.01], destroying feature variance. In the presence of outliers, use RobustScaler or StandardScaler instead.",
    "core_logic": "Why this matters: Feature magnitudes alter distance metrics and optimizer convergence. In algorithms relying on Euclidean distance (KNN, K-Means), dot products (SVM, neural networks), or gradient descent updates, Min-Max Normalization eliminates arbitrary unit bias and balances parameter update rates across all dimensions.",
    "architectural_logic": "In production ML workflows, MinMaxScaler is integrated strictly inside Scikit-Learn Pipelines or online Feature Store ingestion DAGs. Parameters (x_min, x_max) are computed exclusively on the training fold, with clip=True enabled to prevent unforeseen production drift from exceeding bounded ranges.",
    "connected_logic": [
        {
            "title": "Hessian Conditioning & Gradient Descent Convergence",
            "content": "• When feature scales differ by orders of magnitude, the Hessian matrix of the loss function develops an extreme condition number (λ_max / λ_min >> 1), creating a deep elliptical ravine.\n• Min-Max scaling rounds out the loss contours into an isotropic bowl, equalizing gradient magnitudes across parameters and enabling optimizers (SGD, Adam) to use larger learning rates without divergent oscillations."
        },
        {
            "title": "Regularization Penalty Distortion in Linear Models",
            "content": "• In Ridge (L2) and Lasso (L1) regression, the penalty term applies an identical shrinkage weight λ to all coefficients regardless of their natural feature scale.\n• If one feature has raw values in millions (tiny coefficient) and another has values in decimals (huge coefficient), unscaled regularization penalizes features unfairly; linear scaling restores equitable coefficient shrinkage."
        },
        {
            "title": "Preventing Saturation in Sigmoidal Neural Layers",
            "content": "• In neural networks utilizing Sigmoid or Softmax activation layers, large unscaled inputs push initial net activations into saturated asymptotic regions (|z| > 5).\n• In these saturated regions, activation derivatives vanish (σ'(z) ≈ 0), halting backpropagation; Min-Max scaling keeps initial layer activations within the sensitive linear dynamic range."
        },
        {
            "title": "Strict Train-Test Pipeline Encapsulation",
            "content": "• Computing x_min and x_max across the combined dataset before train/test splitting leaks global distribution extrema into the training process.\n• In production ML pipelines, the scaler is fit strictly on training splits and serialized inside a Scikit-Learn Pipeline or Feature Store to transform test batches consistently."
        }
    ],
    "key_takeaways": [
        "Range Compression: Min-Max linearly bounds features into [0, 1] while preserving exact relative ordering and distance ratios.",
        "Optimizer Acceleration: Eliminates narrow loss canyons, enabling Gradient Descent to converge up to 100x faster along spherical contours.",
        "Model Sensitivity: Crucial for distance-based (KNN, K-Means), margin-based (SVM), and neural models; tree-based ensembles are completely invariant to scaling.",
        "Outlier Sensitivity: Extremely fragile to extreme values; a single massive outlier collapses all remaining observations into an uninformative microscopic band."
    ],
    "definition_bullets": [
        "Min-Max Normalization: A linear scaling transformation mapping raw numerical values into a predefined bounded interval, typically [0, 1].",
        "Loss Landscape Conditioning: Rescaling feature axes to equalize gradient magnitudes and eliminate oscillatory zig-zagging during optimization."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_min_max_scaling':
            item.update(MIN_MAX_SCALING_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_min_max_scaling not found in {filepath}")
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
        if item.get('id') == 'concept_min_max_scaling':
            item.update(MIN_MAX_SCALING_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
