import json

Z_SCORE_UPDATE = {
    "def": "Z-score Standardization (StandardScaler) transforms numerical features by centering them around a zero mean (μ = 0) and scaling them to unit variance (σ = 1), expressing each observation in terms of standard deviations from the average.",
    "definition": "Z-score Standardization (StandardScaler) transforms numerical features by centering them around a zero mean (μ = 0) and scaling them to unit variance (σ = 1), expressing each observation in terms of standard deviations from the average.",
    "formula": "$$z_i = \\frac{x_i - \\mu}{\\sigma}, \\quad \\mu = \\frac{1}{N}\\sum_{j=1}^{N} x_j, \\quad \\sigma = \\sqrt{\\frac{1}{N}\\sum_{j=1}^{N} (x_j - \\mu)^2}$$",
    "formula_explanation": "",
    "logic": "Rather than squashing data into hard [0, 1] boundaries, standardization centers values around zero and normalizes their spread. It prevents high-variance features from hijacking gradient descent, stops PCA from being dominated by arbitrary units, and eliminates gradient zig-zagging in neural networks.",
    "example": "Customer metrics: Comparing 'Annual Spend' ($12,000) and 'Items Bought' (3). Unscaled KNN would measure Euclidean distances almost entirely in dollars. Standardizing both to zero mean and unit variance gives both attributes an equal voice.",
    "simple_summary": "Standardization centers your data at 0 and rescales its spread so the standard deviation is 1. Unlike Min-Max, it is unbounded (values can be negative or greater than 1) and handles outliers gracefully without squishing the rest of the dataset. Deep learning and PCA rely on it because zero-centered inputs allow weights to update smoothly and prevent high-magnitude features from dominating.",
    "core_terms": [
        {
            "term": "Z-score Standardization (StandardScaler)",
            "what_is_it": "• A linear feature scaling method that subtracts the mean (centering at 0) and divides by the standard deviation (scaling spread to 1).\n• Expresses every raw observation as a signed score indicating how many standard deviations it sits above (positive) or below (negative) the dataset mean.",
            "analogy": "Grading on a curve: rather than judging students on raw scores out of 100, assigning grades based on whether they placed +1 standard deviation above the class average or -1 below it.",
            "why_it_matters": "Places diverse features on an identical zero-centered scale without crushing outliers into artificial boundaries, making it the default scaler for machine learning."
        },
        {
            "term": "Zero-Centering & Gradient Zig-Zagging",
            "what_is_it": "• The optimization phenomenon in neural networks where having all-positive inputs forces backpropagation weight gradients in a neuron to share the identical sign.\n• When inputs are strictly positive, layer weights must either all increase or all decrease together, forcing the optimizer into a slow, jagged zig-zag trajectory across parameter space.",
            "analogy": "Trying to steer a bicycle diagonally when the handlebars are locked to alternate only between sharp 90-degree left and right turns instead of steering straight.",
            "why_it_matters": "Explains why deep learning architectures strictly require zero-centered inputs: it decouples weight gradient signs and dramatically speeds up backpropagation."
        },
        {
            "term": "The Linear Transformation Fallacy (Normal Distribution Myth)",
            "what_is_it": "• The widespread misconception that applying Z-score standardization converts skewed or multimodal data into a Gaussian normal distribution.\n• Because standardization only subtracts a constant and divides by a scalar (y = mx + b), the underlying shape, skewness, and multimodal peaks remain completely unchanged.",
            "analogy": "Zooming in and panning a photograph on your smartphone: the framing shifts, but the faces and objects inside the photo do not change shape.",
            "why_it_matters": "Reminds engineers that if an algorithm strictly requires Gaussian normality, non-linear transforms like Box-Cox or QuantileTransformer are needed instead."
        }
    ],
    "types_header": "Standardization Configurations & Properties",
    "types_badge": "Scaling Mechanics",
    "quick_types": [
        {
            "type": "StandardScaler(with_mean=True)",
            "definition": "Centers data to zero mean and scales to unit variance; standard default for dense tabular features.",
            "looks_like": "scaler = StandardScaler().fit(X_train)"
        },
        {
            "type": "StandardScaler(with_mean=False)",
            "definition": "Scales to unit variance without centering to zero; mandatory for sparse matrices to preserve sparsity without RAM blowup.",
            "looks_like": "StandardScaler(with_mean=False).fit(X_sparse)"
        },
        {
            "type": "Empirical 68-95-99.7 Rule",
            "definition": "Gaussian property where 68% of data falls in [-1, +1], 95% in [-2, +2], and 99.7% in [-3, +3] under normal distributions.",
            "looks_like": "z ∈ [-3.0, +3.0] covers 99.7% of Gaussian data"
        },
        {
            "type": "Z-Score Outlier Filtering",
            "definition": "Statistical anomaly detection rule that flags observations exceeding |z| > 3.0 as extreme tail outliers.",
            "looks_like": "outliers = df[np.abs(z_scores) > 3.0]"
        },
        {
            "type": "PCA Variance Equalizer",
            "definition": "Standardizing features prior to eigendecomposition so variables with large units do not hijack principal axes.",
            "looks_like": "PCA().fit(StandardScaler().fit_transform(X))"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "z_i",
            "meaning": "Standardized Z-Score",
            "plain_english": "Transformed value representing standard deviations away from the mean"
        },
        {
            "symbol": "x_i",
            "meaning": "Raw Feature Observation",
            "plain_english": "The original unscaled numerical measurement for data instance i"
        },
        {
            "symbol": "μ (mu)",
            "meaning": "Feature Mean",
            "plain_english": "The arithmetic average of the training feature distribution"
        },
        {
            "symbol": "σ (sigma)",
            "meaning": "Standard Deviation",
            "plain_english": "The square root of variance, measuring the spread of the training distribution"
        },
        {
            "symbol": "N",
            "meaning": "Sample Size",
            "plain_english": "Total count of observed training samples used to calculate mean and variance"
        },
        {
            "symbol": "x_j",
            "meaning": "Observation Index j",
            "plain_english": "Individual sample values summed across the training partition"
        }
    ],
    "numerical_example": "Blood Pressure Standardization across Patients (Systolic mmHg):\nObserved patient readings: [110, 120, 130, 140, 150]\n\n1. Calculate Mean (μ):\n   • μ = (110 + 120 + 130 + 140 + 150) / 5 = 650 / 5 = 130.0 mmHg\n\n2. Calculate Variance (σ²) and Standard Deviation (σ):\n   • Deviations (x_i - μ): [-20, -10, 0, +10, +20]\n   • Squared deviations: [400, 100, 0, 100, 400] → Sum = 1000\n   • Variance σ² = 1000 / 5 = 200\n   • Standard Deviation σ = √200 ≈ 14.142 mmHg\n\n3. Calculate Z-Scores (z_i = (x_i - μ) / σ):\n   • Patient 1 (110 mmHg): z₁ = (110 - 130) / 14.142 = -20 / 14.142 = -1.414 (below average)\n   • Patient 3 (130 mmHg): z₃ = (130 - 130) / 14.142 = 0 / 14.142 = 0.000 (at the mean)\n   • Patient 5 (150 mmHg): z₅ = (150 - 130) / 14.142 = +20 / 14.142 = +1.414 (above average)\n   • Outlier Patient 6 (Hypertensive Crisis, 220 mmHg):\n     z₆ = (220 - 130) / 14.142 = +90 / 14.142 = +6.364\n\nOutcome: Unlike Min-Max which compresses all non-outliers into a tiny slice, Patient 6 clearly stands out at +6.36 standard deviations while Patients 1–5 maintain balanced statistical separation.",
    "pitfalls": "Common Pitfall: Centering sparse matrices (e.g. TF-IDF text features or one-hot vectors) with StandardScaler(with_mean=True). Subtracting the mean turns millions of memory-efficient implicit zeros into explicit negative floating-point numbers, instantly converting a 50 MB sparse matrix into a 30 GB dense array that crashes server RAM. Always use with_mean=False for sparse inputs.",
    "core_logic": "Why this matters: In machine learning models with gradient updates, dot products, or variance-based projections, Z-score standardization guarantees that all features contribute equitably to loss gradients and geometric metrics, eliminating arbitrary measurement unit artifacts.",
    "architectural_logic": "In enterprise ML architectures, StandardScaler parameters (mean_, scale_) are calculated strictly on training folds and serialized as part of an immutable pipeline artifact (e.g. ONNX, Scikit-Learn Pipeline). Test and real-time inference payloads are transformed using the saved training parameters to eliminate train-test skew.",
    "connected_logic": [
        {
            "title": "Decoupling Weight Updates in Deep Neural Networks",
            "content": "• When inputs are strictly all-positive (as in Min-Max [0, 1]), backprop weight gradients ∂L/∂w_i = x_i · δ all share the sign of error δ, forcing weights to update in an oscillating zig-zag trajectory.\n• Zero-centered standardized inputs generate mixed-sign feature vectors, freeing weights in each neuron to update along independent gradient directions for significantly faster convergence."
        },
        {
            "title": "Principal Component Analysis (PCA) Axis Distortions",
            "content": "• PCA identifies orthogonal eigenvectors of the covariance matrix that maximize directional variance Var(w^T X).\n• If a feature with arbitrary large units (e.g. Annual Revenue in cents) has a raw variance of 10^8, PCA aligns its first principal axis entirely with that feature; standardization to unit variance (σ² = 1) guarantees fair geometric projection."
        },
        {
            "title": "Equitable Shrinkage in L1/L2 Regularization (Weight Decay)",
            "content": "• Regularization penalties like Ridge (λ ∑ w_i²) and Lasso (λ ∑ |w_i|) apply a uniform penalty scalar across all model coefficients.\n• Unstandardized features force models to learn tiny weights for large-scale features and massive weights for small-scale features, causing regularization to penalize small-scale features disproportionately; standardization restores fair penalty shrinkage."
        },
        {
            "title": "Strict Train-Test Pipeline Encapsulation & Leakage Prevention",
            "content": "• Computing μ and σ across the entire dataset prior to splitting leaks future validation/test distribution statistics into the training fold.\n• In enterprise architectures, StandardScaler is fit exclusively on training data and persisted inside serialization pipelines (e.g. MLflow, Scikit-Learn Pipeline) to guarantee reproducible inference transforms."
        }
    ],
    "key_takeaways": [
        "Zero-Centered Unit Spread: Transforms features into a distribution with mean 0 and standard deviation 1, leaving observations unbounded.",
        "Outlier Preservation: Unlike Min-Max, extreme values remain visible in the distribution tails (e.g. z = +6.3) rather than crushing regular data.",
        "Deep Learning & PCA Foundation: Zero-centering prevents gradient zig-zagging in neural networks, and unit variance prevents high-magnitude features from dominating PCA.",
        "Shape Invariance: Standardization is a linear transform (y = mx + b) and does NOT make non-normal distributions Gaussian."
    ],
    "definition_bullets": [
        "Z-score Standardization: A linear transformation centering data at mean 0 and scaling spread to standard deviation 1.",
        "Zero-Centering: Shifting feature values so their center of mass sits at zero, preventing uniform sign locking during gradient descent."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_z_score_scaling':
            item.update(Z_SCORE_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_z_score_scaling not found in {filepath}")
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
        if item.get('id') == 'concept_z_score_scaling':
            item.update(Z_SCORE_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
