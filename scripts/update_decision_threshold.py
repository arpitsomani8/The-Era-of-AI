import json
import re

def main():
    # 1. Load concepts.json
    with open("src/data/concepts.json", "r", encoding="utf-8") as f:
        concepts = json.load(f)

    # 2. Load all_concepts.json
    with open("scripts/data_sources/all_concepts.json", "r", encoding="utf-8") as f:
        all_concepts = json.load(f)

    # 3. Load concepts_ml.py
    with open("scripts/data_sources/concepts_ml.py", "r", encoding="utf-8") as f:
        py_content = f.read()

    threshold_data = {
        "id": "concept_decision_threshold",
        "title": "Classification Decision Threshold",
        "topic_id": "ml_logistic",
        "topic_label": "Logistic Regression & Sigmoid",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Classification Threshold (Decision cutoff, default 0.5)",
        "def": "A classification decision threshold is the specific probability cutoff a model uses to convert a continuous predicted probability into a discrete class label.",
        "formula": "$$\\hat{y} = \\begin{cases} 1 & \\text{if } \\hat{p} \\ge \\tau \\\\ 0 & \\text{if } \\hat{p} < \\tau \\end{cases}, \\quad \\tau \\in [0, 1]$$",
        "logic": "A classification model does not natively output hard labels like 'Spam' or 'Fraud'—it outputs a probability percentage like 0.72. The decision threshold is the boundary line that decides whether 0.72 counts as positive or negative. Moving this threshold lets engineers balance false alarms against missed detections to fit real-world business priorities.",
        "example": "Fraud detection: A transaction has a predicted fraud probability of 0.25. Under the default 0.50 threshold, it would be labeled legitimate (missed fraud). By lowering the threshold to 0.20, the system flags the transaction for review, successfully stopping a $10,000 theft at the cost of a quick SMS confirmation.",
        "tags": [
            "Decision Threshold",
            "Confusion Matrix",
            "Precision-Recall Tradeoff",
            "Classification",
            "Logistic Regression",
            "Cost Curve"
        ],
        "definition": "A classification decision threshold is the specific probability cutoff a model uses to convert a continuous predicted probability into a discrete class label.",
        "formula_explanation": "",
        "simple_summary": "Think of a decision threshold like the sensitivity dial on an airport metal detector. If the detector is set super sensitive (low threshold), it beeps at every belt buckle and coin. You catch every dangerous item (high recall), but you cause long lines from false alarms (lower precision). If you turn the dial way down (high threshold), it only beeps for massive heavy metal objects. You never get false alarms (high precision), but you risk missing smaller dangers (lower recall).",
        "core_terms": [
            {
                "term": "What is a Decision Threshold (τ)?",
                "what_is_it": "• The cutoff number that divides continuous model probabilities into positive (Class 1) vs negative (Class 0).\n• When predicted probability p̂ ≥ τ, output Class 1; when p̂ < τ, output Class 0.",
                "analogy": "A passing grade cutoff in school: setting the pass mark at 50% vs 75% decides who passes and who fails.",
                "why_it_matters": "Turns abstract continuous probability percentages into actionable binary business decisions."
            },
            {
                "term": "The 4 Outcomes (The Confusion Matrix)",
                "what_is_it": "• True Positive (TP): Model flags fraud, and it actually is fraud (Correct detection).\n• False Positive (FP): Model flags fraud, but it is legitimate (False alarm).\n• True Negative (TN): Model says legitimate, and it is legitimate (Correct approval).\n• False Negative (FN): Model says legitimate, but it was actual fraud (Costly miss).",
                "analogy": "A smoke alarm: ringing during a real fire (TP), ringing from burnt toast (FP), staying quiet when all is safe (TN), staying quiet during a real fire (FN).",
                "why_it_matters": "In the real world, the financial and human costs of a False Positive and a False Negative are rarely equal."
            },
            {
                "term": "The Precision vs. Recall Trade-Off",
                "what_is_it": "• Precision = TP / (TP + FP): When the model raises a flag, how often is it right?\n• Recall = TP / (TP + FN): Of all real positive cases, how many did the model successfully catch?\n• Lowering threshold increases Recall but reduces Precision; raising threshold increases Precision but reduces Recall.",
                "analogy": "Fishing with a wide net (low threshold) catches all the salmon (high recall) but also lots of sea kelp (low precision); fishing with a spear (high threshold) catches only salmon (high precision) but lets many swim away (low recall).",
                "why_it_matters": "The central design dial for adjusting model behavior to match organizational priorities."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "p̂ (p-hat)",
                "meaning": "Predicted Probability",
                "plain_english": "The continuous confidence percentage output by the model, between 0.0 and 1.0"
            },
            {
                "symbol": "τ (tau) / t",
                "meaning": "Decision Threshold",
                "plain_english": "The chosen cutoff boundary (e.g. 0.50, 0.20, 0.85)"
            },
            {
                "symbol": "ŷ (y-hat)",
                "meaning": "Predicted Class Label",
                "plain_english": "The final discrete decision, strictly either 0 or 1"
            },
            {
                "symbol": "TP, TN",
                "meaning": "True Positives, True Negatives",
                "plain_english": "Correct predictions for the positive and negative classes"
            },
            {
                "symbol": "FP, FN",
                "meaning": "False Positives, False Negatives",
                "plain_english": "False alarm vs missed positive detection"
            }
        ],
        "numerical_example": "Evaluating 100 Transactions with 10 Real Frauds:\nModel outputs probabilities for the 100 transactions.\n\nScenario A: Default Threshold (τ = 0.50)\n• Flagged as fraud: 8 transactions\n• TP = 6, FP = 2, FN = 4, TN = 88\n• Precision = 6 / (6 + 2) = 75%\n• Recall = 6 / (6 + 4) = 60% (Missed 4 fraudulent transactions!)\n\nScenario B: Lower Threshold for Safety (τ = 0.20)\n• Flagged as fraud: 20 transactions\n• TP = 9, FP = 11, FN = 1, TN = 79\n• Precision = 9 / (9 + 11) = 45% (More false alarms)\n• Recall = 9 / (9 + 1) = 90% (Caught 9 out of 10 frauds!)\n\nTakeaway: Lowering the threshold from 0.50 to 0.20 raised recall from 60% to 90%, preventing 3 major thefts!",
        "pitfalls": "Common Mistakes to Avoid:\n1. Always defaulting to 0.5: 0.50 is just an arbitrary mathematical midpoint, rarely an optimal business threshold.\n2. Tuning the threshold on the Test Set: Tuning on test data leaks test set information into your model; always tune on validation folds.\n3. Calling model.predict() in production: Scikit-Learn's predict() hardcodes the 0.5 threshold; always call predict_proba() and apply your tuned threshold.\n4. Chasing raw accuracy on imbalanced data: A model predicting negative on everything achieves 99% accuracy when positive prevalence is 1%, but catches 0% of fraud.\n5. Ignoring asymmetric financial costs: Optimizing for F1-score treats False Positives and False Negatives symmetrically, but a $10,000 missed fraud is far worse than a $0.05 SMS verification false alarm.",
        "core_logic": "Why this matters: Machine learning models optimize statistical loss functions, not business value. Converting probabilities into actions requires an operational decision boundary that aligns with real-world asymmetric risk. Tuning the threshold bridges the gap between raw probability calibration and practical business outcomes.",
        "architectural_logic": "In production scoring services, models expose continuous probability endpoints. Thresholding is decoupled from model inference: a rule engine or policy service applies the operational threshold (y_pred = probs >= threshold), enabling risk teams to adjust thresholds in real time without retraining the machine learning model.",
        "key_takeaways": [
            "Converts Probabilities to Decisions: The threshold (τ) maps continuous probabilities [0, 1] into binary actions {0, 1}.",
            "The 0.5 Default Myth: 0.5 is arbitrary; high-stakes problems require tuning the threshold to match asymmetric costs.",
            "Lowering τ Boosts Recall: Catches more positive cases at the expense of more false alarms.",
            "Never Call model.predict(): In production, always extract probabilities via model.predict_proba() and apply your tuned threshold."
        ],
        "definition_bullets": [
            "Decision Threshold: The probability cutoff value used to convert a continuous probability prediction into a binary class decision.",
            "Confusion Matrix: A 2x2 table cross-referencing actual labels against predicted labels to track TP, FP, TN, and FN outcomes."
        ],
        "types_header": "Threshold Strategies Across Industries",
        "types_badge": "Real-World Applications",
        "quick_types": [
            {
                "type": "High-Recall Regime (Low Threshold: τ = 0.05 to 0.20)",
                "definition": "Used in cancer screening, fraud detection, and defect detection where a missed positive (FN) is disastrous.",
                "looks_like": "y_pred = (probs >= 0.10)"
            },
            {
                "type": "High-Precision Regime (High Threshold: τ = 0.80 to 0.95)",
                "definition": "Used in spam filtering and automated user bans where a false alarm (FP) causes severe user backlash.",
                "looks_like": "y_pred = (probs >= 0.85)"
            },
            {
                "type": "Balanced F1-Score Threshold",
                "definition": "Tuned to maximize the harmonic mean of precision and recall when False Positives and False Negatives have similar impact.",
                "looks_like": "argmax_t F1(t)"
            },
            {
                "type": "Cost-Sensitive Financial Threshold",
                "definition": "Tuned directly to minimize real-world monetary loss: Total Cost = (Cost_FP × FP) + (Cost_FN × FN).",
                "looks_like": "min_t Cost(t)"
            }
        ],
        "connected_logic": [
            {
                "title": "Why model.predict() is a Production Anti-Pattern",
                "content": "• In Scikit-Learn, calling model.predict(X) hardcodes the arbitrary 0.5 cutoff: (probs >= 0.5).astype(int).\n• In production engineering, this strips away all confidence information and forces an un-tuned cutoff.\n• Best practice: Always call probs = model.predict_proba(X)[:, 1] and apply y_pred = (probs >= tuned_threshold).astype(int)."
            },
            {
                "title": "Constructing the Financial Cost Curve",
                "content": "• In business, every error has an explicit dollar value: e.g. an undetected fraud (FN) costs $500, while sending an automated verification SMS (FP) costs $0.05.\n• Plot Total Dollar Cost vs. Threshold across τ ∈ [0.01, 0.99].\n• The global minimum of this curve reveals the exact operational threshold that saves the company the most money."
            },
            {
                "title": "Precision-Recall Curves vs. ROC Curves",
                "content": "• An ROC curve plots True Positive Rate vs False Positive Rate across all thresholds, but can look deceptively optimistic on heavily imbalanced datasets.\n• The Precision-Recall (PR) curve plots Precision vs Recall across all thresholds, focusing exclusively on the minority positive class.\n• For fraud, medical diagnoses, and rare events, always use PR curves to evaluate and pick your threshold."
            },
            {
                "title": "Probability Calibration (Platt Scaling & Isotonic)",
                "content": "• For a threshold to be meaningful, a predicted probability of 0.80 must mean that approximately 80 out of 100 cases are truly positive.\n• Many algorithms (like Naive Bayes and Tree ensembles) output distorted, uncalibrated probabilities.\n• Use Scikit-Learn's CalibratedClassifierCV (Platt sigmoid scaling or Isotonic regression) to calibrate probabilities before selecting thresholds."
            }
        ]
    }

    # 1. Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_decision_threshold":
            c.update(threshold_data)
            print("Updated concept_decision_threshold in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # 2. Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_decision_threshold":
            c.update(threshold_data)
            print("Updated concept_decision_threshold in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # 3. Update in concepts_ml.py
    pattern = r'\{\s*"id":\s*"concept_decision_threshold".*?\},(?=\s*\{\s*"id":\s*"concept_log_loss_classification")'
    match = re.search(pattern, py_content, re.DOTALL)
    if match:
        lines = json.dumps(threshold_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        py_content = py_content[:match.start()] + indented_replacement + py_content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(py_content)
        print("Updated concept_decision_threshold in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
