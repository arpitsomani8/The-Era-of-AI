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

    logits_data = {
        "id": "concept_logits_log_odds",
        "title": "Log-Odds & Logits",
        "topic_id": "ml_logistic",
        "topic_label": "Logistic Regression & Sigmoid",
        "category": "ml",
        "category_label": "Classical Machine Learning",
        "raw_subtopic": "Log-Odds & Logit Transformation: ln(p / (1-p))",
        "def": "Odds compare the likelihood of an event happening versus not happening. Log-odds (or logits) are the natural logarithm of those odds, transforming bounded probabilities into an unconstrained scale from -∞ to +∞.",
        "formula": "$$\\text{Log-Odds} = \\text{logit}(p) = \\ln\\left(\\frac{p}{1 - p}\\right) = w_1 x_1 + w_2 x_2 + b \\iff p = \\frac{1}{1 + e^{-z}}$$",
        "logic": "Probabilities are trapped between 0 and 1, making them impossible to fit with an ordinary straight line (w^T x + b) that can extend to infinity. The logit transformation maps the narrow [0, 1] probability range onto the entire real number line (-∞, +∞), allowing linear models to fit valid parameters.",
        "example": "A football team has an 80% chance of winning (p = 0.80). The odds of winning are 0.80 / 0.20 = 4 (meaning 4 to 1). Taking the natural log gives the log-odds: ln(4) ≈ 1.386. In machine learning, a model outputting a raw score of z = 1.386 translates back to an 80% predicted probability.",
        "tags": [
            "Logits",
            "Log-Odds",
            "Odds Ratio",
            "Logistic Regression",
            "Sigmoid",
            "Probability"
        ],
        "definition": "Odds compare the likelihood of an event happening versus not happening. Log-odds (or logits) are the natural logarithm of those odds, transforming bounded probabilities into an unconstrained scale from -∞ to +∞.",
        "formula_explanation": "",
        "simple_summary": "Think of probability, odds, and log-odds as three ways of expressing the same confidence on different scales: Probability is a percentage between 0% and 100%. Odds compare winning vs losing (like betting 4 to 1 at a horse race). Log-Odds (Logits) stretch those odds across the entire number line, from negative infinity to positive infinity. This lets machine learning models use simple linear math (w x + b) without ever getting stuck at 0% or 100%.",
        "core_terms": [
            {
                "term": "Probability vs. Odds",
                "what_is_it": "• Probability (p): How likely an event is out of all possibilities, strictly between 0.0 and 1.0.\n• Odds (p / (1 - p)): The ratio of the probability of an event happening to the probability of it NOT happening, ranging from 0 to +∞.",
                "analogy": "Rolling a 6-sided die: the probability of rolling a 1 is 1/6 (about 16.7%), but the odds of rolling a 1 are 1 to 5 (1/5 = 0.20).",
                "why_it_matters": "Beginners frequently confuse them; odds are the mathematical bridge connecting probabilities to linear models."
            },
            {
                "term": "What is a Logit / Log-Odds?",
                "what_is_it": "• Taking the natural logarithm of the odds: logit(p) = ln(p / (1 - p)).\n• In machine learning, 'logits' refers to the raw linear scores (z = w^T x + b) produced by a model before applying Sigmoid or Softmax.",
                "analogy": "An uncalibrated radio signal: the raw wave can be +50 or -30 microvolts, which your radio's tuner (Sigmoid) translates into audible volume.",
                "why_it_matters": "Logits can be any real number from -∞ to +∞, which allows standard linear algebra to work without crashing into probability boundaries."
            },
            {
                "term": "The Inverse Relationship (Logit ↔ Sigmoid)",
                "what_is_it": "• Logit and Sigmoid are mathematical inverses: they undo each other!\n• Logit(p) converts a bounded probability into an unconstrained raw score z.\n• Sigmoid(z) converts an unconstrained raw score z back into a valid probability p.",
                "analogy": "Freezing and melting: freezing turns liquid water into solid ice (logit), and melting turns ice back into liquid water (sigmoid).",
                "why_it_matters": "This two-way bridge is what allows Logistic Regression to be trained as a linear regression model and evaluated as a probabilistic classifier."
            }
        ],
        "symbol_guide": [
            {
                "symbol": "p",
                "meaning": "Probability",
                "plain_english": "The chance of the event occurring, strictly bounded inside 0 < p < 1"
            },
            {
                "symbol": "1 - p",
                "meaning": "Complementary Probability",
                "plain_english": "The chance of the event NOT occurring"
            },
            {
                "symbol": "p / (1 - p)",
                "meaning": "Odds",
                "plain_english": "The ratio of success to failure, ranging from 0 to +∞"
            },
            {
                "symbol": "ln",
                "meaning": "Natural Logarithm",
                "plain_english": "Logarithm with base e ≈ 2.71828"
            },
            {
                "symbol": "z / logit(p)",
                "meaning": "Log-Odds / Logit",
                "plain_english": "The unconstrained raw score, extending from -∞ to +∞"
            }
        ],
        "numerical_example": "Step-by-Step Walkthrough Across 3 Probability Levels:\nFormula: Odds = p / (1 - p) | Log-Odds = ln(Odds)\n\n1. Low Probability (p = 0.10 — Unlikely Event):\n• Odds = 0.10 / (1 - 0.10) = 0.10 / 0.90 = 1/9 ≈ 0.111 (1 to 9 odds)\n• Log-Odds = ln(0.111) ≈ -2.197 (Negative score!)\n\n2. Even Split (p = 0.50 — Coin Flip):\n• Odds = 0.50 / (1 - 0.50) = 0.50 / 0.50 = 1.0 (1 to 1 even odds)\n• Log-Odds = ln(1.0) = 0.000 (Exactly zero!)\n\n3. High Probability (p = 0.90 — Highly Likely Event):\n• Odds = 0.90 / (1 - 0.90) = 0.90 / 0.10 = 9.0 (9 to 1 odds)\n• Log-Odds = ln(9.0) ≈ +2.197 (Positive score!)\n\nNotice the perfect symmetry: p = 0.10 produces -2.197, and p = 0.90 produces +2.197!",
        "pitfalls": "Common Mistakes to Avoid:\n1. Confusing odds with probability: Odds of 4:1 mean an 80% probability (4 / (4 + 1)), NOT a 400% probability.\n2. Thinking logits must stay between 0 and 1: Logits can be any finite real number (-15.4, +42.0); only probabilities are bounded between 0 and 1.\n3. Thinking weights change probability by a fixed percentage: In linear regression, a weight of +2 increases y by 2 units. In logistic regression, a weight of +2 increases log-odds by 2 units, which translates to a different probability change depending on where you are on the S-curve.\n4. Confusing Logit with Sigmoid: Sigmoid converts a raw score into a probability; Logit converts a probability into a log-odds.\n5. Passing probabilities to functions expecting logits: Functions like PyTorch's BCEWithLogitsLoss expect raw unbounded scores; passing squashed probabilities will severely distort the loss calculation.",
        "core_logic": "Why this matters: Standard linear regression assumes an unconstrained output domain (-∞, +∞). Attempting to fit a line directly to probabilities violates this assumption, generating nonsensical predictions outside [0, 1]. Logistic Regression solves this by fitting the linear model to log-odds instead, guaranteeing valid probability calibration when inverted through Sigmoid.",
        "architectural_logic": "In deep learning frameworks, the final linear layer of classification models outputs raw logits (e.g. torch.nn.Linear(in_features, num_classes)). Softmax or Sigmoid is deferred to the loss function (CrossEntropyLoss, BCEWithLogitsLoss) to compute gradients directly on logits, which mathematically avoids numerical precision issues from exponentiating large numbers.",
        "key_takeaways": [
            "Probability vs Odds: Probability is a percentage (0 to 1); odds compare success to failure (0 to ∞).",
            "Logits are Unbounded: Taking the log of odds maps probabilities onto (-∞, +∞), enabling linear modeling.",
            "Inverses of Each Other: Logit turns probabilities into raw scores; Sigmoid turns raw scores into probabilities.",
            "Why Called Regression: Logistic Regression fits a linear regression line to log-odds, then converts them to probabilities."
        ],
        "definition_bullets": [
            "Odds: The ratio of the probability of an event occurring to the probability of it not occurring (p / (1 - p)).",
            "Logit: The natural logarithm of odds, ln(p / (1 - p)), converting probabilities into an unconstrained real-valued scale."
        ],
        "types_header": "The 3 Representations of Likelihood",
        "types_badge": "Mathematical Formulations",
        "quick_types": [
            {
                "type": "Probability (p)",
                "definition": "Strictly bounded between 0.0 and 1.0; intuitive for humans, risk assessment, and business decisions.",
                "looks_like": "Range: [0.0, 1.0]"
            },
            {
                "type": "Odds (p / (1 - p))",
                "definition": "The ratio of winning to losing; ranges from 0 to +∞, where 1.0 represents an even 50/50 coin flip.",
                "looks_like": "Range: [0.0, +∞)"
            },
            {
                "type": "Log-Odds / Logit (ln(Odds))",
                "definition": "The natural log of odds; maps onto the entire real number line (-∞, +∞), symmetric around zero.",
                "looks_like": "Range: (-∞, +∞)"
            },
            {
                "type": "The Logit Function",
                "definition": "The mathematical mapping function logit(p) = ln(p / (1 - p)) that translates probabilities into log-odds.",
                "looks_like": "logit: (0, 1) → (-∞, +∞)"
            }
        ],
        "connected_logic": [
            {
                "title": "Why It Is Called Logistic 'Regression'",
                "content": "• Ordinary linear regression predicts continuous values: y = w^T x + b.\n• If we set y to probability, the line will inevitably predict impossible numbers like -2.5 or +3.8.\n• Logistic Regression fixes this by making the Log-Odds the target of the linear equation: ln(p / (1 - p)) = w^T x + b.\n• Because it fits a linear regression line to log-odds, it is fundamentally a regression model used for classification!"
            },
            {
                "title": "Interpreting Odds Ratios (e^w)",
                "content": "• In Logistic Regression, each weight w_i represents the change in log-odds for a 1-unit increase in feature x_i.\n• Exponentiating the weight (e^w_i) gives the Odds Ratio!\n• For example, if a medical model has w_smoking = 0.693, then e^0.693 = 2.0, meaning smoking doubles the odds of disease (a 2x increase)."
            },
            {
                "title": "The S-Curve Dynamic: Why Probability Slopes Vary",
                "content": "• Because of the non-linear S-curve, a +1 increase in logit changes probability differently depending on where you start.\n• Near z = 0 (the steep middle), a +1 jump in logit moves probability from 50% to 73% (+23% jump!).\n• Out at z = 4 (the flat plateau), a +1 jump only moves probability from 98.2% to 99.3% (+1.1% jump)."
            },
            {
                "title": "Logits in Modern Deep Learning & LLMs",
                "content": "• In neural networks and Large Language Models (like GPT-4), the output of the final linear layer (before Softmax) is called the 'logits tensor'.\n• Each token in the vocabulary receives an unconstrained logit score representing raw evidence.\n• Temperature scaling (z / T) divides these logits before Softmax to control generation randomness and creativity."
            }
        ]
    }

    # 1. Update in concepts.json
    for c in concepts:
        if c.get("id") == "concept_logits_log_odds":
            c.update(logits_data)
            print("Updated concept_logits_log_odds in concepts.json")
            break

    with open("src/data/concepts.json", "w", encoding="utf-8") as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)

    # 2. Update in all_concepts.json
    for c in all_concepts:
        if c.get("id") == "concept_logits_log_odds":
            c.update(logits_data)
            print("Updated concept_logits_log_odds in all_concepts.json")
            break

    with open("scripts/data_sources/all_concepts.json", "w", encoding="utf-8") as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)

    # 3. Update in concepts_ml.py
    pattern = r'\{\s*"id":\s*"concept_logits_log_odds".*?\},(?=\s*\{\s*"id":\s*"concept_multiclass_softmax")'
    match = re.search(pattern, py_content, re.DOTALL)
    if match:
        lines = json.dumps(logits_data, indent=4, ensure_ascii=False).splitlines()
        indented_replacement = "\n".join("    " + line for line in lines) + ","
        py_content = py_content[:match.start()] + indented_replacement + py_content[match.end():]
        with open("scripts/data_sources/concepts_ml.py", "w", encoding="utf-8") as f:
            f.write(py_content)
        print("Updated concept_logits_log_odds in concepts_ml.py")
    else:
        print("Could not find regex match in concepts_ml.py")

if __name__ == "__main__":
    main()
