import json
import os

CONCEPTS_PATH = r"c:\Users\arpit\OneDrive\Desktop\The Era of AI\src\data\concepts.json"
TOPICS_PATH = r"c:\Users\arpit\OneDrive\Desktop\The Era of AI\src\data\topics.json"
NODES_PATH = r"c:\Users\arpit\OneDrive\Desktop\The Era of AI\src\data\allNodes.json"

with open(CONCEPTS_PATH, "r", encoding="utf-8") as f:
    concepts = json.load(f)

with open(TOPICS_PATH, "r", encoding="utf-8") as f:
    topics = json.load(f)

with open(NODES_PATH, "r", encoding="utf-8") as f:
    nodes = json.load(f)

# 1. ADD THE 3 MISSING CONCEPTS
new_concepts = [
    {
        "id": "concept_group_attribution_bias",
        "title": "Group Attribution Bias (In-Group Bias & Out-Group Homogeneity)",
        "category": "eval",
        "category_label": "4. Model Evaluation",
        "topic_id": "eval_fairness_bias",
        "topic_label": "Fairness, Types of Bias & Mitigation",
        "def": "Group attribution bias occurs when a model generalizes characteristics from an individual to an entire group, or perceives members of an out-group as all being alike while seeing in-group members as diverse and nuanced.",
        "formula": "P(\\hat{y} = 1 \\mid G = A) \\neq P(\\hat{y} = 1 \\mid G = B)",
        "logic": "Human annotators and unbalanced datasets often over-generalize rare negative behaviors from minority groups while forgiving majority in-group members. Machine learning models amplify this skew into rigid stereotyping.",
        "example": "Credit scoring systems that penalize an applicant simply because they belong to a demographic group with higher average debt, ignoring their flawless personal financial history.",
        "tags": ["fairness", "bias", "group attribution", "ethics", "responsible ai"],
        "core_terms": [
            {
                "term": "In-Group Favoritism",
                "what_is_it": "The systematic tendency to evaluate members of one's own group more favorably and with greater individualized nuance.",
                "analogy": "A hiring manager who assumes graduates from their own alma mater are all brilliant individuals, giving them the benefit of the doubt.",
                "why_it_matters": "When historical training datasets were labeled by majority groups, models absorb their unconscious leniency toward in-groups."
            },
            {
                "term": "Out-Group Homogeneity",
                "what_is_it": "The psychological fallacy of viewing all members of an external group as 'all the same', denying them individual variation.",
                "analogy": "Assuming that everyone in another department or city thinks, acts, and behaves identically.",
                "why_it_matters": "Leads models to assign identical risk scores to all members of a demographic regardless of individual merit."
            }
        ],
        "symbol_guide": [
            {"symbol": "G", "meaning": "Demographic or protected group attribute", "plain_english": "e.g. age group, ethnicity, or region"},
            {"symbol": "P(ŷ = 1 | G = A)", "meaning": "Probability of positive outcome for Group A", "plain_english": "Approval rate for group A"},
            {"symbol": "P(ŷ = 1 | G = B)", "meaning": "Probability of positive outcome for Group B", "plain_english": "Approval rate for group B"}
        ],
        "numerical_example": "In a job screening test: 80% of applicants from Group A are scored positively (variance 0.35 across resumes), whereas 20% of applicants from Group B are scored positively with near-zero score variance (model treats all Group B resumes identically). Disparity ratio = 0.20 / 0.80 = 0.25 (violates the 80% four-fifths fairness rule).",
        "pitfalls": "Novice Trap: Removing sensitive attributes (like race or gender) from the dataset does NOT prevent group attribution bias! Models easily reconstruct protected traits through proxy features like zip codes, school names, and browsing habits."
    },
    {
        "id": "concept_production_ml_pipelines_automl",
        "title": "Production ML Pipelines, Randomization & AutoML",
        "category": "mlops",
        "category_label": "7. MLOps & Production",
        "topic_id": "mlops_hygiene",
        "topic_label": "Production Data Hygiene & Engineering Pitfalls",
        "def": "Production ML pipelines orchestrate automated data ingestion, validation, hyperparameter tuning, model training, and continuous deployment into deterministic, reproducible production DAG workflows.",
        "formula": "\\text{Pipeline}(D_t) = \\text{Deploy}(\\arg\\min_{\\theta} \\mathcal{L}(M_\\theta, \\text{Transform}(D_t)))",
        "logic": "Jupyter notebooks are great for exploration, but production systems require idempotent, containerized pipelines that automatically retrain and evaluate models when new data arrives without manual human intervention.",
        "example": "An e-commerce fraud detection pipeline that pulls daily transactions from Apache Kafka, runs automated feature scaling, retrains an XGBoost model, runs regression tests, and canary deploys the model to Kubernetes.",
        "tags": ["mlops", "pipelines", "automl", "orchestration", "kubernetes"],
        "core_terms": [
            {
                "term": "ML Pipeline DAG",
                "what_is_it": "A Directed Acyclic Graph specifying the exact sequence of data extraction, validation, training, and deployment steps.",
                "analogy": "A modern car assembly line where each robotic station performs one strict inspection or assembly task in order.",
                "why_it_matters": "Guarantees reproducibility and allows failed pipeline stages to retry automatically without restarting from scratch."
            },
            {
                "term": "Automated Machine Learning (AutoML)",
                "what_is_it": "Algorithmic search that automatically tests multiple feature transforms, model architectures, and hyperparameters to find the optimal model.",
                "analogy": "A master chef who systematically tests 50 slight variations of a recipe to find the version that wins the cooking contest.",
                "why_it_matters": "Saves hundreds of engineering hours by automating tedious grid/random/Bayesian hyperparameter sweeps."
            }
        ],
        "symbol_guide": [
            {"symbol": "D_t", "meaning": "Data batch collected at time window t", "plain_english": "The latest week of customer data"},
            {"symbol": "M_θ", "meaning": "Model parameterized by weights θ", "plain_english": "The trained model parameters"},
            {"symbol": "Transform(D)", "meaning": "Deterministic feature engineering pipeline", "plain_english": "Scaling, encoding, and imputation"}
        ],
        "numerical_example": "An AutoML pipeline evaluates 3 candidate models: Random Forest (F1: 0.84, latency: 12ms), LightGBM (F1: 0.89, latency: 4ms), and Deep MLP (F1: 0.88, latency: 45ms). LightGBM achieves the highest Pareto efficiency score and is automatically promoted to the canary staging server.",
        "pitfalls": "Novice Trap: Random seeds must be explicitly locked and logged across all pipeline stages! Failing to set random seeds makes it impossible to reproduce bugs when a pipeline run behaves erratically."
    },
    {
        "id": "concept_big_data_feature_stores",
        "title": "Big Data Infrastructure & Distributed Feature Stores",
        "category": "mlops",
        "category_label": "7. MLOps & Production",
        "topic_id": "mlops_hygiene",
        "topic_label": "Production Data Hygiene & Engineering Pitfalls",
        "def": "A centralized data management layer that curates, computes, stores, and serves standardized machine learning features for both offline batch training and ultra-low-latency real-time online inference.",
        "formula": "\\text{FeatureStore} = \\{\\text{Offline}: \\text{Parquet/Snowflake}, \\text{Online}: \\text{Redis/Cassandra} \\}",
        "logic": "Without a feature store, different teams recalculate the same features (like 'user 30-day average spend') with subtly different logic, creating training-serving skew and duplicating millions of dollars in compute costs.",
        "example": "Ride-sharing apps use Redis-backed feature stores to look up a driver's recent acceptance rate and proximity in less than 5 milliseconds when matching a ride.",
        "tags": ["feature store", "feast", "redis", "low latency", "big data"],
        "core_terms": [
            {
                "term": "Online Feature Store",
                "what_is_it": "An ultra-fast key-value store (like Redis or DynamoDB) serving the latest feature values with sub-10ms response times during live user queries.",
                "analogy": "A restaurant chef's pre-chopped ingredients counter right at their fingertips during the busy dinner rush.",
                "why_it_matters": "Live fraud detection or search ranking models must score transactions in under 20 milliseconds."
            },
            {
                "term": "Offline Feature Store",
                "what_is_it": "A scalable column-oriented database (like Snowflake, BigQuery, or Parquet on S3) storing historical feature values with point-in-time accuracy for training.",
                "analogy": "The temperature-controlled warehouse storing months of supplies in bulk.",
                "why_it_matters": "Enables time-travel queries to reproduce the exact state of features as they were when an event happened in the past."
            }
        ],
        "symbol_guide": [
            {"symbol": "x(t)", "meaning": "Feature vector computed at historical timestamp t", "plain_english": "Point-in-time accurate user stats"},
            {"symbol": "Latency < 10ms", "meaning": "Online query SLA", "plain_english": "Maximum allowed lookup delay during live serving"}
        ],
        "numerical_example": "Feature 'user_30d_purchases': At live checkout time, online store serves current count: 14 (retrieved in 2.3ms from Redis). During historical model retraining for an order placed on Oct 1st, offline store point-in-time lookup correctly returns count: 6 (avoiding future data leakage).",
        "pitfalls": "Novice Trap: Time-travel leakage! If your training query computes features using data timestamped AFTER the prediction event, your model will look brilliant in tests but fail disastrously in production."
    }
]

# Add new concepts if not already present
existing_ids = set(c["id"] for c in concepts)
for nc in new_concepts:
    if nc["id"] not in existing_ids:
        concepts.append(nc)
        print(f"Added new concept: {nc['id']}")

with open(CONCEPTS_PATH, "w", encoding="utf-8") as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print(f"Total concepts now: {len(concepts)}")

# 2. ADD THE 6 MISSING TOPICS TO allNodes.json
existing_node_ids = set(n["id"] for n in nodes)
missing_topics = [t for t in topics if t["id"] not in existing_node_ids]

for mt in missing_topics:
    node_entry = {
        "id": mt["id"],
        "category": mt["category"],
        "label": mt["label"],
        "level": 2,
        "x": mt.get("x", 0),
        "y": mt.get("y", 0),
        "def": mt.get("def", ""),
        "formula": mt.get("formula", ""),
        "logic": mt.get("logic", ""),
        "example": mt.get("example", ""),
        "subtopics": mt.get("subtopics", []),
        "connections": mt.get("connections", [f"{mt['category']}_root"])
    }
    nodes.append(node_entry)
    print(f"Added missing node to allNodes.json: {mt['id']} ({mt['label']})")

with open(NODES_PATH, "w", encoding="utf-8") as f:
    json.dump(nodes, f, indent=2, ensure_ascii=False)
print(f"Total nodes now in allNodes.json: {len(nodes)}")
