"""
MLOps & Production Systems Core Concepts (5 concepts):
- Model Registry & Experiment Tracking
- High-Throughput Serving (vLLM PagedAttention, ONNX)
- Data Drift vs Concept Drift Monitoring
- Feature Stores & Continuous Training CI/CD
- Fairness, Accountability & Responsible AI Auditing
"""

MLOPS_CONCEPTS = [
    {
        "id": "model-registry-experiment-tracking",
        "topic_id": "mlops_root",
        "topic_label": "Production ML Systems & MLOps",
        "category": "mlops",
        "category_label": "MLOps & Systems",
        "title": "Model Registry & Experiment Tracking",
        "raw_sub": "Model Registry & Experiment Tracking (MLflow, Weights & Biases)",
        "definition": "A centralized governance hub that tracks hyperparameters, training metrics, code commits, and artifact binaries across thousands of experimental runs, providing stage transitions (Staging, Production, Archived) for reliable reproducibility.",
        "formula": "$$\\text{Run} = \\langle \\text{Git Commit}, \\,\\boldsymbol{\\theta}_{hypers}, \\,\\mathcal{M}_{metrics}, \\,\\mathcal{A}_{weights}, \\,\\text{Environment Hash} \\rangle$$",
        "formula_explanation": "Every model artifact is uniquely versioned with cryptographic hashes of code, dependencies, and trained weights.",
        "logic": "Without tracking, teams cannot reproduce models trained months ago or verify which dataset version created a production model, leading to catastrophic compliance and operational risks.",
        "example": "Using MLflow or Weights & Biases to log learning curves, evaluate candidate checkpoints, and promote the winning model checkpoint to `production` with a single click."
    },
    {
        "id": "high-throughput-serving-vllm",
        "topic_id": "mlops_root",
        "topic_label": "Production ML Systems & MLOps",
        "category": "mlops",
        "category_label": "MLOps & Systems",
        "title": "High-Throughput Serving & PagedAttention (vLLM)",
        "raw_sub": "High-Throughput Serving (vLLM PagedAttention, TensorRT-LLM, ONNX)",
        "definition": "Production inference optimization technologies that maximize GPU hardware utilization. PagedAttention (vLLM - Kwon et al., 2023) manages LLM Key-Value cache memory like virtual memory pages in operating systems, eliminating internal and external fragmentation.",
        "formula": "$$\\text{Memory Waste}_{vLLM} < 4\\% \\quad \\text{vs Conventional Serving: } 60\\% - 80\\% \\text{ waste}$$",
        "formula_explanation": "Continuous iteration-level batching dynamically injects new requests as soon as finished requests complete, without waiting for batch completion.",
        "logic": "Standard LLM serving pre-allocates contiguous memory for maximum possible sequence lengths (e.g. 4096 tokens), leaving huge empty memory gaps. PagedAttention allocates blocks dynamically on demand.",
        "example": "vLLM serves 20-30x more tokens per second per GPU compared to standard Hugging Face Transformers, enabling economical production scale."
    },
    {
        "id": "data-drift-concept-drift-monitoring",
        "topic_id": "mlops_root",
        "topic_label": "Production ML Systems & MLOps",
        "category": "mlops",
        "category_label": "MLOps & Systems",
        "title": "Data Drift vs Concept Drift Monitoring",
        "raw_sub": "Data Drift vs Concept Drift Monitoring (PSI, KS-Test)",
        "definition": "Data Drift refers to shifts in the input feature distribution $P(X)$ over time while relationship $P(Y|X)$ remains constant. Concept Drift occurs when the true statistical relationship between inputs and targets $P(Y|X)$ changes due to macroeconomic or real-world shifts.",
        "formula": "$$\\text{PSI} = \\sum_{i=1}^{B} (P_i - Q_i) \\ln\\left(\\frac{P_i}{Q_i}\\right), \\quad \\text{KS} = \\sup_x |F_{base}(x) - F_{curr}(x)|$$",
        "formula_explanation": "Population Stability Index (PSI): $\\text{PSI} < 0.1$ indicates stability, $> 0.25$ indicates significant drift requiring model retraining. KS is Kolmogorov-Smirnov test.",
        "logic": "Models trained on static historical data inevitably decay in accuracy as consumer habits, inflation, or seasons change. Automated drift alarms trigger automated retraining pipelines.",
        "example": "E-commerce spending during COVID-19 lockdown: purchase behavior shifted overnight. Concept drift rendered previous fraud detection models inaccurate until retrained."
    },
    {
        "id": "feature-stores-cicd-pipelines",
        "topic_id": "mlops_root",
        "topic_label": "Production ML Systems & MLOps",
        "category": "mlops",
        "category_label": "MLOps & Systems",
        "title": "Feature Stores & Continuous Training CI/CD",
        "raw_sub": "Feature Stores & Continuous Training CI/CD Pipelines",
        "definition": "A feature store (e.g. Feast, Hopsworks) provides a unified data platform with a dual interface: low-latency key-value storage (Redis) for real-time online inference, and distributed storage (Snowflake/BigQuery) with point-in-time time-travel joins for offline training.",
        "formula": "$$\\text{Time-Travel Join: } \\forall (u, t) \\in \\text{Labels}, \\quad \\mathbf{x}_{features} = \\text{Feature}(u, \\tau \\le t)$$",
        "formula_explanation": "Strict point-in-time correctness guarantees training datasets never leak features that occurred after prediction event timestamp $t$.",
        "logic": "Training-serving skew (features computed differently in Python during training vs in C++/Java during online serving) is the #1 cause of silent production model failure.",
        "example": "Credit card fraud: real-time feature 'number of transactions in last 10 minutes' is served from Redis in 2ms during checkout and queried with exact timestamps for historical model training."
    },
    {
        "id": "fairness-accountability-auditing",
        "topic_id": "mlops_root",
        "topic_label": "Production ML Systems & MLOps",
        "category": "mlops",
        "category_label": "MLOps & Systems",
        "title": "Fairness, Accountability & Responsible AI Auditing",
        "raw_sub": "Fairness, Accountability & Responsible AI Auditing",
        "definition": "Auditing frameworks to identify, measure, and mitigate systemic bias, demographic disparities, and privacy leakage in production AI models. Enforces criteria such as Demographic Parity, Equalized Odds, and Differential Privacy.",
        "formula": "$$\\text{Demographic Parity: } P(\\hat{Y}=1 \\mid A=0) = P(\\hat{Y}=1 \\mid A=1)$$ $$\\text{Equalized Odds: } P(\\hat{Y}=1 \\mid A=0, Y=y) = P(\\hat{Y}=1 \\mid A=1, Y=y)$$",
        "formula_explanation": "$A \\in \\{0, 1\\}$ is a protected demographic attribute (gender, ethnicity, age) and $Y$ is the ground truth outcome.",
        "logic": "Models trained on historical data frequently reproduce historical socio-economic inequities. Formal auditing ensures algorithmic fairness before models are approved for lending, hiring, or healthcare.",
        "example": "Using Fairlearn or AIF360 to audit loan approval algorithms, ensuring qualified applicants receive equal acceptance rates regardless of gender."
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(MLOPS_CONCEPTS)} MLOps concepts successfully.")
