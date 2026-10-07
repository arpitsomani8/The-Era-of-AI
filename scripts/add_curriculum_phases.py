import json
import os

def create_concept_obj(
    cid, title, tid, tlabel, cat, cat_label, definition, formula, logic, example,
    core_terms, symbol_guide, numerical_example, pitfalls, tags, takeaways
):
    return {
        "id": cid,
        "title": title,
        "topic_id": tid,
        "topic_label": tlabel,
        "category": cat,
        "category_label": cat_label,
        "raw_subtopic": title,
        "def": definition,
        "formula": formula,
        "logic": logic,
        "example": example,
        "tags": tags,
        "raw_sub": title,
        "definition": definition,
        "formula_explanation": f"Mathematical formulation and loss objective for {title}.",
        "simple_summary": definition.split('.')[0] + '.',
        "core_terms": core_terms,
        "symbol_guide": symbol_guide,
        "numerical_example": numerical_example,
        "pitfalls": pitfalls,
        "core_logic": logic,
        "architectural_logic": f"{title} integrates into production machine learning pipelines by establishing mathematically sound boundaries and optimal computational resource utilization.",
        "key_takeaways": takeaways,
        "definition_bullets": [
            f"**Core Purpose:** {definition}",
            f"**Operational Role:** {logic}",
            f"**Production Significance:** {example}"
        ]
    }

# Read existing data
with open('src/data/concepts.json', 'r', encoding='utf-8') as f:
    concepts = json.load(f)

with open('src/data/topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

with open('src/data/allNodes.json', 'r', encoding='utf-8') as f:
    nodes = json.load(f)

with open('src/data/interviewQuestions.json', 'r', encoding='utf-8') as f:
    interviews = json.load(f)

existing_concept_ids = set(c['id'] for c in concepts)
existing_topic_ids = set(t['id'] for t in topics)
existing_node_ids = set(n['id'] for n in nodes)
existing_interview_ids = set(q['id'] for q in interviews)

new_concepts = []

# ==========================================
# 1. TOPIC: ml_svm_ensembles (Category: ml)
# ==========================================
t_svm_id = "ml_svm_ensembles"
t_svm_label = "Support Vector Machines & Production Ensembles"

new_concepts.append(create_concept_obj(
    "concept_svm_max_margin",
    "Support Vector Machines (SVM & Maximum Margin Hyperplanes)",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "Support Vector Machines find the optimal hyperplane that separates classes with the maximum possible margin, relying only on critical boundary instances called support vectors.",
    r"\max_{w, b} \frac{2}{\|w\|} \quad \text{s.t.} \quad y_i(w^T x_i + b) \ge 1 \quad \forall i",
    "By maximizing the geometric margin (2/||w||), SVM minimizes the structural risk rather than empirical risk, drastically preventing overfitting on small-to-medium sized datasets.",
    "Used in multi-tenant financial fraud detection to cleanly separate fraudulent credit transfers from authentic customer behaviors.",
    [
        {"term": "Support Vector", "what_is_it": "The data points that lie closest to the decision boundary and determine the position and orientation of the separating hyperplane.", "analogy": "The fence posts that directly define the boundary line between two properties.", "why_it_matters": "All other training points can be removed without altering the final decision boundary."},
        {"term": "Margin", "what_is_it": "The perpendicular distance between the separating hyperplane and the closest data points from either class.", "analogy": "A wide median strip on a highway separating oncoming traffic lanes.", "why_it_matters": "Wider margins guarantee greater tolerance to future measurement noise and variance."}
    ],
    [
        {"symbol": "w", "meaning": "Weight vector orthogonal to the separating hyperplane", "plain_english": "Direction vector pointing perpendicular to the decision boundary."},
        {"symbol": "b", "meaning": "Bias term / intercept", "plain_english": "Shifts the hyperplane offset from the coordinate origin."},
        {"symbol": "y_i", "meaning": "Binary class label in {-1, +1}", "plain_english": "Ground truth classification sign for training sample i."}
    ],
    "Given weight vector w = [3, 4] with norm ||w|| = 5:\nGeometric margin = 2 / ||w|| = 2 / 5 = 0.4 units on either side of the separating hyperplane w^T x + b = 0.",
    "Do not train linear SVMs without standardizing feature scales; unscaled features cause the optimizer to bias the margin orientation toward high-magnitude features.",
    ["SVM", "Maximum Margin", "Support Vectors", "Convex Optimization"],
    [
        "SVM solves a convex quadratic programming problem with a guaranteed global optimum (no local minima).",
        "Only support vectors determine the decision boundary; removing non-support vectors leaves the model unchanged.",
        "Feature scaling (StandardScaler) is strictly mandatory before fitting an SVM."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_kernel_trick_rbf",
    "The Kernel Trick & RBF Kernels (Non-Linear Mapping)",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "The Kernel Trick implicitly projects non-linearly separable data into an infinite-dimensional Hilbert space by computing dot products via kernel functions without ever explicitly calculating high-dimensional coordinates.",
    r"K(x_i, x_j) = \exp\left(-\gamma \|x_i - x_j\|^2\right) = \langle \phi(x_i), \phi(x_j) \rangle",
    "Enables linear decision boundaries in latent high-dimensional spaces to act as intricate, non-linear contour boundaries in the original feature space with O(N) computational complexity.",
    "Classifying genomic sequences and protein folding structures where biological interactions represent complex non-linear combinations.",
    [
        {"term": "RBF Kernel (Radial Basis Function)", "what_is_it": "A stationary kernel whose value depends only on the Euclidean distance between two feature vectors.", "analogy": "A localized spotlight centered on each training point that dims smoothly with distance.", "why_it_matters": "Can model arbitrarily complex non-linear decision boundaries with a single smoothness parameter gamma."},
        {"term": "Gamma Parameter", "what_is_it": "Controls the radius of influence of each support vector in the feature space.", "analogy": "How focused or wide a flashlight beam is.", "why_it_matters": "High gamma leads to tight localized islands (overfitting); low gamma creates overly smooth boundaries (underfitting)."}
    ],
    [
        {"symbol": "K(x_i, x_j)", "meaning": "Kernel evaluation between two input vectors", "plain_english": "Implicit inner product in higher-dimensional transformed space."},
        {"symbol": "\\gamma", "meaning": "Kernel scale parameter (1 / (2*sigma^2))", "plain_english": "Determines how fast similarity drops to zero with Euclidean distance."}
    ],
    "For x1 = [1, 2], x2 = [2, 3] with gamma = 0.5:\nSquared Euclidean distance ||x1 - x2||^2 = (1-2)^2 + (2-3)^2 = 1 + 1 = 2.\nKernel similarity K(x1, x2) = exp(-0.5 * 2) = exp(-1.0) ≈ 0.3678.",
    "Setting gamma too high turns the SVM into a lookup table where each training point forms an isolated circular decision island, completely ruining test generalization.",
    ["Kernel Trick", "RBF Kernel", "Hilbert Space", "Non-linear Separation"],
    [
        "The kernel trick avoids computing expensive or infinite-dimensional coordinate mappings phi(x).",
        "Mercer's Theorem guarantees that any positive semi-definite kernel corresponds to an inner product in some space.",
        "Always tune C and gamma jointly via grid search or Bayesian optimization."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_svm_slack_soft_margin",
    "Soft-Margin Optimization & Slack Variables (C-Hyperparameter)",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "Soft-margin SVM introduces non-negative slack variables that permit controlled margin violations and misclassifications to handle overlapping distributions and noisy real-world data.",
    r"\min_{w, b, \xi} \frac{1}{2}\|w\|^2 + C \sum_{i=1}^n \xi_i \quad \text{s.t.} \quad y_i(w^T x_i + b) \ge 1 - \xi_i, \quad \xi_i \ge 0",
    "The C hyperparameter governs the bias-variance tradeoff: large C strictly penalizes slack (narrow margin, low bias, high variance), while small C tolerates violations (wide margin, high bias, low variance).",
    "Multi-tenant customer churn prediction where customer behavioral noise creates overlapping feature boundaries.",
    [
        {"term": "Slack Variable (xi_i)", "what_is_it": "A measurement of how far a training sample violates the canonical margin boundary.", "analogy": "A hall pass permitting students a specific margin of lateness without failing.", "why_it_matters": "Allows linear classifiers to remain stable when datasets contain overlapping outliers."},
        {"term": "C Parameter", "what_is_it": "The regularization constant governing the penalty weight assigned to slack violations.", "analogy": "A strict judge (high C) versus a lenient mediator (low C).", "why_it_matters": "Directly controls whether the model favors boundary simplicity or training sample accuracy."}
    ],
    [
        {"symbol": "\\xi_i", "meaning": "Slack variable for sample i", "plain_english": "0 if strictly correct; between 0 and 1 if inside margin; > 1 if misclassified."},
        {"symbol": "C", "meaning": "Slack penalty tradeoff multiplier", "plain_english": "Higher C penalizes mistakes aggressively; lower C tolerates margin intruders."}
    ],
    "Sample i has margin distance y_i(w^T x_i + b) = 0.6.\nSince the margin target is 1.0, slack xi_i = 1.0 - 0.6 = 0.4.\nWith penalty C = 10, this sample adds 10 * 0.4 = 4.0 to the overall optimization loss.",
    "Assuming C acts like an L2 penalty weight lambda: in SVM, C is inversely proportional to regularization (High C = Less Regularization, Low C = Strong Regularization).",
    ["Slack Variables", "Soft Margin", "C Hyperparameter", "Optimization"],
    [
        "Hard-margin SVM fails entirely if data is not linearly separable; soft-margin is universally used in production.",
        "Samples with xi_i > 0 are margin violators; samples with xi_i > 1 are misclassified training samples.",
        "Low C creates a wider highway that ignores small outlier rocks; High C swerves around every single pebble."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_ensemble_architectures",
    "Ensemble Architectures (Voting, Bagging, Boosting & Stacking)",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "Ensemble techniques combine predictions from multiple base learners to reduce variance (Bagging), reduce bias (Boosting), or optimize diverse algorithmic hypotheses (Stacking / Voting).",
    r"\hat{y}_{\text{voting}} = \arg\max_c \sum_{m=1}^M w_m \cdot P_m(y=c|x), \quad \hat{y}_{\text{stacking}} = g\left(f_1(x), f_2(x), \dots, f_M(x)\right)",
    "Uncorrelated errors from diverse models cancel out mathematically, driving ensemble error significantly below that of any individual constituent model.",
    "Winning Kaggle competition solutions and enterprise loan approval engines combining LightGBM, CatBoost, and Logistic Regression.",
    [
        {"term": "Bagging (Bootstrap Aggregating)", "what_is_it": "Training multiple instances of the same model on random bootstrap samples with replacement and averaging predictions.", "analogy": "Asking 100 independent doctors for a diagnosis and taking the majority consensus.", "why_it_matters": "Reduces variance without increasing bias (e.g. Random Forest)."},
        {"term": "Stacking (Stacked Generalization)", "what_is_it": "Training a meta-learner (e.g., Logistic Regression) on the out-of-fold predictions of multiple base models.", "analogy": "A chief executive who weighs the recommendations of specialized department heads.", "why_it_matters": "Blends completely different model families (trees, linear, neural nets) into a unified predictor."}
    ],
    [
        {"symbol": "f_m(x)", "meaning": "Prediction of m-th base model", "plain_english": "Output generated by an individual estimator."},
        {"symbol": "g(\\cdot)", "meaning": "Meta-model combiner", "plain_english": "Higher-level model trained to combine base model outputs."},
        {"symbol": "w_m", "meaning": "Weight assigned to model m", "plain_english": "Confidence multiplier in weighted soft voting."}
    ],
    "Three models predict fraud probability: Model 1 = 0.85, Model 2 = 0.90, Model 3 = 0.40.\nSoft Voting average = (0.85 + 0.90 + 0.40) / 3 = 2.15 / 3 = 0.7167 (Final decision: Fraudulent).",
    "Stacking base model predictions on the training set directly causes massive data leakage; out-of-fold cross-validation predictions must be used to train meta-learners.",
    ["Ensembles", "Bagging", "Boosting", "Stacking", "Soft Voting"],
    [
        "Ensemble diversity is essential: combining 10 identical models yields zero variance reduction.",
        "Bagging reduces variance; Boosting reduces bias; Stacking optimizes multi-model cooperation.",
        "Soft voting (averaging probabilities) consistently outperforms hard voting (majority rule on class labels)."
    ]
))

new_concepts.append(create_concept_obj(
    "concept_scikit_joblib_multitenant",
    "Scikit-Learn, Joblib Model Serialization & Multi-Tenant Classifiers",
    t_svm_id, t_svm_label, "ml", "Classical Machine Learning",
    "Serializing fitted scikit-learn estimators and preprocessing pipelines using Joblib/pickle, and structuring multi-tenant ML inference architectures where tenant models are dynamically routed or partitioned.",
    r"\text{Latency}_{\text{infer}} = T_{\text{deserialize}} + T_{\text{pipeline\_transform}} + T_{\text{predict}} < 5\,\text{ms}",
    "Joblib employs efficient disk-to-memory memory mapping (mmap) for large NumPy weight arrays, enabling sub-millisecond model loading and zero-copy shared memory access across multi-worker server processes.",
    "A multi-tenant SaaS CRM platform maintaining 1,200 tenant-specific lead scoring models loaded on-demand via LRU memory cache.",
    [
        {"term": "Joblib Serialization", "what_is_it": "Python serialization optimized for objects containing large internal NumPy arrays.", "analogy": "Packing precision machine parts into custom pre-formed foam cases rather than generic bubble wrap.", "why_it_matters": "Loads large weight matrices up to 10x faster than standard Python pickle."},
        {"term": "Multi-Tenant Model Partitioning", "what_is_it": "Architectural strategy of training customer-specific models or prepending tenant ID embeddings to guarantee data isolation.", "analogy": "Safe deposit boxes inside a bank vault where each client has their own key and compartment.", "why_it_matters": "Prevents data leakage across enterprise clients while tailoring models to tenant-specific distributions."}
    ],
    [
        {"symbol": "\\text{dump}(model, path)", "meaning": "Joblib disk serialization", "plain_english": "Saves trained weights and preprocessors to binary storage."},
        {"symbol": "\\text{load}(path, mmap)", "meaning": "Memory-mapped loading", "plain_english": "Reads model weights into process memory with zero copy overhead."}
    ],
    "Joblib mmap benchmark: A 450 MB ensemble model loads in 18 ms via memory mapping versus 420 ms via standard uncompressed pickle deserialization.",
    "Deserializing untrusted Joblib files via joblib.load opens severe remote code execution vulnerabilities; only deserialize files signed with trusted cryptographic hashes.",
    ["Joblib", "Scikit-Learn", "Multi-Tenant", "Serialization", "Inference Latency"],
    [
        "Always serialize the complete Pipeline (imputer, scaler, encoder, classifier) together, never the classifier alone.",
        "Multi-tenant architectures should keep an LRU cache of recently queried tenant models in Redis or local RAM.",
        "Pin exact scikit-learn and NumPy versions in requirements.txt to prevent silent deserialization crashes."
    ]
))

print(f"Added {len(new_concepts)} concepts for ml_svm_ensembles.")

# Write updated concepts back
# We'll continue adding all 8 topics...
