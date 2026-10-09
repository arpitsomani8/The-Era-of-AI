import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
CONCEPTS_PATH = os.path.join(ROOT_DIR, "src", "data", "concepts.json")
ALL_CONCEPTS_PATH = os.path.join(SCRIPT_DIR, "data_sources", "all_concepts.json")
MATH_PY = os.path.join(SCRIPT_DIR, "data_sources", "concepts_math.py")

bayes_concept = {
    "id": "concept_bayes_theorem",
    "title": "Bayes' Theorem: Prior, Likelihood & Posterior",
    "topic_id": "math_prob",
    "topic_label": "Probability & Statistical Inference",
    "category": "math",
    "category_label": "Mathematical Foundations",
    "raw_subtopic": "Bayes' Theorem: Prior, Likelihood, Evidence & Posterior",
    "def": "Bayes' Theorem is the fundamental mathematical formula for updating the probability of a hypothesis as new evidence or data is observed: Posterior ∝ Likelihood × Prior.",
    "formula": "$$P(H \\mid D) = \\frac{P(D \\mid H) \\cdot P(H)}{P(D)}, \\quad P(D) = P(D \\mid H)P(H) + P(D \\mid \\neg H)P(\\neg H)$$",
    "logic": "Provides a mathematically sound framework to merge domain knowledge (Prior) with observed data (Likelihood) into an updated probability (Posterior). In ML, setting Gaussian priors on weights derives L2 regularization, while Bayesian Neural Networks use it to quantify uncertainty.",
    "example": "Spam filtering: If 10% of emails are spam (Prior P(S)=0.1), and 80% of spam contains 'cash prize' vs 1% of clean mail, Bayes' Theorem calculates the posterior chance that an email with 'cash prize' is spam as ~89.9%.",
    "tags": [
        "Bayes Theorem",
        "Probability",
        "Prior",
        "Likelihood",
        "Posterior",
        "Naive Bayes",
        "Regularization"
    ],
    "raw_sub": "Bayes' Theorem: Prior, Likelihood, Evidence & Posterior",
    "definition": "Bayes' Theorem calculates how much our beliefs should update when observing new evidence, stating that the Posterior probability is proportional to Likelihood multiplied by Prior.",
    "formula_explanation": "P(H|D) is the updated posterior belief. P(D|H) is the likelihood of observing data D under hypothesis H. P(H) is the baseline prior belief. P(D) is the total marginal evidence normalizing probabilities between 0 and 1.",
    "simple_summary": "Bayes' Theorem is the logic of learning from evidence: your new belief (Posterior) equals how well your clue fits the theory (Likelihood) multiplied by how sensible the theory was in the first place (Prior).",
    "core_terms": [
        {
            "term": "Prior Probability P(H)",
            "what_is_it": "• What you believed before seeing any new data or clues.\n• Represents baseline historical knowledge or real-world background rarity (e.g., only 10% of all incoming emails are spam).",
            "analogy": "In a desert, your prior belief that it will rain today is 1% before you even look outside at the morning sky.",
            "why_it_matters": "Prevents AI models from jumping to wild conclusions when observing rare or noisy anomalies."
        },
        {
            "term": "Likelihood P(D | H)",
            "what_is_it": "• How probable the observed clue is if the hypothesis is actually true.\n• Answers: 'If this email is indeed spam, how likely is it to contain the phrase Claim your cash prize?'",
            "analogy": "If it actually rains, the chance of seeing dark gray storm clouds is 90%.",
            "why_it_matters": "In machine learning, likelihood directly defines training loss functions (such as Cross-Entropy and Mean Squared Error)."
        },
        {
            "term": "Posterior Probability P(H | D)",
            "what_is_it": "• Your updated, revised probability after considering the new evidence: Posterior ∝ Likelihood × Prior.\n• It balances how strong the new clue is against how plausible the hypothesis was in the first place.",
            "analogy": "After seeing dark storm clouds roll in, your revised probability of rain jumps from 1% up to 45%.",
            "why_it_matters": "The final probability used by AI systems for spam filtering, medical diagnostics, and autonomous decision-making."
        }
    ],
    "types_header": "The Components of Bayes' Theorem in AI",
    "types_badge": "Bayesian Pillars",
    "quick_types": [
        {
            "type": "Prior P(H)",
            "definition": "Baseline belief before observing data. In ML, sets regularizers (L1 / L2 weight decay).",
            "looks_like": "Baseline Rarity: P(Spam) = 0.10"
        },
        {
            "type": "Likelihood P(D | H)",
            "definition": "How well the hypothesis explains observed evidence. In ML, defines the training loss function.",
            "looks_like": "Model Compatibility: P(Words | Spam)"
        },
        {
            "type": "Evidence P(D)",
            "definition": "Total probability of observing the data across all hypotheses. Acts as a normalizing scale (0 to 1).",
            "looks_like": "Normalizing Constant: P(D|H)P(H) + P(D|¬H)P(¬H)"
        },
        {
            "type": "Posterior P(H | D)",
            "definition": "Updated belief after considering evidence. Forms final classification probability.",
            "looks_like": "Revised Belief: P(Spam | Words) = 0.64"
        },
        {
            "type": "Golden Proportionality",
            "definition": "Evidence P(D) is constant during optimization, so: Posterior ∝ Likelihood × Prior.",
            "looks_like": "AI Optimization Rule: Posterior ∝ Likelihood × Prior"
        }
    ],
    "symbol_guide": [
        {
            "symbol": "P(H | D)",
            "meaning": "Posterior Probability",
            "plain_english": "Updated belief in hypothesis H after observing data D"
        },
        {
            "symbol": "P(D | H)",
            "meaning": "Likelihood",
            "plain_english": "Probability of observing data D if hypothesis H is true"
        },
        {
            "symbol": "P(H)",
            "meaning": "Prior Probability",
            "plain_english": "Baseline plausibility of hypothesis H before seeing new data"
        },
        {
            "symbol": "P(D)",
            "meaning": "Marginal Evidence",
            "plain_english": "Total probability of seeing data D across all possible scenarios"
        },
        {
            "symbol": "P(¬H)",
            "meaning": "Complement Probability",
            "plain_english": "Probability that the hypothesis is false: 1 - P(H)"
        }
    ],
    "numerical_example": "Medical Diagnosis Example (The Base Rate Fallacy):\n• Prior P(Disease) = 1% (0.01)  ==>  P(No Disease) = 99% (0.99)\n• Test Accuracy P(Positive | Disease) = 90% (0.90)\n• False Positive P(Positive | No Disease) = 5% (0.05)\n\nQuestion: If a patient tests positive, what is the chance they actually have the disease?\n\n1. Calculate Total Evidence P(Positive):\n   • P(Positive) = (0.90 × 0.01) + (0.05 × 0.99) = 0.009 + 0.0495 = 0.0585\n\n2. Calculate Posterior P(Disease | Positive):\n   • P(Disease | Positive) = (0.90 × 0.01) / 0.0585 = 0.009 / 0.0585 ≈ 15.38%\n\nInsight:\nEven with a 90% accurate test, a positive result only means a ~15.4% chance of disease, because the initial prior was so rare (1%)!",
    "pitfalls": "Common Trap: The Base Rate Fallacy. People frequently ignore the Prior P(H) and assume a 90% accurate test means a 90% chance of disease. When the baseline condition is rare, most positive signals are actually false positives.",
    "core_logic": "Provides a formal mechanism to integrate domain knowledge (the Prior) with real observed data (the Likelihood) to reach a statistically sound revised conclusion (the Posterior).",
    "architectural_logic": "In machine learning, Maximum A Posteriori (MAP) estimation incorporates parameter priors into optimization. Placing a zero-mean Gaussian prior over neural weights mathematically yields L2 regularization (weight decay), preventing overfitting. Furthermore, Bayesian Neural Networks place distributions over weights to estimate predictive uncertainty.",
    "connected_logic": [
        {
            "title": "The Naive Bayes Classifier in NLP",
            "content": "• Assumes all input features (words in an email) are conditionally independent given the class label.\n• Despite this 'naive' independence assumption, it executes with extreme computational efficiency and remains a dependable gold standard for text classification."
        },
        {
            "title": "The Bridge to Regularization: MLE vs. MAP",
            "content": "• Maximum Likelihood Estimation (MLE) ignores priors, finding weights that maximize data likelihood alone.\n• Maximum A Posteriori (MAP) incorporates weight priors: a Gaussian prior on weights mathematically derives L2 Regularization (Ridge), while a Laplace prior derives L1 Regularization (Lasso)."
        },
        {
            "title": "Bayesian Neural Networks (BNNs) & AI Uncertainty",
            "content": "• Standard neural networks use fixed weights (w = 0.42), producing dangerously confident wrong answers on unfamiliar data.\n• BNNs replace weights with probability distributions (w ~ N(μ, σ²)); on out-of-distribution inputs, prediction variance explodes, allowing the AI to signal: 'I am uncertain.'"
        },
        {
            "title": "The Base Rate Fallacy: Why Priors Matter",
            "content": "• Ignoring the prior P(H) leads humans and algorithms to massively overestimate rare events when presented with positive signals.\n• Bayes' Theorem mathematically protects systems from overreacting to single sensational clues when baseline rates are low."
        }
    ],
    "key_takeaways": [
        "Bayes' Theorem updates belief based on evidence: Posterior ∝ Likelihood × Prior.",
        "Prior P(H) is what you knew before; Likelihood P(D|H) measures how well the hypothesis explains data; Posterior P(H|D) is the updated belief.",
        "Evidence P(D) acts as a normalizing constant ensuring probabilities sum to 1.",
        "MAP estimation with a Gaussian prior is mathematically equivalent to L2 regularization (weight decay).",
        "Bayesian Neural Networks replace deterministic weights with distributions to quantify model uncertainty."
    ],
    "definition_bullets": [
        "Prior P(H): Baseline probability of a hypothesis before observing new evidence.",
        "Likelihood P(D|H): Probability of observing the evidence given the hypothesis is true.",
        "Posterior P(H|D): Refined probability of the hypothesis after incorporating observed evidence."
    ]
}

# 1. Update src/data/concepts.json
with open(CONCEPTS_PATH, 'r', encoding='utf-8') as f:
    concepts = json.load(f)

for idx, c in enumerate(concepts):
    if c['id'] == 'concept_bayes_theorem':
        concepts[idx] = bayes_concept
        break

with open(CONCEPTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(concepts, f, indent=2, ensure_ascii=False)
print("Updated src/data/concepts.json for concept_bayes_theorem successfully!")

# 2. Update scripts/data_sources/all_concepts.json
if os.path.exists(ALL_CONCEPTS_PATH):
    with open(ALL_CONCEPTS_PATH, 'r', encoding='utf-8') as f:
        all_concepts = json.load(f)
    for idx, c in enumerate(all_concepts):
        if c['id'] == 'concept_bayes_theorem':
            all_concepts[idx] = bayes_concept
            break
    with open(ALL_CONCEPTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(all_concepts, f, indent=2, ensure_ascii=False)
    print("Updated scripts/data_sources/all_concepts.json successfully!")

# 3. Update concepts_math.py
if os.path.exists(MATH_PY):
    import importlib.util
    spec = importlib.util.spec_from_file_location("concepts_math", MATH_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    math_concepts = mod.MATH_CONCEPTS
    for idx, c in enumerate(math_concepts):
        if c['id'] == 'concept_bayes_theorem':
            math_concepts[idx] = bayes_concept
            break
    with open(MATH_PY, "w", encoding="utf-8") as f:
        f.write('"""\nConcepts Database: Mathematical Foundations (19 Concepts)\n"""\n\nMATH_CONCEPTS = ' + json.dumps(math_concepts, indent=4, ensure_ascii=False) + '\n')
    print("Updated concepts_math.py successfully!")
