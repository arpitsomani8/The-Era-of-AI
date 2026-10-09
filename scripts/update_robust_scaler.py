import json

ROBUST_SCALER_UPDATE = {
    "def": "Robust Scaler is an outlier-resilient feature scaling technique that centers data by subtracting the Median (Q2) and scales it by dividing by the Interquartile Range (IQR = Q3 - Q1), preventing extreme values from distorting scaling parameters.",
    "definition": "Robust Scaler is an outlier-resilient feature scaling technique that centers data by subtracting the Median (Q2) and scales it by dividing by the Interquartile Range (IQR = Q3 - Q1), preventing extreme values from distorting scaling parameters.",
    "formula": "$$x_{\\text{robust}} = \\frac{x - \\text{Median}(X)}{\\text{IQR}(X)} = \\frac{x - Q_2}{Q_3 - Q_1}, \\quad \\text{IQR} = Q_3 - Q_1$$",
    "formula_explanation": "",
    "logic": "StandardScaler uses mean and standard deviation, which are easily dragged away by extreme values. RobustScaler computes its center and spread strictly from the middle 50% of the dataset (Median and IQR), making it mathematically immune to extreme tails while keeping genuine outliers clearly visible.",
    "example": "Financial fraud detection: In a transaction dataset with typical purchases between $20 and $100 and a single $5,000,000 fraud wire, RobustScaler centers around median $50 and divides by IQR $40. Regular purchases spread cleanly between -1 and +1, while the fraud event scores +124,998.75 in the distant tail.",
    "simple_summary": "RobustScaler scales your features using the Median and Interquartile Range (IQR) instead of the Mean and Standard Deviation. Because the middle 50% of your data sets the rules, extreme outliers cannot distort your scaling parameters. Normal data stays cleanly spread out between -1 and +1, while outliers stay safely isolated in the far tails.",
    "core_terms": [
        {
            "term": "Robust Scaler (Median & IQR Scaling)",
            "what_is_it": "• A linear feature scaling method that centers data by subtracting the Median (50th percentile) and divides by the Interquartile Range (IQR = 75th - 25th percentile).\n• Unlike Min-Max or StandardScaler, its scaling parameters are calculated strictly from the middle 50% of the data, making them immune to extreme outlier distortion.",
            "analogy": "Calibrating a room thermometer based on typical spring and autumn weather, rather than letting one freak blizzard or heatwave throw off the entire temperature gauge.",
            "why_it_matters": "Normal observations remain spread out cleanly between -1 and +1, while genuine outliers remain intact and clearly identifiable in the distant tails."
        },
        {
            "term": "The 50% Breakdown Point (Robust Statistics)",
            "what_is_it": "• The proportion of corrupt or extreme data points a statistical estimator can handle before producing an arbitrary or invalid result.\n• While the sample mean and variance have a breakdown point of 0% (a single infinite outlier ruins them completely), the median has a 50% breakdown point and IQR has 25%, guaranteeing robust stability.",
            "analogy": "A democracy governed by majority vote (50% threshold) versus a veto system where one single billionaire can overturn the law for everyone else.",
            "why_it_matters": "Protects machine learning models from having their weights and decision boundaries hijacked by rogue sensor glitches or astronomical fraud spikes."
        },
        {
            "term": "Preserving Outliers vs. Erasing Them",
            "what_is_it": "• The core engineering principle that RobustScaler does not clip, round, or delete outliers—it simply prevents them from skewing the scaling parameters.\n• An extreme event (like a $5M fraud transfer) retains its massive relative distance (scaling to +995.0), giving anomaly detection models an unmistakable detection signal.",
            "analogy": "Giving VIP visitors a special badge rather than kicking them out of the building or forcing everyone else to dress like them.",
            "why_it_matters": "Essential for cybersecurity and fraud detection where the outlier is the most valuable predictive signal you are trying to detect."
        }
    ],
    "types_header": "Configuration Options & Specialized Scenarios",
    "types_badge": "Outlier Resilience",
    "quick_types": [
        {
            "type": "RobustScaler(with_centering=True)",
            "definition": "Centers data by subtracting median and scales by IQR; standard default for dense tabular features.",
            "looks_like": "scaler = RobustScaler().fit(X_train)"
        },
        {
            "type": "RobustScaler(with_centering=False)",
            "definition": "Scales by IQR without subtracting median; mandatory for sparse matrices to preserve sparsity without crashing RAM.",
            "looks_like": "RobustScaler(with_centering=False).fit(X_sparse)"
        },
        {
            "type": "Custom Quantile Ranges",
            "definition": "Configuring custom percentiles (e.g. 10th to 90th percentiles) instead of IQR (25th-75th) to tune spread sensitivity.",
            "looks_like": "RobustScaler(quantile_range=(10.0, 90.0))"
        },
        {
            "type": "Financial Fraud Preprocessor",
            "definition": "Scaling transaction amounts so everyday purchases ($20-$100) are not crushed by multi-million dollar fraud wires.",
            "looks_like": "X_scaled = RobustScaler().fit_transform(tx_amounts)"
        },
        {
            "type": "Cybersecurity DDoS Packet Scaler",
            "definition": "Preserving normal network traffic (10-100 req/min) while allowing millions of DDoS packets to spike into distant tails.",
            "looks_like": "RobustScaler().fit_transform(packet_rates)"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "x_robust",
            "meaning": "Robust Scaled Value",
            "plain_english": "The scaled observation centered at median 0 and normalized by interquartile spread"
        },
        {
            "symbol": "x",
            "meaning": "Raw Feature Observation",
            "plain_english": "The original unscaled numerical measurement for data instance i"
        },
        {
            "symbol": "Median(X) / Q_2",
            "meaning": "Sample Median",
            "plain_english": "The 50th percentile, representing the robust central tendency"
        },
        {
            "symbol": "IQR(X)",
            "meaning": "Interquartile Range",
            "plain_english": "The spread of the middle 50% of observations: Q3 - Q1"
        },
        {
            "symbol": "Q_1",
            "meaning": "First Quartile",
            "plain_english": "The 25th percentile boundary of the training distribution"
        },
        {
            "symbol": "Q_3",
            "meaning": "Third Quartile",
            "plain_english": "The 75th percentile boundary of the training distribution"
        }
    ],
    "numerical_example": "The Big Three Scalers Compared on 5 Normal Workers + 1 Billionaire:\nSalaries ($k): [$40, $45, $50, $55, $60, $10,000]\n• Median Q2 = $52.5k\n• Q1 (25th percentile) = $45.0k, Q3 (75th percentile) = $57.5k\n• IQR = Q3 - Q1 = $57.5k - $45.0k = $12.5k\n\n1. RobustScaler Transformation (x_robust = (x - Q2) / IQR):\n   • Worker 1 ($40k): (40 - 52.5) / 12.5 = -12.5 / 12.5 = -1.00\n   • Worker 2 ($45k): (45 - 52.5) / 12.5 = -7.5 / 12.5 = -0.60\n   • Worker 3 ($50k): (50 - 52.5) / 12.5 = -2.5 / 12.5 = -0.20\n   • Worker 4 ($55k): (55 - 52.5) / 12.5 = +2.5 / 12.5 = +0.20\n   • Worker 5 ($60k): (60 - 52.5) / 12.5 = +7.5 / 12.5 = +0.60\n   • Billionaire ($10,000k): (10,000 - 52.5) / 12.5 = 9,947.5 / 12.5 = +795.8\n\n2. Comparison Against Other Scalers:\n   • MinMaxScaler: Normal workers are compressed into [0.000, 0.002]—variance destroyed!\n   • StandardScaler: Mean is pulled to $1,708k, clumping all normal workers at -0.45.\n   • RobustScaler: Normal workers are cleanly distributed across [-1.0, +0.6], and the billionaire remains isolated at +795.8!",
    "pitfalls": "Common Pitfall: Mistakenly assuming that RobustScaler removes, clips, or bounds outliers. RobustScaler is unbounded; extreme observations will receive huge scaled scores (e.g. +795.8). If your model requires strictly bounded inputs (like neural networks with sigmoid heads), follow RobustScaler with Outlier Clipping or use RobustScaler in combination with non-linear transforms. Also, beware of features where > 50% of values are identical (IQR = 0).",
    "core_logic": "Why this matters: In datasets with heavy tails or severe anomalies, parametric estimators (mean and standard deviation) fail catastrophically. RobustScaler calculates its scaling coordinates strictly from the central 50% probability mass, guaranteeing that typical data points retain full variance while outliers are prevented from dominating loss gradients.",
    "architectural_logic": "In production enterprise pipelines, RobustScaler is fit strictly on training splits and persisted inside Scikit-Learn Pipeline or Feature Store definitions. For high-throughput online inference, precalculated median and IQR vectors are stored in low-latency key-value stores (e.g. Redis) to perform vector normalization in sub-millisecond execution times.",
    "connected_logic": [
        {
            "title": "Fraud Detection & Anomaly Signatures",
            "content": "• In credit card fraud models, 99.9% of transactions are under $200, while fraudulent wire transfers or account takeovers can reach millions.\n• Standard scaling inflates sample standard deviation, shrinking regular transactions into an indistinguishable clump; RobustScaler preserves everyday spending resolution while projecting fraud into distant decision boundaries."
        },
        {
            "title": "Network Intrusion & DDoS Telemetry",
            "content": "• In server monitoring, normal user request rates fluctuate within a modest baseline, whereas distributed denial-of-service (DDoS) attacks flood endpoints with millions of packets.\n• RobustScaler anchors the feature origin to typical operating conditions (Q2), enabling threshold detectors and Isolation Forests to cleanly trigger alarms without model recalibration."
        },
        {
            "title": "Loss Function Gradient Stability in Support Vector Machines",
            "content": "• Distance- and margin-based algorithms like SVMs with RBF kernels rely on squared Euclidean distances (exp(-γ ||x_i - x_j||²)) across support vectors.\n• Unscaled or mean-distorted features cause kernel gram matrices to collapse toward zero or identity; RobustScaler preserves accurate kernel inner products for the vast majority of support vectors."
        },
        {
            "title": "Strict Train-Test Pipeline Encapsulation",
            "content": "• Computing median and IQR across the entire dataset before splitting leaks holdout distribution percentiles into the training workflow.\n• In production ML pipelines, RobustScaler is fitted strictly on the training partition and serialized inside a Scikit-Learn Pipeline or Feature Store to transform test batches consistently."
        }
    ],
    "key_takeaways": [
        "Median & IQR Foundation: Centers data using the Median (50th percentile) and scales using IQR (75th - 25th), neutralizing outlier influence.",
        "Variance Protection: Prevents extreme values from crushing regular observations into narrow clumps, unlike Min-Max or StandardScaler.",
        "Unbounded Outlier Retention: Outliers are not deleted or clipped; they remain clearly isolated in the distant tails as strong predictive signals.",
        "Sparse Matrix Caution: When working with sparse data, set with_centering=False to avoid converting implicit zeros into dense memory-consuming floats."
    ],
    "definition_bullets": [
        "Robust Scaler: A feature scaling technique that normalizes numerical data using the median and interquartile range (IQR) to withstand extreme outliers.",
        "Interquartile Range (IQR): The statistical spread covering the middle 50% of the distribution, calculated as Q3 minus Q1."
    ]
}

def update_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    found = False
    for item in data:
        if item.get('id') == 'concept_robust_scaler':
            item.update(ROBUST_SCALER_UPDATE)
            found = True
            break
            
    if not found:
        print(f"Warning: concept_robust_scaler not found in {filepath}")
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
        if item.get('id') == 'concept_robust_scaler':
            item.update(ROBUST_SCALER_UPDATE)
            break
            
    new_content = '"""\nConcepts Database: Data Preparation & Exploration (22 Concepts)\n"""\n\nDATA_CONCEPTS = ' + json.dumps(mod.DATA_CONCEPTS, indent=4, ensure_ascii=False) + '\n'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

update_concepts_data_prep()
